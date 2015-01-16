# $Id$

Summary:    A low memory, computationally efficient implementation of the MaCH algorithm for genotype imputation
Name:       minimac
Version:    20121116
Release:    1
License:    Unknown
Group: Applications/Life Sciences/genetics
# Downloaded minimac-beta-2012.11.16.tgz
# Repackaged as minimac-20121116.tgz
## mkdir -p minimac-20121116
## mv minimac minimac-20121116/
## mv minimac-omp minimac-20121116/
## tar -czvf minimac-20121116.tgz minimac-20121116
Source:     %{name}-%{version}.tgz
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
#BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
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

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

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

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

#%setup -c -n %{name}-%{version}
%setup

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

# These are just binaries
cp minimac $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp minimac-omp $RPM_BUILD_ROOT/%{INSTALL_DIR}

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

