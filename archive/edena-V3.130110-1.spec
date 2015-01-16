##EDENA
#export RPM_BUILD_DIR=/home1/0000/build/rpms/
#export RPM_BUILD_DIR=/admin/build/admin/rpms/stampede/
Summary: Edena - de novo short reads assembler
Name:  edena
Version:  V3.130110
Release:   1	
Group:	Applications/Life Sceinces
License:  GPLv3 
Source0:  Edena%{version}.tar.gz	
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

Packager:   TACC - jiao@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc

%include ../system-defines.inc
%define PNAME edena

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_EDENA

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm   -rf $RPM_BUILD_ROOT

%setup -n EdenaV3.130110 

%build

%install

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

make
cp -R ./bin COPYING referenceManual.pdf $RPM_BUILD_ROOT/%{INSTALL_DIR} 


rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help ( 
[[
This module makes available the edena executable.
Documentation for %{name} is available online - http://www.genomic.ch/edena.php 
The executable can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: gmap")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Sequencing, Alignment")
whatis("Description: de novo short reads assembler")
whatis("URL: http://www.genomic.ch/edena.php")
prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

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

