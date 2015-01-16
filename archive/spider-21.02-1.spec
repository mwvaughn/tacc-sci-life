##SPIDER
Summary: SPIDER - System for Processing Image Data from Electron microscopy and Related fields is an image processing system for electron microscopy. 
Name:	spider
Version:  21.02	
Release:   1	
Group:	Applications/Life Sceinces
License:  GPL 
Source0: http://www.wadsworth.org/spider_doc/spider/download/spiderweb.21.02.tar.gz 
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc

%include ../system-defines.inc
%define PNAME spider

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
FastQC is an application which takes a FastQ file and runs a series
of tests on it to generate a comprehensive QC report.  This will
tell you if there is anything unusual about your sequence.  Each
test is flagged as a pass, warning or fail depending on how far it
departs from what you'd expect from a normal large dataset with no
significant biases.  It's important to stress that warnings or even
failures do not necessarily mean that there is a problem with your
data, only that it is unusual.  It is possible that the biological
nature of your sample means that you would expect this particular
bias in your results.
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_SPIDER

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#setup -c unpack multiple folders in to one folder
%setup -c spiderweb

%build

%install

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

#ln -s ./spider/bin/spider_linux_mp_intel64 ./spider/bin/spider

cp -R ./spider/bin ./spider/docs ./spider/fftw ./spider/man ./spider/proc ./spider/spire $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help ( 
[[
This module loads %{name}. This module makes available the %{name} executables. Documentation for %{name} is available online at the publisher\'s website: http://www.wadsworth.org/spider_doc/spider/docs/documents.html
The executable works on this machine is spider_linux_mp_intel64
Version %{version}
]])

whatis("Name: spider")
whatis("Version: %{version}")
whatis("Category: computational biology, Electron Microscopy")
whatis("Keywords:  Biology, Cryo-EM, Image Processing ")
whatis("Description: spider - an image processing system for electron microscopy")
whatis("URL: http://www.wadsworth.org/spider_doc/spider/docs/spider.html")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "SPIDER_DIR",        "%{INSTALL_DIR}")
setenv (     "SPBIN_DIR",         "%{INSTALL_DIR}/bin")
setenv (     "SPMAN_DIR",         "%{INSTALL_DIR}/man")
setenv (     "SPPROC_DIR",        "%{INSTALL_DIR}/proc")
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

