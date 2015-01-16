Summary:    Stampy
Name:       stampy
Version:    1.0.22
Release:    1
License:    GPL
Vendor:     Wellcome Trust Centre
Group: Applications/Life Sciences
Source:     stampy-1.0.22.tar.gz
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
%define MODULE_VAR TACC_STAMPY

%description
Stampy is a package for the mapping of short reads from illumina sequencing machines onto a reference genome. 

## PREP
%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{PNAME}-%{version}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
#module purge
#module load TACC
module load python
module unload $TACC_FAMILY_COMPILER
module load gcc

sed -i s/-Wl// makefile
make python=python2.7

<<<<<<< HEAD
module unload python
=======
>>>>>>> d6c1cb5b22b254f6ee31c6ffe8d7d3f5d30772bf
cp -r build ext makefile maptools.so plugins README.txt Stampy stampy.py $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
This module loads %{PNAME}, which uses python.
To startup this program, use 'python $TACC_STAMPY_DIR/stampy' in the command line. 
Documentation for %{PNAME} is available online at the publisher website: http://www.well.ox.ac.uk/~gerton/README.txt
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include %{PNAME}.

Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Mapping")
whatis("Description: Stampy - Illumina short reads mapper")
whatis("URL: http://www.well.ox.ac.uk/project-stampy")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

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

