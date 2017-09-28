#
# Joe Allen
# 2017-09-27
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

%define shortsummary Geant4 is a toolkit for the simulation of the passage of particles through matter
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name geant4

# Create some macros (spec file variables)
%define major_version 10
%define minor_version 3
%define patch_version p02

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc                  
%include ./include/%{PLATFORM}/compiler-defines.inc
%include ./include/%{PLATFORM}/mpi-defines.inc
%include ./include/%{PLATFORM}/name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
########################################

Release:   1
License:   Geant4 Software License
Group:     Applications/Life Sciences
URL:       https://geant4.web.cern.ch/geant4/
Packager:  TACC - wallen@tacc.utexas.edu
Source:    %{pkg_base_name}.%{major_version}.0%{minor_version}.%{patch_version}.tar.gz

%package %{PACKAGE}
Summary: %{shortsummary}
Group:   Applications/Life Sciences
%description package
%{pkg_base_name}: %{shortsummary}

%package %{MODULEFILE}
Summary: The modulefile RPM
Group:   Lmod/Modulefiles
%description modulefile
Module file for %{pkg_base_name}

%description
%{pkg_base_name}: %{shortsummary}

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Comment this out if pulling from git
%setup -n %{pkg_base_name}.%{major_version}.0%{minor_version}.%{patch_version}
# If using multiple sources. Make sure that the "-n" names match.
#%setup -T -D -a 1 -n %{pkg_base_name}-%{pkg_version}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include ./include/%{PLATFORM}/system-load.inc
##################################
# If using build_rpm
##################################
%include ./include/%{PLATFORM}/compiler-load.inc
%include ./include/%{PLATFORM}/mpi-load.inc
%include ./include/%{PLATFORM}/mpi-env-vars.inc
##################################
# Manually load modules
##################################
# module load
module load cmake/3.7.1
##################################

%define GEANT4DATA  /scratch/projects/tacc/bio/%{pkg_base_name}/%{version}

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================

# Example configure and make
mkdir -p install/mpi/       # install into here to avoid check-buildroot errors
mkdir build/ && cd build/

cmake   \
	-DCMAKE_C_COMPILER=icc \
	-DCMAKE_CXX_COMPILER=icpc \
	-DCMAKE_CXX_FLAGS="-O3 -DNDEBUG %{TACC_OPT} -w1 -Wno-non-virtual-dtor -Wpointer-arith -Wwrite-strings -fp-model precise" \
	-DCMAKE_C_FLAGS="-O3 -DNDEBUG %{TACC_OPT}" \
	-DCMAKE_INSTALL_PREFIX=../install \
	-DGEANT4_INSTALL_DATADIR=/scratch/projects/tacc/bio/geant4/10.3.p02/ \
	-DGEANT4_BUILD_MULTITHREADED=ON \
	../

make -j4
make install

cd ../
mkdir build-mpi/ && cd build-mpi/

cmake	\
	-DCMAKE_C_COMPILER=icc \
	-DCMAKE_CXX_COMPILER=icpc \
	-DCMAKE_CXX_FLAGS="-O3 -DNDEBUG %{TACC_OPT} -w1 -Wno-non-virtual-dtor -Wpointer-arith -Wwrite-strings -fp-model precise" \
	-DCMAKE_C_FLAGS="-O3 -DNDEBUG %{TACC_OPT}" \
	-DGeant4_DIR="$PWD/../install/lib64/Geant4-10.3.2" \
	-DCMAKE_INSTALL_PREFIX=../install/mpi \
	../examples/extended/parallel/MPI/source/

make -j4
make install

cd ../
cp -r install/* $RPM_BUILD_ROOT/%{INSTALL_DIR}


#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message = [[
The %{pkg_base_name} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN
 - %{MODULE_VAR}_INCLUDE
 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_MPI
 - %{MODULE_VAR}_SHARE

for the location of the %{pkg_base_name} distribution. The data files can be found in:

 %{GEANT4DATA}

When compiling serial or multithreaded code with this version of %{PNAME}, do:

  cmake -DCMAKE_C_COMPILER=icc \
        -DCMAKE_CXX_COMPILER=icpc \
        /path/to/code/

When compiling MPI code with this version of %{PNAME}, do:

  cmake -DCMAKE_C_COMPILER=icc \
        -DCMAKE_CXX_COMPILER=icpc \
        -DG4mpi_DIR=$TACC_GEANT4_MPI/lib64/G4mpi-10.3.2 \
        /path/to/code/

In each example, "/path/to/code/" is replaced with the location of your code.

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, simulation")
whatis("Keywords: Computational Biology, Detector simulation, High energy, Nuclear physics")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

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
setenv( "G4LEDATA",          "%{GEANT4DATA}/G4EMLOW6.50")
setenv( "G4ENSDFSTATEDATA",  "%{GEANT4DATA}/G4ENSDFSTATE2.1")
setenv( "G4NEUTRONHPDATA",   "%{GEANT4DATA}/G4NDL4.5")
setenv( "G4NEUTRONXSDATA",   "%{GEANT4DATA}/G4NEUTRONXS1.4")
setenv( "G4PIIDATA",         "%{GEANT4DATA}/G4PII1.3")
setenv( "G4SAIDXSDATA",      "%{GEANT4DATA}/G4SAIDDATA1.1")
setenv( "G4TENDLDATA",       "%{GEANT4DATA}/G4TENDL1.3")
setenv( "G4LEVELGAMMADATA",  "%{GEANT4DATA}/PhotonEvaporation4.3.2")
setenv( "G4RADIOACTIVEDATA", "%{GEANT4DATA}/RadioactiveDecay5.1.1")
setenv( "G4REALSURFACEDATA", "%{GEANT4DATA}/RealSurface1.0")

setenv( "G4INCLUDE",          "%{INSTALL_DIR}/include/Geant4")
setenv( "G4INSTALL",          "%{INSTALL_DIR}/share/Geant4-10.3.2/geant4make")
setenv( "G4LIB",              "%{INSTALL_DIR}/lib64/Geant4-10.3.2")
setenv( "G4SYSTEM",           "Linux-icc")
setenv( "G4LIB_BUILD_SHARED", "1")
setenv( "G4LIB_USE_ZLIB",     "1")
setenv( "G4MULTITHREADED",    "1")
setenv( "G4UI_USE_TCSH",      "1")

prereq("intel/17.0.4", "cmake/3.8.2")

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/scripts/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include ./include/%{PLATFORM}/post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include ./include/%{PLATFORM}/post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include ./include/%{PLATFORM}/post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT
