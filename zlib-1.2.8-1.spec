#
# Greg Zynda
# 2017-08-01
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

Summary: A Massively Spiffy Yet Delicately Unobtrusive Compression Librar

# Give the package a base name
%define pkg_base_name zlib

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 2
%define patch_version 8

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
#BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1
License:   BSD
Group:     Applications, Libraries
URL:       http://zlib.net
Packager:  TACC - gzynda@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary:   A Massively Spiffy Yet Delicately Unobtrusive Compression Library
Group:     Applications, Libraries
%description package
zlib: A Massively Spiffy Yet Delicately Unobtrusive Compression Library

%package %{MODULEFILE}
Summary:   A Massively Spiffy Yet Delicately Unobtrusive Compression Library
Group: Lmod/Modulefiles
%description modulefile
zlib: A Massively Spiffy Yet Delicately Unobtrusive Compression Library

%description
zlib: A Massively Spiffy Yet Delicately Unobtrusive Compression Library

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

# Comment this out if pulling from git
%setup -n %{pkg_base_name}-%{pkg_version}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include ./include/%{PLATFORM}/system-load.inc

# Insert necessary module commands
##################################
# If using build_rpm
module purge
%include ./include/%{PLATFORM}/compiler-load.inc
#%include ./include/%{PLATFORM}/mpi-load.inc
#%include ./include/%{PLATFORM}/mpi-env-vars.inc
# If not
# module load modules
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

# Source IPP
tar -xzf $IPPROOT/examples/components_and_examples_lin_ps.tgz ./components/interfaces/ipp_zlib/zlib-1.2.8.patch
source /opt/intel/compilers_and_libraries_2017.4.196/linux/ipp/bin/ippvars.sh intel64

# Patch zlib
patch -p1 < components/interfaces/ipp_zlib/zlib-%{version}.patch

# Compile zlib
source /opt/intel/compilers_and_libraries_2017.4.196/linux/bin/compilervars.sh intel64
export CFLAGS="-O3 %{TACC_OPT} -fPIC -m64 -DWITH_IPP -I$IPPROOT/include"
export LDFLAGS="$IPPROOT/lib/intel64/libippdc.a $IPPROOT/lib/intel64/libipps.a $IPPROOT/lib/intel64/libippcore.a"
./configure --prefix=%{INSTALL_DIR}
make shared
make DESTDIR=${RPM_BUILD_ROOT} install

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
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_INC

for the location of the %{PNAME} distribution.

For static linking on Linux* OS, 

  gcc -O3 -o zpipe_ipp.out zpipe.c -I$%{MODULE_VAR}_INC $%{MODULE_VAR}_LIB/libz.a

For static linking on Linux* OS, 

  gcc -O3 -o zpipe_ipp.out zpipe.c -I$%{MODULE_VAR}_INC -L$%{MODULE_VAR}_LIB -lz

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: applications, compression")
whatis("Keywords: compressino, deflate")
whatis("Description: A Massively Spiffy Yet Delicately Unobtrusive Compression Library")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")
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
