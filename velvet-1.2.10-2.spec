#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

%define PNAME velvet
Summary: Velvet - Sequence assembler for very short reads
Version: 1.2.10
Release: 2
License: GPLv2
Group: Applications/Life Sciences
Source:  https://www.ebi.ac.uk/~zerbino/velvet/velvet_%{version}.tgz
Packager: TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}VELVET

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------

%description
Velvet is a de novo genomic assembler specially designed for short read sequencing technologies, such as Solexa or 454, developed by Daniel Zerbino and Ewan Birney at the European Bioinformatics Institute (EMBL-EBI), near Cambridge, in the United Kingdom.

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

# Unpack source
%setup -n %{PNAME}_%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------

%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start

module swap $TACC_FAMILY_COMPILER gcc
# CFLAGS='-march=sandybridge -mtune=haswell' CXXFLAGS='-march=sandybridge -mtune=haswell'
make 'CFLAGS=-openmp -m64 -march=sandybridge -mtune=haswell' 'MAXKMERLENGTH=64' 'LONGSEQUENCES=1' 'CATEGORIES=4' cleanobj zlib obj velveth velvetg

## Install Steps End
#------------------------------------------------

cp -R ./third-party ./tests ./velvetg ./velveth ./contrib ./data ./Columbus_manual.pdf ./Manual.pdf $RPM_BUILD_ROOT/%{INSTALL_DIR}


#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} built with gcc and makes available the Velvet assembler
Documentation is available online at http://www.ebi.ac.uk/~zerbino/velvet/
Velvet is configured as such: MAXKMERLENGTH=64 LONGSEQUENCES CATEGORIES=4 OPENMP

Version %{version}
]])

whatis("Name: velvet")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, Assembly")
whatis("Description: Velvet - Sequence assembler for very short reads")
whatis("URL: http://www.ebi.ac.uk/~zerbino/velvet/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

## VERSION FILE
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
#%files -n %{name}-%{comp_fam_ver}
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
