Summary:    Arachne
Name:       arachne
Version:    3.2
Release:    1
License:    Broad Institute
Vendor:     Broad Institute
Group: Applications/Life Sciences
Source:     arachne-3.2.tar.gz
Packager:   TACC - wonaya@tacc.utexas.edu
BuildRoot:  /scratch/02114/wonaya/tmp/%{name}-%{version}-buildroot

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
%define MODULE_VAR TACC_ARACHNE

%description
Arachne is a toolkit developed for Whole Genome Shotgun Assembly.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{PNAME}-%{version}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
module purge
module load TACC
#module unload $TACC_FAMILY_COMPILER
#module load gcc/4.7.1
module load python

./configure --prefix=$PWD
make

module unload python

cp -r bin $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
To startup this program, use go to %{MODULE_VAR}_DIR/bin/ in the command line to see all the available tools. 
Documentation for %{PNAME} is available online at the publisher website: http://www.broadinstitute.org/crd/wiki/index.php/Arachne
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include %{PNAME}.

Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics")
whatis("Description: Arachne - a toolkit developed for Whole Genome Shotgun Assembly")
whatis("URL: http://www.broadinstitute.org/crd/wiki/index.php/Arachne")

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

