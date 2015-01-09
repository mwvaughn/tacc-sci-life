# $Id$

Name: mrsfast
Version: 3.2.0
Release: 1
License: See http://mrsfast.sourceforge.net/mrsFASTUltraManual
Group: Applications/Life Sciences
Source:  http://sourceforge.net/projects/mrsfast/files/mrsfast-ultra-3.2.0/mrsfast-ultra-3.2.0.zip
Packager: TACC - jcarson@tacc.utexas.edu
Summary: micro-read substitution-only Fast Alignment Search Tool 



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
%define MODULE_VAR TACC_MRSFAST
%define PNAME mrsfast

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
mrsFAST is designed to map short reads to reference genome assemblies

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{PNAME}-ultra-%{version}

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

make 

# make install not supported
cp -r ./* $RPM_BUILD_ROOT%{INSTALL_DIR} 


# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME}
distribution. Documentation can be found online at http://mrsfast.sourceforge.net/mrsFASTUltraManual

Version %{version}

]])

whatis("Name: mrsFAST")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Proteomics, Mapping")
whatis("URL: http://mrsfast.sourceforge.net/Home")
whatis("Description: Fast, memory-efficient short read mapping to reference genome assemblies.")

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

