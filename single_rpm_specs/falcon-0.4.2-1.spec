%define		PNAME	falcon
Version:	0.4.2
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/FALCON-integrate
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	A set of tools for fast aligning long reads for consensus and assembly

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR      %{MODULE_VAR_PREFIX}FALCON

## PACKAGE DESCRIPTION
%description
The Falcon tool kit is a set of simple code collection which I use for studying efficient assembly algorithm for haploid and diploid genomes. It has some back-end code implemented in C for speed and some simple front-end written in Python for convenience.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
#%setup -n %{PNAME}-%{version}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

export CC=icc
export ncores=16
export falcon=`pwd`
export falcon_install=${RPM_BUILD_ROOT}/%{INSTALL_DIR}
export python_site=${falcon_install}/lib/python2.7/site-packages
export PATH=${falcon_install}/bin:${PATH}
export PYTHONPATH=${python_site}:${PYTHONPATH}

module purge
module load TACC
module load python/2.7.9 hdf5
export PYTHONUSERBASE=${falcon_install}
#pyINSTALL="python setup.py install --prefix=${falcon_install}"
pyINSTALL="pip install -U --user ./"

# Make python site-packages path
mkdir -p ${python_site}
[ "%{PLATFORM}" = "stampede" ] && easy_install --user pyparsing==1.5.7

TB=/work/03076/gzynda/rpmbuild/SOURCES/falcon.tar.gz
[ -d FALCON-integrate ] && rm -rf FALCON-integrate
if [ -e $TB ]
then
        tar -xzf $TB
        cd FALCON-integrate
else
        git clone git@github.com:PacificBiosciences/FALCON-integrate.git
        cd FALCON-integrate
        git checkout 4b7d4c95870176193615eb497c01e48f4688899d
        git submodule update --init --recursive
        cd ..
        tar -czf $TB FALCON-integrate
        cd FALCON-integrate
fi

## Make pypeFLOW
cd pypeFLOW
git checkout master
$pyINSTALL

## Make FALCON
cd ${falcon}/FALCON-integrate/FALCON
patch -p1 << "EOF"
diff --git a/setup.py b/setup.py
index 3dd7bf2..f4910fe 100755
--- a/setup.py
+++ b/setup.py
@@ -51,6 +51,5 @@ setup(name='falcon_kit',
       },
       scripts = scripts,
       zip_safe = False,
-      setup_requires=install_requires,
       install_requires=install_requires
      )
diff --git a/src/py/bash.py b/src/py/bash.py
index 228fc4d..9e7332a 100644
--- a/src/py/bash.py
+++ b/src/py/bash.py
@@ -18,7 +18,7 @@ def make_executable(path):
     mode |= (mode & 0444) >> 2    # copy R bits to X
     os.chmod(path, mode)
 
-def write_script_and_wrapper(script, wrapper_fn, job_done):
+def write_script_and_wrapper(script, wrapper_fn, job_done, tmpdir=""):
     """
     Write script to a filename based on wrapper_fn, in same directory.
     Write wrapper to call it,
@@ -57,20 +57,24 @@ def write_script_and_wrapper(script, wrapper_fn, job_done):
         # We are trying to avoid this problem:
         #   /bin/bash: bad interpreter: Text file busy
         exe = ''
-
+    if tmpdir:
+        trap = "trap 'touch {job_exit}; rm -rf {tmpdir}' EXIT"
+    else:
+        trap = "trap 'touch {job_exit}' EXIT"
+    trap = trap.format(**locals())
     wrapper = """
 set -vex
 cd {wdir}
-trap 'touch {job_exit}' EXIT
+{trap}
 ls -il {sub_script_bfn}
 hostname
 ls -il {sub_script_bfn}
 time {exe} ./{sub_script_bfn}
 touch {job_done}
-"""
-    wrapper = wrapper.format(**locals())
+""".format(**locals())
     with open(wrapper_fn, 'w') as ofs:
         ofs.write(wrapper)
+    make_executable(os.path.join(wdir, wrapper_fn))
     return job_done, job_exit
 
 def script_build_rdb(config, input_fofn_fn, run_jobs_fn):
@@ -138,13 +142,16 @@ def scripts_daligner(run_jobs_fn, db_prefix, rdb_build_done, pread_aln=False):
         job_uid = '%04x' %i
         daligner_cmd = xform_script(bash)
         bash = """
+function retry {{ for i in {{1..3}}; do ( $@ ) && return 0 || sleep 2; done; return 1; }}
 db_dir={db_dir}
 ln -sf ${{db_dir}}/.{db_prefix}.bps .
 ln -sf ${{db_dir}}/.{db_prefix}.idx .
 ln -sf ${{db_dir}}/{db_prefix}.db .
+sleep 1
 {daligner_cmd}
-#rm -f *.C?.las
-#rm -f *.N?.las
+sleep 1
+rm -f *.C?.las
+rm -f *.N?.las
 """.format(db_dir=db_dir, db_prefix=db_prefix, daligner_cmd=daligner_cmd)
         yield job_uid, bash
 
@@ -192,28 +199,45 @@ def scripts_merge(config, db_prefix, run_jobs_fn):
         #merge_script_file = os.path.abspath("%s/m_%05d/m_%05d.sh" %% (wd, p_id, p_id))
 
         script = []
+        script.append("function retry { for i in {1..3}; do ( $@ ) && return 0 || sleep 2; done; return 1; }")
         for line in bash_lines:
-            script.append(line.replace('&&', ';'))
+            script.append("retry %s" %% (line,))
         script.append("mkdir -p ../las_files")
         script.append("ln -sf ../m_%05d/%s.%d.las ../las_files" %% (p_id, db_prefix, p_id))
         script.append("ln -sf ./m_%05d/%s.%d.las .. " %% (p_id, db_prefix, p_id))
         yield p_id, '\n'.join(script + [''])
 
-def script_run_consensus(config, db_fn, las_fn, out_file_bfn):
+def script_run_consensus(config, db_fn, las_fn, out_file_bfn, tmpdir=""):
     """config: falcon_sense_option, length_cutoff
     """
     params = dict(config)
     params.update(locals())
+    ### Section to handle temporary directories
+    db_loc = db_fn
+    c_cmd = ""
+    d_cmd = ""
+    if tmpdir:
+        db_prefix, db_name = os.path.split(db_fn)
+        db_loc = os.path.join(tmpdir, db_name)
+        c_cmd = """
+mkdir {tmpdir}
+cp {db_prefix}/raw_reads.db {db_prefix}/.raw_reads.idx {db_prefix}/.raw_reads.bps {tmpdir}
+""".format(db_prefix=db_prefix, tmpdir=tmpdir)
+        d_cmd = "rm -rf {tmpdir}".format(tmpdir=tmpdir)
+    ### Section for skip
     if config["falcon_sense_skip_contained"]:
-        pipe = """LA4Falcon -H{length_cutoff} -fso {db_fn} {las_fn} | """
+        pipe = """LA4Falcon -H{length_cutoff} -fso {db_loc} {las_fn} | """
     else:
-        pipe = """LA4Falcon -H{length_cutoff}  -fo {db_fn} {las_fn} | """
+        pipe = """LA4Falcon -H{length_cutoff}  -fo {db_loc} {las_fn} | """
     pipe += """fc_consensus {falcon_sense_option} >| {out_file_bfn}"""
-
+    ### Generate main script
     script = """
 set -o pipefail
-%s
-""" %pipe
+{c_cmd}
+{pipe}
+{d_cmd}
+""".format(c_cmd=c_cmd, pipe=pipe, d_cmd=d_cmd)
+    params['db_loc'] = db_loc
     return script.format(**params)
 
 def script_run_falcon_asm(config, las_fofn_fn, preads4falcon_fasta_fn, db_file_fn):
diff --git a/src/py/functional.py b/src/py/functional.py
index 020c241..ee8cc13 100644
--- a/src/py/functional.py
+++ b/src/py/functional.py
@@ -70,7 +70,8 @@ def get_daligner_job_descriptions(run_jobs_stream, db_prefix):
     for dali, pairs in dali2pairs.items():
         sorts = [pair2sort[pair] for pair in sorted(pairs, key=lambda k: (int(k[0]), int(k[1])))]
         id = tuple(map(int, blocks_dali(dali)))
-        script = '\n'.join([dali] + sorts) + '\n'
+        sorts = map(lambda x: "retry %s" %% (x), sorts)
+        script = '\n'.join([dali,'sleep 2'] + sorts) + '\n'
         result[id] = script
     return result
 
diff --git a/src/py/mains/run.py b/src/py/mains/run.py
index e3acd16..09e2afe 100644
--- a/src/py/mains/run.py
+++ b/src/py/mains/run.py
@@ -54,7 +54,7 @@ def _run_script_slurm(job_data):
         sge_option = job_data["sge_option"]
         with open(script_fn, 'r') as original: data = original.read()
         with open(script_fn, 'w') as modified: modified.write("#!/bin/sh" + "\n" + data)
-        sge_cmd="sbatch -J {job_name} {sge_option} {script}".format(job_name=job_name, cwd=os.getcwd(),sge_option=sge_option, script=script_fn)
+        sge_cmd="sbatch -J {job_name} {sge_option} /bin/sh {script}".format(job_name=job_name, cwd=os.getcwd(),sge_option=sge_option, script=script_fn)
         system(sge_cmd, check=True)
 
 def _run_script_local(job_data):
@@ -317,19 +317,35 @@ def task_daligner_gather(self):
     fc_run_logger.debug('nblock=%d, out_dir:\n%s'%%(nblock, out_dict))
 
     # Create m_* dirs.
+    from multiprocessing import Pool
+    p = Pool(processes=48)
+    dirs = []
     for block in xrange(1, nblock+1):
         mdir = os.path.join(main_dir, 'm_%05d' %block) # By convention. pbsmrtpipe works differently.
-        mkdir(mdir)
+        dirs.append(mdir)
+    res = p.map(mkdir, dirs)
         # TODO: Remove existing symlinks?
     job_rundirs = [os.path.dirname(fn(dal_done)) for dal_done in out_dict.values()]
 
     # Symlink all daligner *.las.
+    cmds = []
+    tmp = []
+    tLimit = 30
     for block, las_path in support.daligner_gather_las(job_rundirs):
-            #fc_run_logger.warning('block: %s, las_path: %s' %%(block, las_path))
-            mdir = os.path.join(main_dir, 'm_%05d' %block) # By convention. pbsmrtpipe works differently.
-            las_path = os.path.relpath(las_path, mdir)
-            cmd = 'ln -sf {} {}'.format(las_path, mdir)
-            system(cmd)
+        #fc_run_logger.warning('block: %s, las_path: %s' %%(block, las_path))
+        mdir = os.path.join(main_dir, 'm_%05d' %block) # By convention. pbsmrtpipe works differently.
+        las_path = os.path.relpath(las_path, mdir)
+        newLas = os.path.join(mdir, os.path.basename(las_path))
+        cmd = '[ -e %s ] || ln -s %s %s'%%(newLas, las_path, mdir)
+        tmp.append(cmd)
+        if len(tmp) >= tLimit:
+            cmds.append('; '.join(tmp))
+            tmp = []
+    if len(tmp):
+        cmds.append('; '.join(tmp))
+    res = p.map(system, cmds)
+    p.close()
+    p.join()
     system("touch %s" %da_done)
 
 def create_daligner_tasks(run_jobs_fn, wd, db_prefix, rdb_build_done, config, pread_aln=False):
diff --git a/src/py/run_support.py b/src/py/run_support.py
index 2bbae32..e9c9124 100644
--- a/src/py/run_support.py
+++ b/src/py/run_support.py
@@ -9,6 +9,7 @@ import sys
 import tempfile
 import time
 import uuid
+import random
 
 job_type = None
 logger = None
@@ -258,7 +259,7 @@ level=NOTSET
 handlers=stream
 
 [logger_pypeflow]
-level=DEBUG
+level=INFO
 handlers=file_pypeflow
 qualname=pypeflow
 propagate=1
@@ -277,7 +278,7 @@ args=(sys.stderr,)
 
 [handler_file_pypeflow]
 class=FileHandler
-level=DEBUG
+level=INFO
 formatter=form01
 args=('pypeflow.log',)
 
@@ -385,5 +386,8 @@ def run_las_merge(script, job_done, config, script_fn):
     bash.write_script_and_wrapper(script, script_fn, job_done)
 
 def run_consensus(db_fn, las_fn, out_file_fn, config, job_done, script_fn):
-    script = bash.script_run_consensus(config, db_fn, las_fn, os.path.basename(out_file_fn))
-    bash.write_script_and_wrapper(script, script_fn, job_done)
+    tmpdir=''
+    if config['use_tmpdir']:
+        tmpdir = 'tmp_%06i'%%(int(random.random()*1000000))
+    script = bash.script_run_consensus(config, db_fn, las_fn, os.path.basename(out_file_fn), tmpdir)
+    bash.write_script_and_wrapper(script, script_fn, job_done, tmpdir)
EOF

sed -i '/setup_requires/d' setup.py
#python setup.py install --prefix=${falcon_install}
$pyINSTALL

## Make DAZZ_DB
cd ${falcon}/FALCON-integrate/DAZZ_DB
# use icc
sed -i 's/gcc/icc/g' Makefile
if [ "%{PLATFORM}" != "ls5" ]
then
	make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -xHOST -no-ansi-alias"
else
	make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -xAVX -axCORE-AVX2 -no-ansi-alias"
fi
[ -d ${falcon_install}/bin ] || mkdir ${falcon_install}/bin
cp fasta2DB DB2fasta quiva2DB DB2quiva DBsplit DBdust Catrack DBshow DBstats DBrm simulator fasta2DAM DAM2fasta ${falcon_install}/bin
## Make DALIGNER
cd ${falcon}/FALCON-integrate/DALIGNER
patch HPCdaligner.c -i - << "EOF"
406a407,408
>                 printf(" %s.%d.%s.%d.C%d.las",root,i,root,j,k);
>                 printf(" %s.%d.%s.%d.N%d.las",root,i,root,j,k);
410a413,414
>                 printf(" %s.%s.C%d.las",root,root,k);
>                 printf(" %s.%s.N%d.las",root,root,k);
EOF
case "%{PLATFORM}" in
	ls5)
		# Use 32 threads on LS5 since HT is on an this code is IO bound.
		sed -i 's/NTHREADS  4/NTHREADS  64/' filter.h
		sed -i 's/NSHIFT    2/NSHIFT    6/' filter.h
		make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -no-ansi-alias -xAVX -axCORE-AVX2"
		;;
	wrangler)
		sed -i 's/NTHREADS  4/NTHREADS  16/' filter.h
		sed -i 's/NSHIFT    2/NSHIFT    4/' filter.h
		make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -no-ansi-alias -xHOST"
		;;
	stampede)
		# Set the number of pthreads (NTHREADS) to 16 to for Stampede
		sed -i 's/NTHREADS  4/NTHREADS  16/' filter.h
		# Set NSHIFT =  log_2(NTHREADS) = 4
		sed -i 's/NSHIFT    2/NSHIFT    4/' filter.h
		make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -no-ansi-alias -xHOST"
		;;
	*)
		echo "The system %{PLATFORM} is currently unsupported."
		exit 1
		;;
esac
cp daligner HPCdaligner HPCmapper LAsort LAmerge LAsplit LAcat LAshow LAcheck daligner_p LA4Falcon DB2Falcon  ${falcon_install}/bin

## Install Steps End
#--------------------------------------

#--------------------------------------

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables: %{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME} distribution.

Documentation: https://github.com/PacificBiosciences/FALCON/wiki/Manual

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, PacBio")
whatis("Description: FALCON - A set of tools for fast aligning long reads for consensus and assembly")
whatis("URL: %{URL}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("PYTHONPATH",	pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("FALCON_PREFIX",		"%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

always_load("python/2.7.9","hdf5")
EOF
## Modulefile End
#--------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}

## POST
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
