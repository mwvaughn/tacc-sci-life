
%define PNAME mach
Summary:    Markov Chain based haplotyper
Version:    1.0.18
Release:    3
License:    Unknown
Group: Applications/Life Sciences/genetics
Source:     http://csg.sph.umich.edu/abecasis/mach/download/%{PNAME}.%{version}.source.tgz
Packager:   TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}MACH

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -c -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Original CFLAGS contained -static which was causing failure
# CFLAGS='-march=sandybridge -mtune=haswell' CXXFLAGS='-march=sandybridge -mtune=haswell'
make all 'CFLAGS=-O2 -march=sandybridge -mtune=haswell -I./libsrc -I./mach1 -D__ZLIB_AVAILABLE__  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE'

# May want to revisit placement of this, or alternative implementation
export DONT_STRIP=1

cp executables/mach1 executables/thunder $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
MACH 1.0 is a Markov Chain based haplotyper. It can resolve long haplotypes or infer
missing genotypes in samples of unrelated individuals. The current version is a pre-release.
Documentation for %{name} is available - http://www.sph.umich.edu/csg/abecasis/MACH
The executable can be found in %{MODULE_VAR}_DIR

This module provides the mach1 and thunder executables.

Version %{version}
]])

whatis("Name: MACH")
whatis("Version: %{version}")
whatis("Category: Computational biology, genetics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing, Genetics, GWAS, Imputation")
whatis("Description: Markov Chain based haplotyper")
whatis("URL: http://www.sph.umich.edu/csg/abecasis/MACH")

prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")

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

