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

%if "%{PLATFORM}" == "ls5"
%define _SD /opt/apps/%{PNAME}/%{version}
%else
%define _SD /opt/%{PNAME}/%{version}
%endif

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
 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_INC
 - %{MODULE_VAR}_LEXE
 - %{MODULE_VAR}_ETC
 - %{MODULE_VAR}_EXAMPLES

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: applications, virtualization")
whatis("Keywords: virtualization, applications")
whatis("Description: Application and environment virtualization")
whatis("URL: %{url}")

prepend_path("PATH",		"%{_SD}/bin")
prepend_path("LD_LIBRARY_PATH",		"%{_SD}/lib64")
prepend_path("MANPATH",		"%{_SD}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{_SD}")
setenv("%{MODULE_VAR}_EXAMPLES",     "%{_SD}/share/%{PNAME}-%{version}/examples")
setenv("%{MODULE_VAR}_BIN",	"%{_SD}/bin")
setenv("%{MODULE_VAR}_ETC",	"%{_SD}/etc")
setenv("%{MODULE_VAR}_INC",	"%{_SD}/include")
setenv("%{MODULE_VAR}_LIB",	"%{_SD}/lib64")
setenv("%{MODULE_VAR}_LEXE",	"%{_SD}/libexec")
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
