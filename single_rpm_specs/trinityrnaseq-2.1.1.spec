%define PNAME trinityrnaseq
Version: 2.1.1
Release: 1
Summary: Trinity - De novo RNA-Seq Assembler
License: BSD
Group: Applications/Life Sciences
Source: /work/03076/gzynda/rpmbuild/SOURCES/trinityrnaseq-2.1.1.tar.gz
URL: https://github.com/trinityrnaseq/trinityrnaseq
Packager: TACC - gzynda@tacc.utexas.edu

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}TRINITY

## PACKAGE DESCRIPTION
%description
Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads. Trinity partitions the sequence data into many individual de Bruijn graphs, each representing the transcriptional complexity at at a given gene or locus, and then processes each graph independently to extract full-length splicing isoforms and to tease apart transcripts derived from paralogous genes.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

if [ "%{PLATFORM}" != "ls5" ]
then
	module purge
	module load TACC
else
	module use $HOME/apps/modulefiles
fi

ml samtools/1.3

#------------------------------------------------
# PATCH FILES
#------------------------------------------------
## Patch scaffold_iworm_contigs
patch trinity-plugins/scaffold_iworm_contigs/Makefile -li - << 'EOF'
1,2c1,3
< CXX    = g++
< prefix = ../htslib
---
> CXX    = icpc
> prefix = ${TACC_SAMTOOLS_DIR}
> IOMP = /opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64_lin/
5c6,7
<       $(CXX) -I$(prefix) -L$(prefix) ScaffoldIwormContigs.cpp error_checker.cpp -lhts -lz -o scaffold_iworm_contigs
---
> 	$(CXX) -I$(prefix)/include -L$(prefix)/lib ScaffoldIwormContigs.cpp error_checker.cpp -lhts -lz -Wl,-rpath,$(IOMP) -o scaffold_iworm_contigs
> 	rm *.cpp Makefile *.h
9,10d10
< 
< 
EOF
## Patch fastool
patch trinity-plugins/fstrozzi-Fastool-7c3e034f05/Makefile -i - << 'EOF'
1,2c1,2
< CC     = gcc
< CFLAGS = -O2 -std=c99 -Werror
---
> CC     = icc
> CFLAGS = -O3 -xAVX -axCORE-AVX2 -std=c99
EOF
## Patch slclust
patch trinity-plugins/slclust/src/Makefile -i - << 'EOF'
37,38c37,38
< CFLAGS        = -I${INCLUDE} ${LOCAL_CFLAGS}
< CC            = g++ ${CFLAGS}
---
> CFLAGS        = -I${INCLUDE} ${LOCAL_CFLAGS} -O3 -xAVX -axCORE-AVX2
> CC            = icpc ${CFLAGS}
EOF
## Patch plugins
patch trinity-plugins/Makefile -i - << 'EOF'
12a13,14
> IOMP = /opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64_lin/
> 
16c18
< 	ln -sf ${TRIMMOMATIC_CODE} Trimmomatic
---
> 	mv ${TRIMMOMATIC_CODE} Trimmomatic
20,22c22
< 	tar xvf samtools-0.1.19.tar.bz2
< 	cd samtools-0.1.19 && $(MAKE) LIBPATH=-ltinfo
< 	mv samtools-0.1.19/samtools ./BIN/.
---
> 	rm samtools-0.1.19.tar.bz2
26,27c26,28
< 	cd ./tmp.jellyfish/ && ./configure CC=gcc CXX=g++ --enable-static --disable-shared --prefix=`pwd` && $(MAKE) LDFLAGS="-lpthread -all-static" AM_CPPFLAGS="-Wall -Wnon-virtual-dtor -I"`pwd`"/include"
< 	mv tmp.jellyfish jellyfish
---
> 	mkdir jellyfish
> 	cd ./tmp.jellyfish/ && ./configure CC=icc CXX=icpc CXXFLAGS="-O3 -xAVX -axCORE-AVX2" --disable-shared --prefix=`pwd`/../jellyfish && $(MAKE) LDFLAGS="-lpthread -all-static" AM_CPPFLAGS="-Wall -Wnon-virtual-dtor -I"`pwd`"/include" install
> 	rm tmp.jellyfish && rm -rf ${JELLYFISH_CODE} ${JELLYFISH_CODE}.tar.gz
30,32c31
< #	tar xjvf htslib-1.2.1.tar.bz2
< #	cd htslib-1.2.1 && ./configure && $(MAKE)
< 	tar xvf ${HTSLIB_CODE} && cd htslib && $(MAKE)
---
> 	rm htslib*
38,39c37,39
< 	cd ${FASTOOL_CODE} && $(MAKE)
< 	ln -sf ${FASTOOL_CODE} fastool
---
> 	mkdir fastool
> 	cd ${FASTOOL_CODE} && $(MAKE) && mv fastool ../fastool/
> 	rm -rf ${FASTOOL_CODE}
43,44c43,45
< 	cd ${PARAFLY_CODE} && sh ./configure --prefix=`pwd` && $(MAKE) install
< 	ln -sf ${PARAFLY_CODE} parafly
---
> 	mkdir parafly
> 	cd ${PARAFLY_CODE} && sh ./configure CXX=icpc CXXFLAGS="-O3 -xAVX -axCORE-AVX2" LDFLAGS="-Wl,-rpath,$(IOMP)" --prefix=`pwd`/../parafly && $(MAKE) install
> 	rm -rf ${PARAFLY_CODE}
53d53
< 
EOF
## Patch main Makefile
patch Makefile -i - << 'EOF'
10,11c10,13
<  INCHWORM_CONFIGURE_FLAGS = CXX=icpc CXXFLAGS="-fast"
<  CHRYSALIS_MAKE_FLAGS = COMPILER=icpc
---
>  IOMP = /opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64_lin/
>  IFLAGS = -O3 -xAVX -axCORE-AVX2
>  INCHWORM_CONFIGURE_FLAGS = CXX=icpc CXXFLAGS="$(IFLAGS)" LDFLAGS="-Wl,-rpath,$(IOMP)"
>  CHRYSALIS_MAKE_FLAGS = COMPILER=icpc SYS_LINK="-Wl,-rpath,$(IOMP)" SYS_OPT="$(IFLAGS)"
EOF
## Patch install tests
patch util/support_scripts/trinity_install_tests.sh -i - << 'EOF'
62c62
< if [ -e "trinity-plugins/BIN/samtools" ]
---
> if [ -x "$(which samtools 2>/dev/null)" ]
EOF

#------------------------------------------------
# Make Trinity
#------------------------------------------------
make -j 4 TRINITY_COMPILER=intel
make -j 4 TRINITY_COMPILER=intel plugins

# Remove unnecessary things
rm -rf trinityrnaseq.wiki
rm Makefile
back=$PWD
# clean up Chrysalis
cd Chrysalis
mv analysis/ReadsToComponents.pl .
find . -type f ! -executable | xargs -n 1 rm
find . -mindepth 1 -maxdepth 1 -type d | xargs -n 1 rm -rf
# clean up plugins
cd $back/trinity-plugins && rm Makefile
cd $back/trinity-plugins/slclust
rm -rf Makefile* README src
cd $back/trinity-plugins/collectl
rm build_collectl.sh collectl-3.6.9.src.tar.gz collectl-3.7.4.src.tar.gz
cd $back/trinity-plugins/GAL_0.2.1
rm README
# clean up Inchworm
cd $back/Inchworm
rm -rf src config* aclocal.m4 depcomp install-sh Make* missing notes stamp-h1
cd $back

# prefix with install_dir
# install destdir to rpm_build_root

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
Insert help
The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution

Trinity and all utility scripts are automaticially added to your path.

Documentation can be found online at %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: ")
whatis("URL: %{url}")
whatis("Description: ")

prepend_path("PATH",              "%{INSTALL_DIR}")
prepend_path("PATH",              "%{INSTALL_DIR}/util")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")

prereq("perl","bowtie/1.1.2","samtools/1.3")
EOF
## Module File End
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
