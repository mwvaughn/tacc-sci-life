##Ninja
#export RPM_BUILD_DIR=/home1/0000/build/rpms/
#export RPM_BUILD_DIR=/admin/build/admin/rpms/stampede/
Summary: Ninja - a software for  large-scale neighbor-joining phylogeny inference
Name:  ninja
Version:  1.2.2
Release:   1	
Group:	Applications/Life Sceinces
License:  LGPL 
Source0:  %{name}_%{version}.tar.gz	
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

Packager:   TACC - jiao@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc

%include ../system-defines.inc
%define PNAME ninja

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
NINJA is software for large-scale neighbor-joining phylogeny inference. It expects inputs to be either alignments (in fasta format) or pairwise distance matrices (in phylip format), and can produce both a distance matrix (phylip) and a tree file (newick format).
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_NINJA

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm   -rf $RPM_BUILD_ROOT

%setup -n %{name}_%{version} 

%build

%install

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

cp ./00README ./ninja ./Ninja.jar $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help ( 
[[
This module loads %{name}. This module makes available the %{name} executables. Documentation for %{name} is available online at the publisher\'s website: http://nimbletwist.com/software/ninja/docs.html

Version %{version}
]])

whatis("Name: ninja")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Sequencing, Phylogeny")
whatis("Description: Ninja - a software for  large-scale neighbor-joining phylogeny inference")
whatis("URL: http://nimbletwist.com/software/ninja/index.html")
prepend_path("PATH",    "%{INSTALL_DIR}")
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

