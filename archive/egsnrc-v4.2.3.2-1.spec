Summary:    egsnrc -- a package for the Monte Carlo simulation of coupled electron-photon transport. 
Name:       egsnrc
Version:    v4.2.3.2
Release:    1
License:    EGSnrc Code System License 
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME egsnrs

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
The EGSnrc system represents a derivative work based on the EGS4 system originally developed at the Stanford Linear Accelerator Centre (SLAC). The core system (all simulation subroutines, the PEGS4 data preprocessor, the Mortran3 preprocessor, material databases, multiple elastic scattering and spin data bases, and all other files and supporting material that do not have an explicit license statement) is therefore distributed according to an agreement between the National Research Council of Canada (NRC) and SLAC under the terms of the EGSnrc license.
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_EGSNRC

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
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

    
    
# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc 
# Load additional modules here (as needed)
module purge 
module load TACC


./install_egs << EOF


egs

f95
-fPIC
-O2
-g

gcc
-O -fPIC
x.conf
x
g++
0
no
no
EOF

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
This module makes available the openbabel executable. Documentation for %{name} is available online at the publisher\'s website: http://irs.inms.nrc.ca/software/egsnrc/egsnrc.html

Version %{version}
]])

whatis("Name: egsnrc")
whatis("Version: %{version}")
whatis("Category: computational chemistry, simulation")
whatis("Keywords:  Chemistry, Monte Carlo, Electron-proton Transport")
whatis("Description: egsnrc - a package for the Monte Carlo simulation of coupled electron-photon transport.") 
whatis("URL: http://irs.inms.nrc.ca/software/egsnrc/egsnrc.html")

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

