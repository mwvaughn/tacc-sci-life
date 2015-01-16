# $Id$

Summary:    A low memory, computationally efficient implementation of the MaCH algorithm for genotype imputation
Name:       minimac
Version:    20130717
Release:    1
License:    Copyright 2009, Regents of the University of Michigan
Group: Applications/Life Sciences/genetics
# Unpackages to
# minimac.src
# ├── libStatGen
# └── minimac
Source:     http://www.sph.umich.edu/csg/cfuchsb/minimac.src.tgz
Packager:   TACC - vaughn@tacc.utexas.edu

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

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BWA

%define MODULE_VAR TACC_MINIMAC

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description

# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n minimac.src

##
## BUILD
##

%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

%include ../system-load.inc
# %include compiler-load.inc
# %include mpi-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

cd minimac
make all

cp bin/minimac $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp bin/minimac-omp $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
minimac is a low memory, computationally efficient implementation of the MaCH algorithm for genotype imputation. It is designed to work on phased genotypes and can handle very large reference panels with hundreds or thousands of haplotypes. The current version is a pre-release.
Documentation for %{name} is available - http://genome.sph.umich.edu/wiki/Minimac
The executable can be found in %{MODULE_VAR}_DIR

This module provides the mach1 and thunder executables.

Version %{version}
]])

whatis("Name: minimac")
whatis("Version: %{version}")
whatis("Category: Computational biology, genetics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing, Genetics, GWAS, Imputation")
whatis("Description: Low-memory Markov Chain-based haplotyper")
whatis("URL: http://genome.sph.umich.edu/wiki/Minimac")

prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")

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

