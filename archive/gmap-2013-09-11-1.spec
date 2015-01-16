##GMAP
#export RPM_BUILD_DIR=/home1/0000/build/rpms/
#export RPM_BUILD_DIR=/admin/build/admin/rpms/stampede/
Summary: GMAP: a genomic mapping and alignment program for mRNA and EST sequences 
Name:  gmap
Version:  20130911
Release:   1	
Group:	Applications/Life Sceinces
License:  Boost Software License
Source0:  %{name}-gsnap-2013-09-11.tar.gz	
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

Packager:   TACC - jiao@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc

%include ../system-defines.inc
%define PNAME gmap

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
%define MODULE_VAR TACC_GMAP

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-2013-09-11

%build

%install

%include ../system-load.inc

module purge
module load TACC
module load samtools

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

./configure --with-gmapdb=/tmp --prefix=%{INSTALL_DIR}
make

rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help ( 
[[
This module makes available the GSNAP and GMAP executables.
Documentation for %{name} is available online - http://research-pub.gene.com/gmap/
The executable can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: gmap")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Sequencing, Alignment")
whatis("Description: GMAP: a genomic mapping and alignment program for mRNA and EST sequences")
whatis("URL: http://research-pub.gene.com/gmap/")
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

