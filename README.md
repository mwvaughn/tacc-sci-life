Overview
========
The Life Sciences Computing group at the Texas Advanced Computing Center (TACC) uses this repository to build modules for TACC's supercomputing systems

Older modules are in the "archive" directory.  The "scripts" directory contains helpful utility scripts.  The "include" directory contains system specific information that gets loaded during the RPM build process. SPEC files follow a specific naming convention to keep track of the version and revision information.  In general, new revisions are made because the previous version of the SPEC file contained an error (or in the case of Amber, the app updates itself with bugfixes as part of the build process). The naming convention follows this pattern:

<application name>-<major version>.<minor version>.<patch>-<spec revision number>.spec

Workflow
========

For an idea of how module building and testing works, let's take a look at Bowtie 2.2.4.  Login to a TACC system, and try this:

```
$ cd $WORK
$ mkdir rpmbuild && cd rpmbuild
$ git clone https://github.com/mwvaughn/tacc-sci-life.git SPECS
Cloning into 'SPECS'...
remote: Counting objects: 1568, done.
remote: Total 1568 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (1568/1568), 5.78 MiB | 3.61 MiB/s, done.
Resolving deltas: 100% (730/730), done.

$ cd SPECS

# now build the directory structure
$ ./scripts/buildDirectories.sh
creating ls4 directory
creating ls4/BUILD directory
creating ls4/RPMS directory
creating ls4/SOURCES directory
creating ls4/SRPMS directory
creating stampede directory
creating stampede/BUILD directory
creating stampede/RPMS directory
creating stampede/SOURCES directory
creating stampede/SRPMS directory
creating maverick directory
creating maverick/BUILD directory
creating maverick/RPMS directory
creating maverick/SOURCES directory
creating maverick/SRPMS directory

# download the bowtie source code. The location will be in the bowtie spec file:
$ grep -m1 -i "source" bowtie-2.2.4-1.spec
Source:  http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.4/bowtie2-2.2.4-source.zip

# now let's download the bowtie source in the appropriate SOURCES directory.
$ wget -P ../stampede/SOURCES http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.4/bowtie2-2.2.4-source.zip
# Note: if on Lonestar or Maverick, be sure to pick the correct sub-directory.
# e.g. on Lonestar: wget -P ../ls4/SOURCES http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.4/bowtie2-2.2.4-source.zip

# now build the spec file
$ rpmbuild -bb bowtie-2.2.4-1.spec
# if this command works, it should generate a .rpm file

# for testing, let's start by looking at the contents of the RPM:
$ rpm -qlp ../stampede/RPMS/x86_64/bowtie-2.2.4-1.x86_64.rpm
# this should list the contents of the RPM file.  make sure that everything that should be there is indeed there.

# now try installing it locally
$ ./scripts/myRpmInstall -h
Usage: myRpmInstall <prefix> <file.rpm>

$ mkdir $WORK/apps
$ ./scripts/myRpmInstall $WORK/apps ../ls4/RPMS/x86_64/bowtie-2.2.4-1.x86_64.rpm
Installing RPM
Preparing...                ########################################### [100%]
   1:bowtie                 ########################################### [100%]
Editing modulefile paths
Updating paths in the modulefile /work/01114/jfonner/apps/modulefiles/bowtie/2.2.4.lua
Checking the $MODULEPATH variable.
looks like the $MODULEPATH environment variable needs updating.
Check the README.md file if you aren't sure how to do that.

# looks like the modulefile was updated, but it is in a place that isn't in the $MODULEPATH yet.  Let's add it
$ module use $WORK/apps/modulefiles
$ module save
Saved current collection of modules to: default
$ module key bowtie
Rebuilding cache file, please wait ... done

---------------------------------------------------------------------------------------------------------------------------------------------------------
The following modules match your search criteria: "bowtie"
---------------------------------------------------------------------------------------------------------------------------------------------------------

  bowtie: bowtie/1.0.0, bowtie/1.1.1, bowtie/2.1.0, bowtie/2.2.4
    Ultrafast, memory-efficient short read aligner

---------------------------------------------------------------------------------------------------------------------------------------------------------
To learn more about a package enter:

   $ module spider Foo

where "Foo" is the name of a module

To find detailed information about a particular package you
must enter the version if there is more than one version:

   $ module spider Foo/11.1
---------------------------------------------------------------------------------------------------------------------------------------------------------

# Great! we see bowtie/2.2.4 in the list.  Let's try loading it to test the modulefile
$ ml bowtie/2.2.4

Lmod Error: Can not load: "bowtie/2.2.4" module without these modules loaded:
  perl

# OK, we have to load perl first
$ ml perl bowtie/2.2.4
$ jfonner@login2:SPECS (master)$ which bowtie2
/work/01114/jfonner/apps/bowtie/2.2.4/bowtie2
# success

# now test to see which libraries are called:
$ ldd `which bowtie2`
    not a dynamic executable

# that doesn't seem right... is this really an executable?
$ head -n1 `which bowtie2`
#!/usr/bin/env perl

# AHA! That's just a perl wrapper (that explains why the perl prerequisite is there).  Let's look for the real executables.
$ ls $TACC_BOWTIE_DIR
bowtie2          bowtie2-align-s  bowtie2-build-l  bowtie2-inspect    bowtie2-inspect-s  scripts
bowtie2-align-l  bowtie2-build    bowtie2-build-s  bowtie2-inspect-l  doc

$ for exe in $TACC_BOWTIE_DIR/bowtie2-*; do echo $(basename $exe); ldd $exe; echo "------"; done
bowtie2-align-l
    libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003001000000)
    libstdc++.so.6 => /opt/apps/gcc/4.4.5/lib64/libstdc++.so.6 (0x00002b213e5c8000)
    libm.so.6 => /lib64/libm.so.6 (0x0000003000c00000)
    libgcc_s.so.1 => /opt/apps/gcc/4.4.5/lib64/libgcc_s.so.1 (0x00002b213e8d9000)
    libc.so.6 => /lib64/libc.so.6 (0x0000003000400000)
    /lib64/ld-linux-x86-64.so.2 (0x0000003000000000)
------
bowtie2-align-s
    libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003001000000)
    libstdc++.so.6 => /opt/apps/gcc/4.4.5/lib64/libstdc++.so.6 (0x00002acfbacbc000)
    libm.so.6 => /lib64/libm.so.6 (0x0000003000c00000)
    libgcc_s.so.1 => /opt/apps/gcc/4.4.5/lib64/libgcc_s.so.1 (0x00002acfbafcd000)
    libc.so.6 => /lib64/libc.so.6 (0x0000003000400000)
    /lib64/ld-linux-x86-64.so.2 (0x0000003000000000)
------
bowtie2-build
    not a dynamic executable
------
bowtie2-build-l
    libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003001000000)
    libstdc++.so.6 => /opt/apps/gcc/4.4.5/lib64/libstdc++.so.6 (0x00002b657d7c2000)
    libm.so.6 => /lib64/libm.so.6 (0x0000003000c00000)
    libgcc_s.so.1 => /opt/apps/gcc/4.4.5/lib64/libgcc_s.so.1 (0x00002b657dad3000)
    libc.so.6 => /lib64/libc.so.6 (0x0000003000400000)
    /lib64/ld-linux-x86-64.so.2 (0x0000003000000000)
------
bowtie2-build-s
    libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003001000000)
    libstdc++.so.6 => /opt/apps/gcc/4.4.5/lib64/libstdc++.so.6 (0x00002b353ba06000)
    libm.so.6 => /lib64/libm.so.6 (0x0000003000c00000)
    libgcc_s.so.1 => /opt/apps/gcc/4.4.5/lib64/libgcc_s.so.1 (0x00002b353bd17000)
    libc.so.6 => /lib64/libc.so.6 (0x0000003000400000)
    /lib64/ld-linux-x86-64.so.2 (0x0000003000000000)
------
bowtie2-inspect
    not a dynamic executable
------
bowtie2-inspect-l
    libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003001000000)
    libstdc++.so.6 => /opt/apps/gcc/4.4.5/lib64/libstdc++.so.6 (0x00002b12d6128000)
    libm.so.6 => /lib64/libm.so.6 (0x0000003000c00000)
    libgcc_s.so.1 => /opt/apps/gcc/4.4.5/lib64/libgcc_s.so.1 (0x00002b12d6439000)
    libc.so.6 => /lib64/libc.so.6 (0x0000003000400000)
    /lib64/ld-linux-x86-64.so.2 (0x0000003000000000)
------
bowtie2-inspect-s
    libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003001000000)
    libstdc++.so.6 => /opt/apps/gcc/4.4.5/lib64/libstdc++.so.6 (0x00002b9e85e5f000)
    libm.so.6 => /lib64/libm.so.6 (0x0000003000c00000)
    libgcc_s.so.1 => /opt/apps/gcc/4.4.5/lib64/libgcc_s.so.1 (0x00002b9e86170000)
    libc.so.6 => /lib64/libc.so.6 (0x0000003000400000)
    /lib64/ld-linux-x86-64.so.2 (0x0000003000000000)
------
# OK, there are no "not found" messages.  That's good.  A bunch of libraries reference /opt/apps/gcc/4.4.5/lib64/, which is another module.  Let's try changing modules to make sure that we don't have a dependency there.
$ module list

Currently Loaded Modules:
  1) TACC-paths   2) Linux   3) cluster-paths   4) intel/13.0.2.146   5) mvapich2/1.9a2   6) xalt/0.4.6   7) cluster   8) TACC   9) perl/5.16.2

# try switching the compiler (intel in this case) and the MPI stack (mvapich2 in this case).
$ ml swap intel gcc
$ ml unload mvapich2
$ for exe in $TACC_BOWTIE_DIR/bowtie2-*; do echo $(basename $exe); ldd $exe; echo "------"; done
```

To be continued...

