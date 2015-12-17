%define	PNAME	cd-hit
Version: 4.6.4
Release: 2
License: GPL
Group: Applications/Life Sciences
Source:  https://github.com/weizhongli/cdhit/releases/download/V4.6.4/cd-hit-4.6.4.tar.gz
Packager: TACC - gzynda@tacc.utexas.edu
Summary: Clustering DNA/protein sequence database at high identity with tolerance. 

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

%define MODULE_VAR	%{MODULE_VAR_PREFIX}CDHIT

## PACKAGE DESCRIPTION
%description
CD-HIT is a program for clustering DNA/protein sequence database at high identity with tolerance.

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
fi

## Make
make CC=icpc openmp=yes LDFLAGS="-Wl,-rpath=$ICC_LIB -o" PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR} CCFLAGS="-O3 -xAVX -axCORE-AVX2 -fopenmp"

## Install Steps End
#--------------------------------------
make PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR} install
#--------------------------------------
## Module File
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME} distribution. Documentation can be found online at http://weizhong-lab.ucsd.edu/cd-hit/ref.php

Version %{version}

]])

whatis("Name: CDHIT")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Proteomics, Clustering")
whatis("URL: https://github.com/weizhongli/cdhit")
whatis("Description: Clustering DNA/protein sequence database at high identity with tolerance.")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
prepend_path("PATH"       ,"%{INSTALL_DIR}")
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
