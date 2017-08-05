#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME singularity
Version:  2.1
Release:  1
License:  BSD (modified)
Group:    Applications/Life Sciences
Source:   singularity-2.1.tar.gz
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

#--------------------------------------
# Copy the binaries
ln -s /usr/bin/singularity $RPM_BUILD_ROOT/%{INSTALL_DIR}/singularity

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This Singularity module is a wrapper for the machine version of Singularity -
version 2.1 - located only on the compute nodes. Loading this module will keep
the machine version of Singularity in your path, and will prevent conflicts
with other versions. A tutorial for using Singularity on Stampede can be found
here:

    https://github.com/TACC/TACC-Singularity

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


# In SPECS dir:
# ./build_rpm.sh singularity-compute-2.1.spec
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

