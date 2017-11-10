#
# Joe Allen
# 2017-11-09
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

%define shortsummary EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name eman

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2
#%define patch_version 0

%define pkg_version %{major_version}.%{minor_version}

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
License:   GPLv2
Group:     Applications/Life Sciences
URL:       http://blake.bcm.tmc.edu/EMAN2/
Packager:  TACC - wallen@tacc.utexas.edu
Source:    v%{major_version}.%{minor_version}.tar.gz

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
%setup -n %{pkg_base_name}%{major_version}-%{major_version}.%{minor_version}
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
#%include ./include/%{PLATFORM}/mpi-load.inc
#%include ./include/%{PLATFORM}/mpi-env-vars.inc
##################################
# Manually load modules
##################################
# module load
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

module purge
module load TACC
module load cmake/3.8.2 gsl/2.3 boost/1.64 qt4/4.8.7 fftw3/3.3.6 hdf5/1.8.16

BUILD_DIR=`dirname $(pwd)`
TMP_INSTALL_DIR="${BUILD_DIR}/install"
rm -rf ${TMP_INSTALL_DIR}/
mkdir ${TMP_INSTALL_DIR}

# Example configure and make
mkdir build-dependencies/
cd build-dependencies/


##### Install FTGL from git #####
git clone https://github.com/ulrichard/ftgl
cd ftgl
./autogen.sh
./configure --prefix=${TMP_INSTALL_DIR}/dependencies
make -j4
make install 
cd ../


##### Install sip #####
wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.3/sip-4.19.3.tar.gz
tar -xvzf sip-4.19.3.tar.gz
cd sip-4.19.3/

python configure.py \
       --bindir=${TMP_INSTALL_DIR}/dependencies/bin \
       --destdir=${TMP_INSTALL_DIR}/dependencies/lib/python2.7/site-packages \
       --incdir=${TMP_INSTALL_DIR}/dependencies/include/python2.7 \
       --sipdir=${TMP_INSTALL_DIR}/dependencies/share/sip \
       --stubsdir=${TMP_INSTALL_DIR}/dependencies/lib/python2.7/site-packages 

make -j4
make install
cd ../

# put sip in environment to install pyqt4
export PYTHONPATH=${TMP_INSTALL_DIR}/dependencies/lib/python2.7/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=${TMP_INSTALL_DIR}/dependencies/lib/python2.7/site-packages:$LD_LIBRARY_PATH
export PATH=${TMP_INSTALL_DIR}/dependencies/bin:$PATH


##### Install pyqt4 #####
wget https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.12.1/PyQt4_gpl_x11-4.12.1.tar.gz
tar -xvzf PyQt4_gpl_x11-4.12.1.tar.gz

cd PyQt4_gpl_x11-4.12.1/
python configure-ng.py \
       --confirm-license \
       --bindir=${TMP_INSTALL_DIR}/dependencies/bin \
       --destdir=${TMP_INSTALL_DIR}/dependencies/lib/python2.7/site-packages \
       --designer-plugindir=${TMP_INSTALL_DIR}/dependencies/designer \
       --enable=QtCore \
       --enable=QtGui \
       --enable=QtOpenGL \
       --enable=QtWebKit \
       --sip-incdir=${TMP_INSTALL_DIR}/dependencies/include/python2.7 \
       --no-sip-files

# Bug in curret qt4 module
for FILE in ./qtdetail.mk ./pylupdate/Makefile ./pyrcc/Makefile ./QtCore/Makefile ./QtGui/Makefile ./Qt/Makefile ./QtOpenGL/Makefile ./QtOpenGL/Makefile ./QtWebKit/Makefile
do
sed -i 's/\/scratch\/01206\/jbarbosa\/rpmbuild\/BUILDROOT\/tacc-qt4-4.8.7-5.el7.centos.x86_64\/tmprpm/\/opt\/apps/g' $FILE
sed -i 's/\/scratch\/01206\/jbarbosa\/rpmbuild\/BUILDROOT\/tacc-qt4-4.8.7-5.el7.centos.x86_64\/\/tmprpm/\/opt\/apps/g' $FILE
done

make -j4
make install
cd ../


##### Install PyOpenGL #####
wget https://pypi.python.org/packages/df/fe/b9da75e85bcf802ed5ef92a5c5e4022bf06faa1d41b9630b9bb49f827483/PyOpenGL-3.1.1a1.tar.gz#md5=77ee6044ceb2cf952aca89a9b2d3d585
tar -xvzf PyOpenGL-3.1.1a1.tar.gz
cd PyOpenGL-3.1.1a1/
python setup.py install --prefix=${TMP_INSTALL_DIR}/dependencies
cd ../


##### Install EMAN2 #####
# set up environment
export FFTWDIR=$TACC_FFTW3_DIR
export GSLDIR=$TACC_GSL_DIR
export BOOSTDIR=$TACC_BOOST_DIR
export HDF5DIR=$TACC_HDF5_DIR
export PYTHON_ROOT=/opt/apps/intel17/python/2.7.13/
export PYTHON_VERSION=2.7.13
export QMAKESPEC=/opt/apps/qt4/4.8.7/mkspecs/linux-g++/
export CC=`which icc`
export CXX=`which icpc`

cd ../
mkdir build/
cd build

cmake -DEMAN_INSTALL_PREFIX=${TMP_INSTALL_DIR} \
      -DCMAKE_C_COMPILER=icc \
      -DCMAKE_CXX_COMPILER=icpc \
      -DCMAKE_CXX_FLAGS="-O3 %{TACC_OPT} -I/usr/include/freetype2 " \
      -DCMAKE_C_FLAGS="-O3 %{TACC_OPT} -I/usr/include/freetype2 " \
      -DFTGL_INCLUDE_PATH=${TMP_INSTALL_DIR}/dependencies/include \
      -DFTGL_LIBRARY=${TMP_INSTALL_DIR}/dependencies/lib/libftgl.so \
      -DNUMPY_INCLUDE_PATH=$TACC_PYTHON_LIB/python2.7/site-packages/numpy-1.12.1-py2.7-linux-x86_64.egg/numpy/core/include \
      ../

make -j4    
make install

# small bug in eman2
cp ${TMP_INSTALL_DIR}/bin/e2version.py ${TMP_INSTALL_DIR}/lib/


# Move tmp install files into buildroot
cp -r ${TMP_INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}
rm -rf ${TMP_INSTALL_DIR}/



# Do I need to do this?
# replace /work/03439/wallen/rpmbuild/stampede2/BUILD/install with $TACC_EMAN_DIR
# what about binary files that match?
#sed -i 's/\/work\/03439\/wallen\/rpmbuild\/stampede2\/BUILD\/install/\$TACC_EMAN_DIR/g'  *



# OLD
# The following four files have python3 code which produce syntax errors 
# during brp-python-bytecompile:
#
# $PWD/install/lib/python2.7/lib2to3/tests/data/py3_test_grammar.py
# $PWD/install/lib/python2.7/site-packages/PyQt4/uic/port_v3/proxy_base.py
# $PWD/install/lib/python2.7/site-packages/jinja2/asyncfilters.py
# $PWD/install/lib/python2.7/site-packages/jinja2/asyncsupport.py
#
# This definition should make it so rpmbuild tries to compile all python
# executables, but does not terminate the build if a few fail:
# %global _python_bytecompile_errors_terminate_build 0

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
 - %{MODULE_VAR}_LIB

for the location of the %{pkg_base_name} distribution.

Threading is enabled in this installation; MPI is disabled.

To use this package, please load these modules first:

  intel/17.0.4
  boost/1.64
  gsl/2.3
  hdf5/1.8.16
  fftw3/3.3.6
  qt4/4.8.7

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Computational Biology, Chemistry, Structural Biology, Image Processing, Image Reconstruction, CryoEM")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")

setenv("EMAN2DIR",              "%{INSTALL_DIR}")

prepend_path("PATH",            "%{INSTALL_DIR}/dependencies/bin")
prepend_path("PATH",            "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/dependencies/lib/python2.7/site-packages")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/dependencies/lib")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")
prepend_path("PYTHONPATH",      "%{INSTALL_DIR}/dependencies/lib/python2.7/site-packages")
prepend_path("PYTHONPATH",      "%{INSTALL_DIR}/lib")

prereq("boost/1.64", "gsl/2.3", "hdf5/1.8.16", "fftw3/3.3.6", "qt4/4.8.7")

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
