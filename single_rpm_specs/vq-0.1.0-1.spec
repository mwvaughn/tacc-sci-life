%define PNAME vq
Version: 0.1.0
Release: 1
Summary: vQ - the virtual scheduler
License: BSD
Source: %{PNAME}-%{version}.tar.gz
Group: Applications
URL: https://github.com/zyndagj/vQ
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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}JAVA

## PACKAGE DESCRIPTION
%description
A virtual job scheduler for use in a cluster environment.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT

## SETUP
#%setup -n 

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

[ -d vQ ] && rm -rf vQ
git clone git@github.com:zyndagj/vQ.git
cd vQ
chmod +x vQ.py

mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp vQ.py $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -r test_programs $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
A virtual job scheduler for use in a cluster environment.

The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution
	%{MODULE_VAR}_BIN - the location of the %{PNAME} binaries
	%{MODULE_VAR}_TEST - the location of the %{PNAME} test programs

Documentation can be found online at %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: hpc, distributed, scheduler")
whatis("Keywords: hpc, slurm, sge, scheduler, falcon, canu")
whatis("URL: %{url}")
whatis("Description: ")

prepend_path("PATH",			"%{INSTALL_DIR}/bin")

setenv( "%{MODULE_VAR}_DIR",	"%{INSTALL_DIR}")
setenv( "%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv( "%{MODULE_VAR}_TEST",	"%{INSTALL_DIR}/test_programs")

prereq("python")
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
