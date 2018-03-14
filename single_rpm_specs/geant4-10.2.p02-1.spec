#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME geant4
Version:  10.2.p02
Release:  1
License:  Geant4 Software License
Group:    Applications/Life Sciences
Source0:  https://geant4.web.cern.ch/geant4/support/source/geant4.10.02.p02.tar.gz
Source1:  https://geant4.web.cern.ch/geant4/support/source/G4NDL.4.5.tar.gz
Source2:  https://geant4.web.cern.ch/geant4/support/source/G4EMLOW.6.48.tar.gz
Source3:  https://geant4.web.cern.ch/geant4/support/source/G4PhotonEvaporation.3.2.tar.gz
Source4:  https://geant4.web.cern.ch/geant4/support/source/G4RadioactiveDecay.4.3.2.tar.gz
Source5:  https://geant4.web.cern.ch/geant4/support/source/G4SAIDDATA.1.1.tar.gz
Source6:  https://geant4.web.cern.ch/geant4/support/source/G4NEUTRONXS.1.4.tar.gz
Source7:  https://geant4.web.cern.ch/geant4/support/source/G4ABLA.3.0.tar.gz
Source8:  https://geant4.web.cern.ch/geant4/support/source/G4PII.1.3.tar.gz
Source9:  https://geant4.web.cern.ch/geant4/support/source/RealSurface.1.0.tar.gz
Source10: https://geant4.web.cern.ch/geant4/support/source/G4ENSDFSTATE.1.2.3.tar.gz
Source11: https://geant4.web.cern.ch/geant4/support/source/G4TENDL.1.0.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  A toolkit for the simulation of the passage of particles through matter.

### NOTE: Source0 is the main distribution called in this spec file. The other 
### 11 source files (Source1-Source11) are about 3.2 GB when unpacked. So to 
### save some space, we already unpacked them here (on stampede):
###               /scratch/projects/tacc/bio/geant4/10.2/
### They are packaged with the app on ls5.

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}GEANT4

# define the data dirs and make sure they exist
%if "%{PLATFORM}" == "ls5"
    %define GEANT4DATA  %{INSTALL_DIR}/share/Geant4-10.2.2/data
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
%setup -n %{PNAME}.10.02.p02

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

mv %{PNAME}.10.02.p02 %{PNAME}-%{version}-cmake
mkdir %{PNAME}.10.02.p02 # the clean script will complain if this is not here
mkdir -p %{PNAME}-%{version}/share/Geant4-10.2.2/data
mkdir %{PNAME}-%{version}-cmake/build/
cd %{PNAME}-%{version}-cmake/build/

%if "%{PLATFORM}" == "ls5"
for G4LIB in ` ls /work/03439/wallen/files/geant4-extras `
do
	tar -xzf /work/03439/wallen/files/geant4-extras/$G4LIB -C $RPM_BUILD_DIR/%{PNAME}-%{version}/share/Geant4-10.2.2/data
done
cmake -DGEANT4_INSTALL_DATA=ON -DGEANT4_INSTALL_DATADIR=$RPM_BUILD_DIR/%{PNAME}-%{version}/share/Geant4-10.2.2/data -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_DIR/%{PNAME}-%{version} -DGEANT4_BUILD_MULTITHREADED=ON ../
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

# Install MPI libs
%if "%{PLATFORM}" == "ls5"
cd ../
mkdir build-mpi/
cd build-mpi/
cmake -DGeant4_DIR=$RPM_BUILD_ROOT/%{INSTALL_DIR}/lib64/Geant4-10.2.2 -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_DIR/%{PNAME}-%{version}/mpi ../examples/extended/parallel/MPI/source

make -j 4
make install

cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/mpi $RPM_BUILD_ROOT/%{INSTALL_DIR}/
%endif


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
Documentation is available online at: http://geant4.web.cern.ch/geant4/

The top-level directory can be found in $%{MODULE_VAR}_DIR
The MPI libraries and include files can be found in $%{MODULE_VAR}_MPI
The data files can be found in $%{MODULE_VAR}_SHARE/Geant4-10.2.2/data/

Normally when using %{PNAME}, the user must source the scripts geant4.sh and geant4make.sh.
Loading this module does that automatically.

When compiling serial or multithreaded code with this version of %{PNAME}, do:

  cmake -DGeant4_DIR=$TACC_GEANT4_DIR/lib64/Geant4-10.2.2 \
        /path/to/code/

When compiling MPI code with this version of %{PNAME}, first load the cray_mpich/7.3.0 
module, then do:

  cmake -DGeant4_DIR=$TACC_GEANT4_DIR/lib64/Geant4-10.2.2 \
        -DG4mpi_DIR=$TACC_GEANT4_MPI/lib64/G4mpi-10.2.2 \
        /path/to/code/

In each example, "/path/to/code/" is replaced with the location of your %{PNAME} code.

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, simulation")
whatis("Keywords: Biology, Detector simulation, High energy, Nuclear physics")
whatis("Description: Geant4 is a toolkit for the simulation of the passage of particles through matter.")
whatis("URL: http://geant4.web.cern.ch/geant4/")

prepend_path( "PATH",            "%{INSTALL_DIR}/bin")
prepend_path( "LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib64")
prepend_path( "LD_LIBRARY_PATH", "%{INSTALL_DIR}/mpi/lib64")

setenv( "%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv( "%{MODULE_VAR}_BIN",     "%{INSTALL_DIR}/bin")
setenv( "%{MODULE_VAR}_INCLUDE", "%{INSTALL_DIR}/include")
setenv( "%{MODULE_VAR}_LIB",     "%{INSTALL_DIR}/lib64")
setenv( "%{MODULE_VAR}_MPI",     "%{INSTALL_DIR}/mpi")
setenv( "%{MODULE_VAR}_SHARE",   "%{INSTALL_DIR}/share")

setenv( "G4ABLADATA",        "%{GEANT4DATA}/G4ABLA3.0")
setenv( "G4LEDATA",          "%{GEANT4DATA}/G4EMLOW6.48")
setenv( "G4ENSDFSTATEDATA",  "%{GEANT4DATA}/G4ENSDFSTATE1.2.3")
setenv( "G4NEUTRONHPDATA",   "%{GEANT4DATA}/G4NDL4.5")
setenv( "G4NEUTRONXSDATA",   "%{GEANT4DATA}/G4NEUTRONXS1.4")
setenv( "G4PIIDATA",         "%{GEANT4DATA}/G4PII1.3")
setenv( "G4SAIDXSDATA",      "%{GEANT4DATA}/G4SAIDDATA1.1")
setenv( "G4LEVELGAMMADATA",  "%{GEANT4DATA}/PhotonEvaporation3.2")
setenv( "G4RADIOACTIVEDATA", "%{GEANT4DATA}/RadioactiveDecay4.3.2")
setenv( "G4REALSURFACEDATA", "%{GEANT4DATA}/RealSurface1.0")

setenv( "G4INCLUDE",          "%{INSTALL_DIR}/include/Geant4")
setenv( "G4INSTALL",          "%{INSTALL_DIR}/share/Geant4-10.2.2/geant4make")
setenv( "G4LIB",              "%{INSTALL_DIR}/lib64/Geant4-10.2.2")
setenv( "G4SYSTEM",           "Linux-g++")
setenv( "G4LIB_BUILD_SHARED", "1")
setenv( "G4LIB_USE_ZLIB",     "1")
setenv( "G4MULTITHREADED",    "1")
setenv( "G4UI_USE_TCSH",      "1")

EOF

# Not sure if these are needed:
# setenv( "G4WORKDIR", "/home1/03439/wallen/geant4_workdir")
# prepend_path( "PATH", "/home1/03439/wallen/geant4_workdir/bin/Linux-g++")

%if "%{PLATFORM}" == "ls5"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
setenv( "CC",  "/opt/apps/gcc/4.9.3/bin/gcc")
setenv( "CXX", "/opt/apps/gcc/4.9.3/bin/g++")

prereq("gcc/4.9.3", "cmake/3.4.1")
EOF
%endif

# NOTE: this build will fail on stampede because cmake >3.3 is required!
%if "%{PLATFORM}" == "stampede"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
setenv( "CC",  "/opt/apps/gcc/4.9.1/bin/gcc")
setenv( "CXX", "/opt/apps/gcc/4.9.1/bin/g++")

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
# ./build_rpm.sh --gcc=49 geant4-10.2.p02-1.spec
# ./build_rpm.sh --gcc=49 --cmpich=7_3 geant4-10.2.p02-1.spec # ls5
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

