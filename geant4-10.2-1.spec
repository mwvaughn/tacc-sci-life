#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME geant4
Version:  10.2
Release:  1
License:  Geant4 Software License
Group:    Applications/Life Sciences
Source0:  http://geant4.cern.ch/support/source/geant4.10.02.tar.gz
Source1:  http://geant4.cern.ch/support/source/G4NDL.4.5.tar.gz
Source2:  http://geant4.cern.ch/support/source/G4EMLOW.6.48.tar.gz
Source3:  http://geant4.cern.ch/support/source/G4PhotonEvaporation.3.2.tar.gz
Source4:  http://geant4.cern.ch/support/source/G4RadioactiveDecay.4.3.tar.gz
Source5:  http://geant4.cern.ch/support/source/G4SAIDDATA.1.1.tar.gz
Source6:  http://geant4.cern.ch/support/source/G4NEUTRONXS.1.4.tar.gz
Source7:  http://geant4.cern.ch/support/source/G4ABLA.3.0.tar.gz
Source8:  http://geant4.cern.ch/support/source/G4PII.1.3.tar.gz
Source9:  http://geant4.cern.ch/support/source/RealSurface.1.0.tar.gz
Source10: http://geant4.cern.ch/support/source/G4ENSDFSTATE.1.0.tar.gz
Source11: http://geant4.cern.ch/support/source/G4TENDL.1.0.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  A toolkit for the simulation of the passage of particles through matter.

### NOTE: Source0 is the main distribution called in this spec file. The other 
### 11 source files (Source1-Source11) are about 3.2 GB when unpacked. So to 
### save some space, we already unpacked them here:
###               /scratch/projects/tacc/bio/geant4/10.2/

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}GEANT4

# define the data dirs and make sure they exist
%if "%{PLATFORM}" == "ls5"
    %define GEANT4DATA  %{INSTALL_DIR}/share/Geant4-10.2.0/data
%endif

# NOTE: this build will fail on stampede because cmake >3.3 is required!
%if "%{PLATFORM}" == "stampede"
    %define GEANT4DATA  /scratch/projects/tacc/bio/%{PNAME}/%{version}
%endif

#%if [ ! -d "%{GEANT4DATA}" ]; then
#    echo "The data directory %{GEANT4DATA} was not found. Aborting rpmbuild."
#    exit 1
#%endif

## PACKAGE DESCRIPTION
%description
Geant4 is a toolkit for the simulation of the passage of particles through matter. Its areas of application include high energy, nuclear and accelerator physics, as well as studies in medical and space science. The two main reference papers for Geant4 are published in Nuclear Instruments and Methods in Physics Research A 506 (2003) 250-303, and IEEE Transactions on Nuclear Science 53 No. 1 (2006) 270-278.

## PREP
%prep 
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%setup -n %{PNAME}.10.02

## BUILD
%build

#------------------------------------------------
# INSTALL 
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#--------------------------------------
## Install Steps Start
module purge
module load TACC

%if "%{PLATFORM}" == "ls5"
    module swap $TACC_FAMILY_COMPILER gcc/4.9.3
    module load cmake/3.4.1
    export CFLAGS="-O3 -march=sandybridge -mtune=haswell"
    export LDFLAGS="-march=sandybridge -mtune=haswell"
%endif

# NOTE: this build will fail on stampede because cmake >3.3 is required!
%if "%{PLATFORM}" == "stampede"
    module swap $TACC_FAMILY_COMPILER gcc/4.9.1
    module load cmake/3.1.0
%endif

export CC=`which gcc`
export CXX=`which g++`

# The objective of this section is to install the compiled software into a virtual
# directory structure so that it can be packaged up into an RPM
#
# install is also a macro that does many things, including creating appropriate
# directories in $RPM_BUILD_ROOT and cd to the right place

# Install serial version
cd $RPM_BUILD_DIR
rm -rf %{PNAME}-%{version}-cmake
rm -rf %{PNAME}-%{version}

mv %{PNAME}.10.02 %{PNAME}-%{version}-cmake
mkdir %{PNAME}.10.02 # the clean script will complain if this is not here
mkdir %{PNAME}-%{version}/
mkdir %{PNAME}-%{version}-cmake/build/
cd %{PNAME}-%{version}-cmake/build/

%if "%{PLATFORM}" == "ls5"
cmake -DGEANT4_INSTALL_DATA=ON -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_DIR/%{PNAME}-%{version} -DGEANT4_BUILD_MULTITHREADED=ON ../
%endif

%if "%{PLATFORM}" == "stampede"
cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_DIR/%{PNAME}-%{version} -DGEANT4_BUILD_MULTITHREADED=ON -DGEANT4_INSTALL_DATADIR=%{GEANT4DATA} ../
%endif

make -j 4
make install

# Copy the relevant files
cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/bin/     $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/include/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/lib64/   $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/share/   $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
# Clean up the old module directory
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This module loads %{PNAME} version %{version} built with gcc and cmake.
Documentation for %{name} is available online at: http://geant4.web.cern.ch/geant4/

The binary executables can be found in %{MODULE_VAR}_BIN
The include files can be found in %{MODULE_VAR}_INCLUDE
The library files can be found in %{MODULE_VAR}_LIB
The share files can be found in %{MODULE_VAR}_SHARE

Normally when using Geant4, the scripts geant4.sh and geant4make.sh must be sourced.
This module file takes care of that.

When compiling code with this version of Geant4, do:

"cmake -DGEANT4_DIR=$TACC_GEANT4_DIR/lib64/Geant4-10.2.0  /path/to/code/"

Where "/path/to/code/" is replaced with the location of your Geant4 code.

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, simulation")
whatis("Keywords: Biology, Detector simulation, High energy, Nuclear physics")
whatis("Description: Geant4 is a toolkit for the simulation of the passage of particles through matter.")
whatis("URL: http://geant4.web.cern.ch/geant4/")

prepend_path("PATH",                  "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN",     "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_INCLUDE", "%{INSTALL_DIR}/include")
setenv (     "%{MODULE_VAR}_LIB",     "%{INSTALL_DIR}/lib64")
setenv (     "%{MODULE_VAR}_SHARE",   "%{INSTALL_DIR}/share")

setenv ( "%{MODULE_VAR}_G4ABLA", "%{GEANT4DATA}/G4ABLA3.0")
setenv ( "%{MODULE_VAR}_G4EMLOW", "%{GEANT4DATA}/G4EMLOW6.48")
setenv ( "%{MODULE_VAR}_G4ENSDFSTATE", "%{GEANT4DATA}/G4ENSDFSTATE1.2")
setenv ( "%{MODULE_VAR}_G4NDL", "%{GEANT4DATA}/G4NDL4.5")
setenv ( "%{MODULE_VAR}_G4NEUTRONXS", "%{GEANT4DATA}/G4NEUTRONXS1.4")
setenv ( "%{MODULE_VAR}_G4PII", "%{GEANT4DATA}/G4PII1.3")
setenv ( "%{MODULE_VAR}_G4SAIDDATA", "%{GEANT4DATA}/G4SAIDDATA1.1")
setenv ( "%{MODULE_VAR}_G4PHOTONEVAPORATION", "%{GEANT4DATA}/PhotonEvaporation3.2")
setenv ( "%{MODULE_VAR}_G4RADIOACTIVEDECAY", "%{GEANT4DATA}/RadioactiveDecay4.3")
setenv ( "%{MODULE_VAR}_G4REALSURFACE", "%{GEANT4DATA}/RealSurface1.0")

EOF

%if "%{PLATFORM}" == "ls5"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("gcc/4.9.3", "cmake/3.4.1")
EOF
%endif

# NOTE: this build will fail on stampede because cmake >3.3 is required!
%if "%{PLATFORM}" == "stampede"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("gcc/4.9.1", "cmake/3.1.0")
EOF
%endif

## Modulefile End
#--------------------------------------

# Lua sytax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#--------------------------------------
## VERSION FILE
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
## VERSION FILE END
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}

## POST 
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT


# In SPECS dir:
# ./build_rpm.sh --gcc=49 geant4-10.2-1.spec
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

