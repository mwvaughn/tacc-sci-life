%define		PNAME	concaterpillar
Version:	1.8a
Release:	1
License:	BSD
URL:		http://leigh.geek.nz/software.shtml
Source:		http://leigh.geek.nz/software/concaterpillar-1.8a.tbz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Summary:	This is a hierarchical likelihood-ratio test for phylogenetic congruence.

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
%define MODULE_VAR      %{MODULE_VAR_PREFIX}%(t=%{PNAME}; echo ${t^^})

## PACKAGE DESCRIPTION
%description
This is a hierarchical likelihood-ratio test for phylogenetic congruence.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
%setup -n %{PNAME}-%{version}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Purge environment and reload TACC defaults
module purge
module load TACC

sed -i "s/bin\/python/bin\/env python/" concaterpillar.py
sed -i "s/\/usr\/local\/bin\///" concaterpillar.py

cp * $RPM_BUILD_ROOT/%{INSTALL_DIR}/

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
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Application, Phylogenetics")
whatis("Description: This is a hierarchical likelihood-ratio test for phylogenetic congruence.")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")

always_load("python/2.7.12", "raxml/7.3.0")
prereq("python/2.7.12","raxml/7.3.0")

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
