# $Id$

# You must build Velvet first, then Oases
# as it requires the build artifacts from velvet

Summary: Oases - De novo transcriptome assembler for very short reads
%define PNAME oases
Version: 0.2.08
Release: 4
License: GPLv2
Group: Applications/Life Sciences
Source:  https://www.ebi.ac.uk/~zerbino/oases/oases_%{version}.tgz
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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}OASES

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Oases is a de novo transcriptome assembler designed to produce transcripts from short read sequencing technologies, such as Illumina, SOLiD, or 454 in the absence of any genomic assembly. It was developed by Marcel Schulz (MPI for Molecular Genomics) and Daniel Zerbino (previously at the European Bioinformatics Institute (EMBL-EBI), now at UC Santa Cruz).

Oases uploads a preliminary assembly produced by Velvet, and clusters the contigs into small groups, called loci. It then exploits the paired-end read and long read information, when available, to construct transcript isoforms.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n oases_0.2.8

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

#--------------------------------------
## Install Steps Start
module swap $TACC_FAMILY_COMPILER gcc

#-----------------------------
# Build parallel version
#-----------------------------

make -k 'VELVET_DIR=%{_topdir}/BUILD/velvet_1.2.10/' 'CFLAGS=-openmp -m64 -march=sandybridge -mtune=haswell' 'MAXKMERLENGTH=64' 'LONGSEQUENCES=1' 'CATEGORIES=4'

cp -R ./oases ./data ./doc ./scripts ./OasesManual.pdf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with gcc and makes available the Oases meta-assembler
Documentation is available online at http://www.ebi.ac.uk/~zerbino/oases/
Velvet/Oases is configured as such: MAXKMERLENGTH=64 LONGSEQUENCES CATEGORIES=4 OPENMP
The oases executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: oases")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, Assembly")
whatis("Description: De novo transcriptome assembler for very short reads")
whatis("URL: http://www.ebi.ac.uk/~zerbino/oases/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

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

