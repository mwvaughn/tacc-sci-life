%define PNAME java
Version: 1.8.77
Release: 1
Summary: Java runtime environment
License: oracle
Group: Applications/Life Sciences
Source: /work/03076/gzynda/rpmbuild/SPECS/../SOURCES/jre-8u77-linux-x64.tar.gz
URL: http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html
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
JAVA is a set of computer software and specifications developed by Sun Microsystems, later acquired by Oracle Corporation, that provides a system for developing application software and deploying it in a cross-platform computing environment.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n jre1.8.0_77

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

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
JAVA is a set of computer software and specifications developed by Sun Microsystems, later acquired by Oracle Corporation, that provides a system for developing application software and deploying it in a cross-platform computing environment.

The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution
	%{MODULE_VAR}_BIN - the location of the %{PNAME} binaries
	%{MODULE_VAR}_LIB - the location of the %{PNAME} libraries
	%{MODULE_VAR}_PLUGIN - the location of the %{PNAME} plugin files

Documentation can be found online at %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: ")
whatis("URL: %{url}")
whatis("Description: ")

prepend_path("PATH",			"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",		"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",			"%{INSTALL_DIR}/man")

setenv( "%{MODULE_VAR}_DIR",	"%{INSTALL_DIR}")
setenv( "JAVA_HOME",		"%{INSTALL_DIR}")
setenv( "%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv( "%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
setenv( "%{MODULE_VAR}_PLUGIN",	"%{INSTALL_DIR}/plugin")
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
