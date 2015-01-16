##eman
##Does not work with module python (2.7) on Stampede, works with system python (2.6)
Summary: Eman - Software for Single Particle Analysis and Electron Micrograph Analysis 
Name:	eman
Version:  1.9	
Release:   1	
Group:	Applications/Life Sceinces
License:  GPL 
Source0: eman-linux-x86_64-cluster-1.9.tar.gz 
BuildRoot: /var/tmp/%{name}-%{version}-buildroot
Packager:   TACC - jiao@tacc.utexas.edu
#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc

%include ../system-defines.inc
%define PNAME eman

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
EMAN is a suite of scientific image processing tools aimed primarily at the transmission electron microscopy community, though it is beginning to be used in other fields as well. EMAN has a particular focus on performing a task known as single particle reconstruction. In this method, images of nanoscale molecules and molecular assemblies embedded in vitreous (glassy) ice are collected on a transmission electron microscope, then processed using EMAN to produce a complete 3-D recosntruction at resolutions now approaching atomic resolution.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_EMAN

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n EMAN

%build

%install

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

#which direcotires are needed for precompiled version, chimeraext, python?
#Syntax error, chimeraext/FilterKit/Filter.py

cp -R ./bin ./doc ./chimeraext ./include ./lib ./python ./README $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help ( 
[[
This module loads %{name}. This module makes available the %{name} executables. Documentation for %{name} is available online at the publisher\'s website: http://blake.bcm.edu/emanwiki/EMAN
These executables can be found in %{MODULE_VAR}_DIR, including refine.

Version %{version}
]])

whatis("Name: EMAN")
whatis("Version: %{version}")
whatis("Category: computational biology, Electron Microscopy")
whatis("Keywords:  Biology, Cryo-EM, Image Processing, Reconstruction")
whatis("Description: eman - Software for Single Particle Analysis and Electron Micrograph Analysis")
whatis("URL: http://blake.bcm.edu/emanwiki/EMAN")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",   "%{INSTALL_DIR}/lib")
prepend_path("PYTHONPATH",        "%{INSTALL_DIR}/lib")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "EMANDIR",           "%{INSTALL_DIR}")
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

