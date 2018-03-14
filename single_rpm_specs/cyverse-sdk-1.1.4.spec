%define		PNAME	cyverse-sdk
Version:	1.1.4
Release:	1
License:	BSD
URL:		https://github.com/iPlantCollaborativeOpenSource/cyverse-sdk
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	CyVerse provides full scriptable access to its underlying infrastructure via the Agave API

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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}CYVERSE

## PACKAGE DESCRIPTION
%description
CyVerse provides full scriptable access to its underlying infrastructure via the Agave API, which provides a comprehensive set of RESTful web services that make it easy for developers and users to:

 - Develop and run applications on HPC, Cloud, Condor, and container-based computing systems
 - Use MyProxy-based authentication for federated identity
 - Bring their own computing and storage resources into CyVerse
 - Share data and applications, even with people who aren't CyVerse users
 - Connect computing and data tasks via web-based events
 - Manage data on any cloud storage platform one has access to
 - Build sophisticated web-based applications that take advantage of all these underlying capabilities

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

[ -e %{PNAME} ] && rm -rf %{PNAME}
git clone %{url}.git
cd %{PNAME}
#git checkout 0e4d7f0fb2e5f8461d4a2f91affd7659eec13281
#git checkout 7e10ae38a9c2ac57e98e963ac1394257e555eb1c
git checkout b1b21200e8f78c37fd90a8f0142935c4f6721017

module purge
module load TACC python

tar -xzf cyverse-cli.tgz -C $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
 - %{MODULE_VAR}_BIN

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: cyverse, cli, sdk")
whatis("Keywords: development, cli, sdk")
whatis("Description: CyVerse provides full scriptable access to its underlying infrastructure via the Agave API")
whatis("URL: %{url}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "cyverse-cli/bin"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "cyverse-cli/bin"))

always_load("python")
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
