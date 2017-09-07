#
# Joe Allen
# 2017-09-07
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

%define shortsummary Open Babel is an open source chemistry toolbox
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name openbabel

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 4
%define patch_version 1

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc                  
%include ./include/%{PLATFORM}/compiler-defines.inc
#%include ./include/%{PLATFORM}/mpi-defines.inc
%include ./include/%{PLATFORM}/name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
########################################

Release:   1
License:   GPL
Group:     Applications/Life Sciences
URL:       http://openbabel.org/wiki/Main_Page
Packager:  TACC - wallen@tacc.utexas.edu
Source:    %{pkg_base_name}-%{major_version}-%{minor_version}-%{patch_version}.tar.gz
Patch1:    openbabel-2-4-1.patch

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
%setup -n %{pkg_base_name}-%{pkg_base_name}-%{major_version}-%{minor_version}-%{patch_version}
# If using multiple sources. Make sure that the "-n" names match.
#%setup -T -D -a 1 -n %{pkg_base_name}-%{pkg_version}
%patch1 -p1

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
#%include ./include/%{PLATFORM}/mpi-load.inc
#%include ./include/%{PLATFORM}/mpi-env-vars.inc
##################################
# Manually load modules
##################################
# module load
module load cmake/3.8.2
##################################

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

# Eigen2 include files are necessary (do not need to install)
wget http://bitbucket.org/eigen/eigen/get/2.0.17.tar.gz
mkdir eigen-2.0.17/
tar -xvzf 2.0.17.tar.gz -C eigen-2.0.17/ --strip-components=1

mkdir build/
cd build/

cmake -DCMAKE_INSTALL_PREFIX=../install \
      -DCMAKE_CXX_COMPILER=$I_MPI_CXX \
      -DCMAKE_C_COMPILER=$I_MPI_CC \
      -DCMAKE_CXX_FLAGS="%{TACC_OPT}" \
      -DCMAKE_C_FLAGS="%{TACC_OPT}" \
      -DENABLE_OPENMP=ON \
      -DBUILD_EXAMPLES=ON \
      -DEIGEN2_INCLUDE_DIR="$PWD/../eigen-2.0.17" \
      -Wno-dev \
      ../

make -j4
make install


# Getting rpm fail on /usr/lib/rpm/check-buildroot, so trying this
cd ../
cp -r install/* $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf install/*

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

 - TACC_BABEL_DIR
 - TACC_BABEL_BIN
 - TACC_BABEL_LIB
 - TACC_BABEL_SHARE

for the location of the %{pkg_base_name} distribution.

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Computational Biology, Chemistry, Docking, Small Molecule")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")

setenv("TACC_BABEL_DIR",     "%{INSTALL_DIR}")
setenv("TACC_BABEL_BIN",	"%{INSTALL_DIR}/bin")
setenv("TACC_BABEL_LIB",	"%{INSTALL_DIR}/lib")
setenv("TACC_BABEL_SHARE",	"%{INSTALL_DIR}/share")

setenv("BABEL_LIBDIR",		"%{INSTALL_DIR}/lib/%{pkg_base_name}/%{version}")
setenv("BABEL_DATADIR",		"%{INSTALL_DIR}/share/%{pkg_base_name}/%{version}")

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
