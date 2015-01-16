Summary:    geant4 -- toolkit for the simulation of the passage of particles through matter
Name:       geant4
Version:    9.5.p01
Release:    1
License:    Geant4 Software License
Group: Applications/Life Sciences
Source:     %{name}.%{version}.tar.gz
Source1:    G4NDL.4.0.tar.gz
Source2:    G4ABLA.3.0.tar.gz
Source3:    G4EMLOW.6.23.tar.gz
Source4:    G4NDL.0.2.tar.gz
Source5:    G4PhotonEvaporation.2.2.tar.gz
Source6:    G4RadioactiveDecay.3.4.tar.gz
Source7:    G4NEUTRONXS.1.1.tar.gz
Source8:    G4PII.1.3.tar.gz
Source9:    RealSurface.1.0.tar.gz

Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}.%{version}-buildroot

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
%define PNAME geant4

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
Geant4 is a toolkit for simulating the passage of particles through matter. It includes a complete range of functionality including tracking, geometry, physics models and hits. The physics processes offered cover a comprehensive range, including electromagnetic, hadronic and optical processes, a large set of long-lived particles, materials and elements, over a wide energy range starting, in some cases, from  and extending in others to the TeV energy range. It has been designed and constructed to expose the physics models utilised, to handle complex geometries, and to enable its easy adaptation for optimal use in different sets of applications. The toolkit is the result of a worldwide collaboration of physicists and software engineers. It has been created exploiting software engineering and object-oriented technology and implemented in the C++ programming language. It has been used in applications in particle physics, nuclear physics, accelerator design, space engineering and medical physics.
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_GEANT4

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
%setup -n %{name}.%{version}
# The next command unpacks Source1
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source). 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -n %{name}.%{version} -T -D -a 1
%setup -n %{name}.%{version} -T -D -a 2
%setup -n %{name}.%{version} -T -D -a 3
%setup -n %{name}.%{version} -T -D -a 4
%setup -n %{name}.%{version} -T -D -a 5
%setup -n %{name}.%{version} -T -D -a 6
%setup -n %{name}.%{version} -T -D -a 7
%setup -n %{name}.%{version} -T -D -a 8
%setup -n %{name}.%{version} -T -D -a 9

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
module swap $TACC_FAMILY_COMPILER gcc
module load cmake

export MY_GEANT4_DIR=`pwd`
cd $MY_GEANT4_DIR

#make a directory for all the data folders, the whole directory will be moved to the install_dir 
mkdir data
mv G4ABLA3.0 G4EMLOW6.23 G4NDL0.2 G4NDL4.0 G4NEUTRONXS1.1 G4PII1.3 PhotonEvaporation2.2 RadioactiveDecay3.4 RealSurface1.0 data/
 
mkdir install
cd install
cmake -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} ..


make 
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install

cd $MY_GEANT4_DIR
cp -r data $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
This module makes available the geant4 executable. Documentation for %{name} is available online at the publisher\'s website: http://geant4.cern.ch//

Version %{version}
]])

whatis("Name: geant4")
whatis("Version: %{version}")
whatis("Category: computational biology, simulation")
whatis("Keywords:  Detector simulation, High energy, Nuclear Physics")
whatis("Description: geant4 - Toolkit for the simulation of the passage of particles through matter. ")
whatis("URL: http://geant4.cern.ch")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv ( "G4LEVELGAMMADATA",    "%{INSTALL_DIR}/data/PhotonEvaporation2.2")
setenv ( "G4RADIOACTIVEDATA",    "%{INSTALL_DIR}/data/RadioactiveDecay3.4")
setenv ( "G4LEDATA",    "%{INSTALL_DIR}/data/G4EMLOW6.23")
setenv ( "G4NEUTRONHPDATA",    "%{INSTALL_DIR}/data/G4NDL4.0")
setenv ( "G4ABLADATA",    "%{INSTALL_DIR}/data/G4ABLA3.0")
setenv ( "G4REALSURFACEDATA",    "%{INSTALL_DIR}/data/RealSurface1.0")
setenv ( "G4NEUTRONXSDATA",    "%{INSTALL_DIR}/data/G4NEUTRONXS1.1")
setenv ( "G4PIIDATA",    "%{INSTALL_DIR}/data/G4PII1.3")


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

