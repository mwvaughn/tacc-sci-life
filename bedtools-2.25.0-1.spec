Name: bedtools
Version: 2.25.0
Release: 1
License: GPL
Source: https://github.com/arq5x/bedtools2/releases/download/v2.25.0/bedtools2-2.25.0.tar.gz
Packager: TACC - gzynda@tacc.utexas.edu
Summary: A flexible suite of utilities for comparing genomic features

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}BEDTOOLS
%define PNAME       bedtools

%package %{PACKAGE}
Summary: A flexible suite of utilities for comparing genomic features
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: A flexible suite of utilities for comparing genomic features
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
The bedtools utilities are a swiss-army knife of tools for a wide-range of genomics analysis tasks. The most widely-used tools enable genome arithmetic: that is, set theory on the genome. For example, bedtools allows one to intersect, merge, count, complement, and shuffle genomic intervals from multiple files in widely-used genomic file formats such as BAM, BED, GFF/GTF, VCF.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif

## SETUP
%setup -n %{PNAME}2-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

#--------------------------------------
%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    ########### Do Not Remove #############

#--------------------------------------
## Install Steps Start
module purge
module load TACC

## Patch Makefile
patch Makefile -li - <<EOF
19c19                         
< export CXX            = g++
---
> export CXX            = icpc
EOF

## Make
make -j 16

## Install Steps End
#--------------------------------------
cp -R bin docs scripts tutorial README.md RELEASE_HISTORY LICENSE $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif
#--------------------------------------

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
%if %{?BUILD_MODULEFILE}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
    ########### Do Not Remove #############

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{name}
distribution. Documentation can be found online at http://bedtools.readthedocs.org/en/latest/

bedtools + scripts

Version %{version}

]])

whatis("Name: Bedtools")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Utility, Interval, Sequencing")
whatis("Description: bedtools: a flexible suite of utilities for comparing genomic features")
whatis("URL: https://github.com/arq5x/bedtools2")

setenv("%{MODULE_VAR}_DIR",	%{INSTALL_DIR})
setenv("%{MODULE_VAR}_SCRIPTS",	pathJoin(%{INSTALL_DIR},"scripts"))

prepend_path("PATH",		pathJoin(%{INSTALL_DIR},"bin"))

#prereq("perl")

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

%endif
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
%defattr(-,root,install,)
%{INSTALL_DIR}
%endif # ?BUILD_PACKAGE

%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE}
%defattr(-,root,install,)
%{MODULE_DIR}
%endif # ?BUILD_MODULEFILE

## POST 
%post %{PACKAGE}
export PACKAGE_POST=1
%include include/post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include include/post-defines.inc

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

