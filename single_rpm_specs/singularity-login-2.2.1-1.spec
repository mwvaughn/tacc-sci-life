%define		PNAME	singularity
Version:	2.2.1
Release:	1
License:	BSD-3-Clause-LBNL
URL:		http://singularity.lbl.gov
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Summary: 	Application and environment virtualization

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

#%define MODULE_VAR      %{MODULE_VAR_PREFIX}LZ4
# This was changed to automatically reflect PNAME
%define MODULE_VAR      %{MODULE_VAR_PREFIX}SINGULARITY

## PACKAGE DESCRIPTION
%description
Singularity provides functionality to build the smallest most minimal
possible containers, and running those containers as single application
environments.

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

#--------------------------------------
# Make the warning binary
cat << 'EOF' > $RPM_BUILD_ROOT/%{INSTALL_DIR}/singularity 
#!/bin/bash
#
# This is a dummy Singularity executable for the stampede login nodes. It
# prints usage information, and directs users to idev / a github tutorial.
#
echo "
================================================================================

 Please do not run Singularity on the %{PLATFORM} login nodes! Instead, submit 
 Singularity job scripts to the queue with 'sbatch'. If you would like to run
 Singularity interactively, please start an interactive session with 'idev'. A
 tutorial for using Singularity on %{PLATFORM} can be found here:

     https://github.com/TACC/TACC-Singularity

 The following Singularity modules are available on %{PLATFORM} compute nodes:

     %{PNAME}/%{version}

 For any additional help or support visit the Singularity website:

    http://singularity.lbl.gov/

================================================================================
"
exit 0
EOF
chmod a+rx $RPM_BUILD_ROOT/%{INSTALL_DIR}/singularity 

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
This Singularity module is a dummy module designed for the %{PLATFORM} login nodes.
Singularity is not installed and should not be run on the login nodes.

A functional Singularity module is available on the compute nodes. Submit
Singularity job scripts to the queue with 'sbatch'. If you would like to run
Singularity interactively, please start an interactive session with 'idev'. A
tutorial for using Singularity on %{PLATFORM} can be found here:

    https://github.com/TACC/TACC-Singularity

The following Singularity modules are available on %{PLATFORM} compute nodes:

    %{PNAME}/%{version}

For any additional help or support visit the Singularity website:

    http://singularity.lbl.gov/
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: applications, virtualization")
whatis("Keywords: virtualization, applications")
whatis("Description: Application and environment virtualization")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
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
