#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME bowtie
Version:      1.2.0
Release:      1
License:      GPL
Group:        Applications/Life Sciences
Source:       https://sourceforge.net/projects/bowtie-bio/files/bowtie/1.2.0/bowtie-1.2-source.zip
Packager:     TACC - jfonner@tacc.utexas.edu
Summary:      Memory-efficient short read (NGS) aligner


## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}BOWTIE

## PACKAGE DESCRIPTION
%description
Bowtie is an ultrafast, memory-efficient short read aligner. It aligns short DNA sequences (reads) to the human genome at a rate of over 25 million 35-bp reads per hour. Bowtie indexes the genome with a Burrows-Wheeler index to keep its memory footprint small: typically about 2.2 GB for the human genome (2.9 GB for paired-end).

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n %{PNAME}-1.2

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#--------------------------------------
## Install Steps Start
module purge
module load TACC

sed -i 's/$(PTHREAD_LIB) -ltbb -ltbbmalloc_proxy/-ltbb -lstdc++ -lpthread/g' Makefile
TR=$TBBROOT
# Since LDFLAGS is not used in bowtie's compilation, we hijack EXTRA_FLAGS to carry the rpath payload
case "%{PLATFORM}" in
	ls5)
		TL=${TR}/lib/intel64/gcc4.4
		module load gcc/5.2.0
		EF="-I${TR}/include -L${TL} -march=sandybridge -mtune=haswell -Wl,-rpath,$GCC_LIB -Wl,-rpath,$TL"
		;;
	stampedeknl)
		make WITH_AFFINITY=1 CXXFLAGS="-mavx512f -mavx512cd -mavx512er -mavx512pf" EXTRA_FLAGS="-I${TBBROOT}/include -L${TBBROOT}/lib/intel64/gcc4.7 -Wl,-rpath,${TBBROOT}/lib/intel64/gcc4.7" prefix=%{INSTALL_DIR} -j2
		;;
	stampede)
		make WITH_AFFINITY=1 LIBRARY_PATH=${LD_LIBRARY_PATH} CXXFLAGS=-march=native EXTRA_FLAGS="-Wl,-rpath,${TBBROOT}/lib/intel64/gcc4.4" prefix=%{INSTALL_DIR} -j2
		;;
	hikari)
		make WITH_AFFINITY=1 LIBRARY_PATH=${LD_LIBRARY_PATH} CXXFLAGS=-march=native EXTRA_FLAGS="-Wl,-rpath,${TBBROOT}/lib/intel64/gcc4.4" prefix=%{INSTALL_DIR} -j2
		;;
	*)
		echo "Please handle %{PLATFORM}"; exit 1
		;;
esac
## Install Steps End
#--------------------------------------
make WITH_AFFINITY=1 EXTRA_FLAGS="${EF}" prefix=%{INSTALL_DIR} -j4
make DESTDIR=${RPM_BUILD_ROOT} prefix=%{INSTALL_DIR} install

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME}
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/

This module provides the bowtie, bowtie-build, and bowtie-inspect binaries + associated scripts.

Version %{version}
]])

whatis("Name: Bowtie")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: http://bowtie-bio.sourceforge.net/index.shtml")
whatis("Description: Ultrafast, memory-efficient short read aligner")

setenv("%{MODULE_VAR}_DIR",              "%{INSTALL_DIR}")
prepend_path("PATH",                     "%{INSTALL_DIR}/bin")

%if "%{PLATFORM}" == "stampede" 
always_load("perl")
%endif

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
## version file for %{name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

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

