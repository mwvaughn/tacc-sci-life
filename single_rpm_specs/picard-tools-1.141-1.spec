%define PNAME 	picard-tools
Version: 		1.141
Release: 		1
License: 		MIT License
Source: 		https://github.com/broadinstitute/picard/releases/download/1.141/picard-tools-1.141.zip
Packager: 		TACC - jcarson@tacc.utexas.edu
Group: 			Applications/Life Sciences
Summary: 		Picard Tools - Manipulate SAM files

## Picard tools is Java and is distributed compiled

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

%define MODULE_VAR	%{MODULE_VAR_PREFIX}PICARD

## PACKAGE DESCRIPTION
%description
#%description -n %{PNAME}-%{version}
Picard Tools comprises Java-based command-line utilities that manipulate SAM files, and a Java API (SAM-JDK) for creating new programs that read and write SAM files. Both SAM text format and SAM binary (BAM) format are supported.

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
	

## Install Steps End
#--------------------------------------
cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}


#--------------------------------------

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME} distribution.

Invoke as follows:

java jvm-args -jar $%{MODULE_VAR}_DIR/picard.jar PicardCommand [opts]

Version %{version}
]])

whatis("Name: Picard")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing")
whatis("Description: Picard comprises Java-based command-line utilities that manipulate SAM files, and a Java API (SAM-JDK) for creating new programs that read and write SAM files. Both SAM text format and SAM binary (BAM) format are supported.")
whatis("URL: https://github.com/broadinstitute/picard")

setenv("%{MODULE_VAR}_DIR",	"%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_SCRIPTS",	pathJoin("%{INSTALL_DIR}","scripts"))

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}","bin"))
prepend_path("MANPATH",		pathJoin("%{INSTALL_DIR}","man"))
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

