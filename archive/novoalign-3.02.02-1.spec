# $Id$

Name:       novoalign
Version: 	3.02.02
Release: 	1
License:    http://www.novocraft.com/main/page.php?id=968
Group: 		Applications/Life Sciences
Source:  	novocraftV3.02.02.Linux2.6.tar.gz
Packager: 	TACC - jcarson@tacc.utexas.edu
Summary: 	novoalign - Aligner for short nucleotide space reads.

#http://www.novocraft.com/main/download.php?filename=V3.02.02/

# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%define debug_package %{nil}
%include ../rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME novoalign
%define MODULE_VAR TACC_NOVOALIGN

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}


#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Novoalign is an aligner for single-ended and paired-end reads from the Illumina Genome Analyser. Novoalign finds global optimum alignments using full Needleman-Wunsch algorithm with affine gap penalties.

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep 

# Remove older attempts
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack tarball
# This will unpack the source to /tmp/BUILD/***
%setup -n novocraft

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include ../system-load.inc

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC

# Novoalign documentation claims to need the following, not sure if true
# module load bedtools
# module load samtools
# module load jdk64       ## running into issues loading this during rpmbuild
# module load picard
# module load gatk

# Source is not available. Using the binaries

cp -r ./* $RPM_BUILD_ROOT%{INSTALL_DIR} 

#------------------------------------------------
# MODULE SECTION
#------------------------------------------------

# I keep both TACC_CUFFLINKS_DIR and TACC_CUFFLINKS_BIN for backward compatibility

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads the %{PNAME} software package.
Documentation for %{PNAME} is available online at the publisher website: http://www.novocraft.com/main/page.php?s=doc_novoalign
The cufflinks executable can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment")
whatis("Description: novoalign - Aligner for short nucleotide space reads.")
whatis("URL: http://www.novocraft.com/main/index.php")

prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}")

EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.02.02#################################################
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

