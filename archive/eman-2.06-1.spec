##eman2
## this is the default version (intel?), there is also a gcc4 version
## need to compile mpi separately under the eman2 directory
Summary: Eman2 - EMAN2 is the successor to EMAN1 (EMAN).
Name:	eman
Version:  2.06	
Release:   1	
Group:	Applications/Life Sceinces
License:  GPL 
Source0: eman-linux-x86_64-2.06.tar.bz2 
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc

%include ../system-defines.inc
%define PNAME eman2

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
%define MODULE_VAR TACC_EMAN2

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n EMAN2

%build

%install

%include ../system-load.inc

module purge
module load TACC
module load python
export EMAN2DIR=`pwd`

cd mpi_eman
make -f Makefile.linux2 install

cd ..

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

cp -R ./bin ./doc ./include ./lib ./mpi_eman ./Python-2.7-ucs4 $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help ( 
[[
This module loads %{name}. This module makes available the %{name} executables. Documentation for %{name} is available online at the publisher\'s website: http://blake.bcm.edu/emanwiki/EMAN
These executables can be found in %{MODULE_VAR}_DIR, including refine.

Version %{version}
]])

whatis("Name: EMAN2")
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
setenv (     "EMAN2DIR",           "%{INSTALL_DIR}")
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
module unload python

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

