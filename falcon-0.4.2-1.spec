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

if [ "%{PLATFORM}" != "ls5" ]
then
        module purge
        module load TACC
fi
module load python
module load hdf5

export CC=icc
export ncores=16
export falcon=`pwd`
export falcon_install=${RPM_BUILD_ROOT}/%{INSTALL_DIR}
export python_site=${falcon_install}/lib/python2.7/site-packages
export PATH=${falcon_install}/bin:${PATH}
export PYTHONPATH=${python_site}:${PYTHONPATH}

# Make python site-packages path
mkdir -p ${python_site}

[ -d FALCON-integrate ] && rm -rf FALCON-integrate
git clone --recursive git@github.com:PacificBiosciences/FALCON-integrate.git
cd FALCON-integrate
git checkout 4b7d4c95870176193615eb497c01e48f4688899d

## Make pypeFLOW
cd pypeFLOW
# have jobs sleep after between submissions so slurm isn't overloaded
sed -i '/jobsReadyToBeSubmitted.pop(0)/ a \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ time.sleep(2)' src/pypeflow/controller.py
python setup.py install --prefix=${falcon_install}

## Make FALCON
cd ${falcon}/FALCON-integrate/FALCON
# add /dev/shm patch
patch src/py/bash.py -i - << "EOF"
123a124
> sleep 1
125,126c126,128
< #rm -f *.C?.las
< #rm -f *.N?.las
---
> sleep 1
> rm -f *.C?.las
> rm -f *.N?.las
173a176
>         script.append("function retry { for i in {1..3}; do ( $@ ) && return 0 || sleep 2; done; return 1; }")
175c178
<             script.append(line.replace('&&', ';'))
---
>             script.append("retry "+line)
187c190
<         pipe = """LA4Falcon -H{length_cutoff} -fso {db_fn} {las_fn} | """
---
>         pipe = """LA4Falcon -H{length_cutoff} -fso /dev/shm/falcon/raw_reads {las_fn} | """
189c192
<         pipe = """LA4Falcon -H{length_cutoff}  -fo {db_fn} {las_fn} | """
---
>         pipe = """LA4Falcon -H{length_cutoff}  -fo /dev/shm/falcon/raw_reads {las_fn} | """
190a194
>     db_prefix = os.path.split(db_fn)[0]
193a198
> mkdir /dev/shm/falcon && cp %s/raw_reads.db %s/.raw_reads.bps %s/.raw_reads.idx /dev/shm/falcon/
195c200,201
< """ %pipe
---
> rm -rf /dev/shm/falcon
> """ % (db_prefix, db_prefix, db_prefix, pipe)
EOF
# fix dependencies
sed -i '/setup_requires/d' setup.py

python setup.py install --prefix=${falcon_install}

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
if [ "%{PLATFORM}" != "ls5" ]
then
	# Set the number of pthreads (NTHREADS) to 16 to for Stampede
	sed -i 's/NTHREADS  4/NTHREADS  16/' filter.h
	# Set NSHIFT =  log_2(NTHREADS) = 4
	sed -i 's/NSHIFT    2/NSHIFT    4/' filter.h
	make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -no-ansi-alias -xHOST"
else
	# Use 32 threads on LS5 since HT is on an this code is IO bound.
	sed -i 's/NTHREADS  4/NTHREADS  32/' filter.h
	sed -i 's/NSHIFT    2/NSHIFT    5/' filter.h
	make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -no-ansi-alias -xAVX -axCORE-AVX2"
fi
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

prereq("python","hdf5")
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
