Summary:    openbabel -- chemical toolbox designed to speak the many languages of chemical data.
Name:       openbabel
Version:    2.3.1
Release:    1
License:    GNU General Public License
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
#BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
 %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME openbabel

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------

%package -n %{name}-%{comp_fam_ver}
Summary: openbabel
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}
Open Babel is a chemical toolbox designed to speak the many languages of chemical data. It's an open, collaborative project allowing anyone to search, convert, analyze, or store data from molecular modeling, chemistry, solid-state materials, biochemistry, or related areas.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR TACC_OPENBABEL

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build   
          
# Start with a clean environment
#if [ -f "$BASH_ENV" ]; then
#   . $BASH_ENV
#   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
#fi
    
    
# Load correct compiler
%include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc 
# Load additional modules here (as needed)
#module purge 
#module load TACC
#module swap $TACC_FAMILY_COMPILER gcc
module load cmake

export MY_OPENBABAL_DIR=`pwd`
cd $MY_OPENBABAL_DIR
#echo $PWD
mkdir install
cd install
cmake .. -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR}


make -j 2
make DESTDIR=$RPM_BUILD_ROOT install 

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with cmake.
This module makes available the openbabel executable. Documentation for %{name} is available online at the publisher\'s website: http://openbabel.org/wiki/Main_Page/

Version %{version}
]])

whatis("Name: openbabel")
whatis("Version: %{version}")
whatis("Category: computational chemistry, simulation")
whatis("Keywords:  Chemistry, Molecular modeling, Format conversion")
whatis("Description: openbabal - chemical toolbox designed to speak the many languages of chemical data ")
whatis("URL: http://openbabel.org/wiki/Main_Page")

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
%files -n %{name}-%{comp_fam_ver}

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

