# $Id$

Name: muscle
Version: 3.8.31
Release: 2
License: GPL
Group: Applications/Life Sciences
Source:  muscle3.8.31_src.tar.gz
Packager: TACC - jcarson@tacc.utexas.edu
Summary: Memory-efficient short read (NGS) aligner

# http://www.drive5.com/muscle/downloads.htm

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%define debug_package %{nil}
%include ../rpm-dir.inc
#%include ../system-defines.inc
#%include ../system-load.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define APPS    /opt/apps
%define MODULES modulefiles
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_MUSCLE
%define PNAME muscle

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
MUSCLE is one of the best-performing multiple alignment programs according to published benchmark tests, with accuracy and speed that are consistently better than CLUSTALW. MUSCLE can align hundreds of sequences in seconds. Most users learn everything they need to know about MUSCLE in a few minutes—only a handful of command-line options are needed to perform common alignment tasks.

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{PNAME}%{version}/src

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
module swap intel gcc

sed -i s/-static// ./mk
make ENV_LINK_OPTS="-Wl,-rpath=$GCC_LIB"
cp -r ./* $RPM_BUILD_ROOT%{INSTALL_DIR} 

# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{name} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{name}
distribution. Documentation can be found online at http://www.drive5.com/muscle/

Version %{version}

]])

whatis("Name: MUSCLE")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: http://www.drive5.com/muscle/")
whatis("Description: Popular multiple alignment software")

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

