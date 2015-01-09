Summary:    Rum
Name:       rum
Version:    2.0.5
Release:    1
License:    GPL
Vendor:     PCBI UPenn
Group: Applications/Life Sciences
Source:     rum-2.0.5.tar.gz
Packager:   TACC - wonaya@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_RUM

%description
RUM is an RNA-Seq alignment pipeline. 

## PREP
%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{PNAME}-%{version}
%build
%install
%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 70df240576caec52f0109c83e777cad8c319b73d
module load perl
module load python

perl Makefile.PL
module unload perl
module unload python
=======

perl Makefile.PL
>>>>>>> d6c1cb5b22b254f6ee31c6ffe8d7d3f5d30772bf
cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
This module loads %{PNAME}, which uses perl.
To startup this program, use '$TACC_RUM_DIR/bin/rum_runner' in the command line. 
Documentation for %{PNAME} is available online at the publisher website: https://github.com/itmat/rum/wiki
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include %{PNAME}.
Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Mapping")
whatis("Description: RUM - RNAseq Unified Mapper")
whatis("URL: http://cbil.upenn.edu/RUM/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/bin/")

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
<<<<<<< HEAD
<<<<<<< HEAD
rm -rf $RPM_BUILD_ROOT
=======
rm -rf $RPM_BUILD_ROOT
>>>>>>> d6c1cb5b22b254f6ee31c6ffe8d7d3f5d30772bf
=======
rm -rf $RPM_BUILD_ROOT
>>>>>>> 70df240576caec52f0109c83e777cad8c319b73d
