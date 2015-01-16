# $Id$

# You must build Velvet first, then Oases 
# as it requires the build artifacts from velvet (lame, I know)

Summary: Oases - De novo transcriptome assembler for very short reads
Name: oases
Version: 0.2.08
Release: 3
License: GPLv2
Group: Applications/Life Sciences
Source0:  oases_%{version}.tgz
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME oases
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_OASES

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Oases is a de novo transcriptome assembler designed to produce transcripts from short read sequencing technologies, such as Illumina, SOLiD, or 454 in the absence of any genomic assembly. It was developed by Marcel Schulz (MPI for Molecular Genomics) and Daniel Zerbino (previously at the European Bioinformatics Institute (EMBL-EBI), now at UC Santa Cruz).

Oases uploads a preliminary assembly produced by Velvet, and clusters the contigs into small groups, called loci. It then exploits the paired-end read and long read information, when available, to construct transcript isoforms.

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}_%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC
#module load gcc/4.4.5

#-----------------------------
# Build parallel version
#-----------------------------

make 'VELVET_DIR=%{_topdir}/BUILD/velvet_1.2.08/' 'CFLAGS=-openmp -m64' 'MAXKMERLENGTH=64' 'LONGSEQUENCES=1' 'CATEGORIES=4'

cp -R ./oases ./data ./doc ./scripts ./OasesManual.pdf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
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

#--------------
#  Version file.
#--------------

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

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

