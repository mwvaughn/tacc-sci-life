#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME singularity
Version:  2.1
Release:  1
License:  BSD (modified)
Group:    Applications/Life Sciences
#Source:   singularity-2.1.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Open-source software container platform

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
#%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
#%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR %{MODULE_VAR_PREFIX}SINGULARITY

## PACKAGE DESCRIPTION
%description
Singularity containers are purpose built and can include a simple binary and library stack or a complicated work flow that includes both network and file system access (or anything in between). The Singularity container images are then completely portable to any binary compatible version of Linux with the only dependency being Singularity running on the target system.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
#%setup -n %{PNAME}-%{version}

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
# Make the warning binary
cat << 'EOF' > $RPM_BUILD_ROOT/%{INSTALL_DIR}/singularity 
#!/bin/bash
#
# This is a dummy Singularity executable for the stampede login nodes. It
# prints usage information, and directs users to idev / a github tutorial.
#
echo "
================================================================================

 Please do not run Singularity on the Stampede login nodes! Instead, submit 
 Singularity job scripts to the queue with 'sbatch'. If you would like to run
 Singularity interactively, please start an interactive session with 'idev'. A
 tutorial for using Singularity on Stampede can be found here:

     https://github.com/TACC/TACC-Singularity

 The following Singularity modules are available on Stampede compute nodes:

     singularity/2.1

 For any additional help or support visit the Singularity website:

    http://singularity.lbl.gov/

================================================================================
"
exit 0
EOF
chmod a+rx $RPM_BUILD_ROOT/%{INSTALL_DIR}/singularity 

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This Singularity module is a dummy module designed for the Stampede login nodes.
Singularity is not installed and should not be run on the login nodes.

A functional Singularity module is available on the compute nodes. Submit
Singularity job scripts to the queue with 'sbatch'. If you would like to run
Singularity interactively, please start an interactive session with 'idev'. A
tutorial for using Singularity on Stampede can be found here:

    https://github.com/TACC/TACC-Singularity

The following Singularity modules are available on %{PLATFORM} compute nodes:

    %{PNAME}/%{version}

For any additional help or support visit the Singularity website:

    http://singularity.lbl.gov/

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology")
whatis("Keywords: Computational Biology, container, image, docker")
whatis("Description: Singularity is an open-source software container platform.")
whatis("URL: http://singularity.lbl.gov/")

prepend_path("PATH",                 "%{INSTALL_DIR}")
setenv(      "%{MODULE_VAR}_DIR",    "%{INSTALL_DIR}")

EOF

## Modulefile End
#--------------------------------------

# Lua sytax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#--------------------------------------
## VERSION FILE
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
## VERSION FILE END
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
