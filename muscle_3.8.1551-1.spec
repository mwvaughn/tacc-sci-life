#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME muscle
Version:      3.8.1551
Release:      1
License:      GPL
Group:        Applications/Life Sciences
Source:       http://www.drive5.com/muscle/muscle_src_3.8.1551.tar.gz
Packager:     TACC - bbeck@tacc.utexas.edu
Summary:      Fast multiple sequence alignment (MSA) software for amino acid or nucleotide sequences


## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

#%define MODULE_VAR  %{MODULE_VAR_PREFIX}MUSCLE
#%define MODULE_VAR  %{MODULE_VAR_PREFIX}%(echo %{PNAME} | awk '{print toupper($0)}')
%define PNAMEU %(echo %{PNAME} | awk '{print toupper($0)}')
%define MODULE_VAR  %{MODULE_VAR_PREFIX}%{PNAMEU}

## PACKAGE DESCRIPTION
%description
MUSCLE is a program for creating multiple alignments of amino acid or nucleotide sequences. A range of options is provided that give you the choice of optimizing accuracy, speed, or some compromise between the two.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep -n %{PNAME}-src-%{version}.tar.gz
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -c -n %{PNAME}-%{version}

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
## Install Steps Start
module swap $TACC_FAMILY_COMPILER gcc

# Since LDFLAGS is not used in muscle's compilation, we hijack LDLIBS to carry the rpath payload as we already have to remove "-static"
make LDLIBS="-lm -Wl,-rpath,$GCC_LIB"

## Install Steps End
#--------------------------------------

cp -R ./%{PNAME} $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{name}
distribution. Documentation can be found online at http://www.drive5.com/muscle/manual

This module provides the %{PNAME} binary and scripts

Version %{version}

]])

whatis("Name: %{PNAMEU}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics, proteomics")
whatis("Keywords: Biology, Genomics, Proteomics, Alignment")
whatis("URL: http://www.drive5.com/muscle")
whatis("Description: Fast multiple sequence alignment (MSA) software for amino acid or nucleotide sequences")

setenv("%{MODULE_VAR}_DIR",              "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_SCRIPTS", pathJoin("%{INSTALL_DIR}","scripts"))
prepend_path("PATH",                     "%{INSTALL_DIR}")

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
## version file for %{name}-%{version}
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

