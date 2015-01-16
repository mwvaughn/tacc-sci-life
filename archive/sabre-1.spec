# $Id$

## Cloned from https://github.com/ucdavis-bioinformatics/sabre.git and packaged as sabre.tgz

Summary: A barcode demultiplexing and trimming tool for FastQ files
Name: sabre
Version: 1.00
Release: 1
License: Artistic
Group: Applications/Life Sciences
Source0:  sabre.tgz
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME sabre

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Sabre is a tool that will demultiplex barcoded reads into separate files. It will work on both single-end and paired-end data in fastq format. It simply compares the provided barcodes with each read and separates the read into its appropriate barcode file, after stripping the barcode from the read (and also stripping the quality values of the barcode bases). If a read does not have a recognized barcode, then it is put into the unknown file. Sabre also has an option (-m) to allow mismatches of the barcodes.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BOWTIE

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/*
%setup -n %{name}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC
module swap intel gcc

#-----------------------------
# Build parallel version
#-----------------------------

make

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install
cp -R ./sabre $RPM_BUILD_ROOT/%{INSTALL_DIR}
 
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

whatis("Name: Sabre")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing")
whatis("URL: https://github.com/ucdavis-bioinformatics/sabre")
whatis("Description: barcode demultiplexing and trimming tool for FastQ files")

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

