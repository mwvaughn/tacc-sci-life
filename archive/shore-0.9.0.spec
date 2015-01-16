# $Id$

Name: shore
Version: 0.9.0
Release: 1
License: GPL
Group: Applications/Life Sciences
Source:  shore-0.9.0.tar.gz
Packager: TACC - jcarson@tacc.utexas.edu
Summary: Mapping and analysis pipeline for short read (SHORE) data produced on the Illumina platform. 

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
%define MODULE_VAR TACC_SHORE
%define PNAME shore

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
SHORE, for Short Read, is a mapping and analysis pipeline for short read data produced on the Illumina platform. It allows the incorporation of different aligners, and its different modules support a range of experiments, such as resequencing, mapping of mutants, ChIP-seq analyses and several more.

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{PNAME}-%{version}

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

module load gsl
module load boost

./configure --prefix=%{INSTALL_DIR} --without-lzma LDFLAGS="$LDFLAGS -L$TACC_GSL_LIB -L$TACC_BOOST_LIB -Wl,-rpath,$TACC_BOOST_LIB " CPPFLAGS=" -I$TACC_GSL_INC -I$TACC_BOOST_INC "

make

make DESTDIR=$RPM_BUILD_ROOT install

# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_BIN, and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME}
distribution. Documentation can be found online at http://sourceforge.net/apps/mediawiki/shore/index.php

Version %{version}

]])

whatis("Name: SHORE")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: http://1001genomes.org/software/shore.html")
whatis("Description: Mapping and analysis pipeline for short read (SHORE) data produced on the Illumina platform. ")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_SCRIPTS","%{INSTALL_DIR}/scripts")
prepend_path("PATH"       ,"%{INSTALL_DIR}/bin")

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

