# $Id$

## Cloned from https://github.com/ucdavis-bioinformatics/sickle.git and packaged as sickle.tgz

Summary: A windowed adaptive trimming tool for FASTQ files using quality
Name: sickle
Version: 1.2
Release: 2
License: Artistic
Group: Applications/Life Sciences
Source0:  sickle.tgz
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

%define PNAME %{name}

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_SICKLE

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Sickle is a tool that uses sliding windows along with quality and length thresholds to determine when quality is sufficiently low to trim the 3'-end of reads and also determines when the quality is sufficiently high enough to trim the 5'-end of reads. It will also discard reads based upon the length threshold.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/*
%setup -n %{name}

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

make

cp -R ./sickle ./sickle.xml $RPM_BUILD_ROOT/%{INSTALL_DIR}
 
# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME}
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/

Version %{version}
]])

whatis("Name: Sickle")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing")
whatis("URL: https://github.com/ucdavis-bioinformatics/sickle")
whatis("Description: A windowed adaptive trimming tool for FASTQ files using quality")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

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

