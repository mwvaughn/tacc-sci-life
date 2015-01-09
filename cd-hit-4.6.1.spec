# $Id$

Name: cd-hit
Version: 4.6.1
Release: 1
License: GPL
Group: Applications/Life Sciences
Source:  https://cdhit.googlecode.com/files/cd-hit-v4.6.1-2012-08-27.tgz
Packager: TACC - jcarson@tacc.utexas.edu
Summary: Clustering DNA/protein sequence database at high identity with tolerance. 

# Original sources was named cd-hit-v4.6.1-2012-08-27.tgz
# Updated Makefile to support DESTDIR.  Re-tarred source.

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include ../system-defines.inc
%include rpm-dir.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_CDHIT
%define PNAME cd-hit

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
CD-HIT is a program for clustering DNA/protein sequence database at high identity with tolerance.

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{PNAME}-v%{version}-2012-08-27

##
## BUILD
##

%build

##
## INSTALL
##
%install

%include ../system-load.inc

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load TACC

make PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR} openmp=yes 
make PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR} install
make clean

# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME}
distribution. Documentation can be found online at http://weizhong-lab.ucsd.edu/cd-hit/ref.php

Version %{version}

]])

whatis("Name: CD-HIT")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Proteomics, Clustering")
whatis("URL: https://code.google.com/p/cdhit/")
whatis("Description: Clustering DNA/protein sequence database at high identity with tolerance.")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_SCRIPTS","%{INSTALL_DIR}/scripts")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

EOF

#--------------
#  Version file.
#--------------

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
#%files -n %{name}-%{comp_fam_ver}
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

