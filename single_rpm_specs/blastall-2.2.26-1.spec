%define		PNAME	blastall
Version:	2.2.26
Release:	1
License:	BSD
URL:		ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy/2.2.26/
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Summary:	Legacy NCBI BLAST sequence alignment package.

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
%define MODULE_VAR      %{MODULE_VAR_PREFIX}%(echo "%{PNAME}" | tr [:lower:] [:upper:])

## PACKAGE DESCRIPTION
%description
The Basic Local Alignment Search Tool (BLAST) is the most widely used sequence similarity tool. There are versions of BLAST that compare protein queries to protein databases, nucleotide queries to nucleotide databases, as well as versions that translate nucleotide queries or databases in all six frames and compare to protein databases or queries.

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

# Download tar
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy/2.2.26/blast-2.2.26-x64-linux.tar.gz
# Untar
tar -xzf blast-2.2.26-x64-linux.tar.gz

cp -r blast-2.2.26/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}

rm -rf blast-2.2.26*

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
 - %{MODULE_VAR}_DATA
 - %{MODULE_VAR}_DOC

for the location of the %{PNAME} distribution.

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment")
whatis("URL: http://www.ncbi.nlm.nih.gov/BLAST")
whatis("Description: Legacy NCBI BLAST sequence alignment package.")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_DATA",	"%{INSTALL_DIR}/data")
setenv("%{MODULE_VAR}_DOC",	"%{INSTALL_DIR}/doc")
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
