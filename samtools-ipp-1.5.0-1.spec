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

%define shortsummary Tools (written in C using htslib) for manipulating next-generation sequencing data
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name samtools

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 5
%define patch_version 0

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
License:   MIT
Group:     Applications/Life Sciences
URL:       https://github.com/samtools/samtools
Packager:  TACC - gzynda@tacc.utexas.edu
Source:    samtools-%{pkg_version}.tar.bz2

%package %{PACKAGE}
Summary: %{shortsummary}
Group: Applications/Life Sciences
%description package
%{shortsummary}

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Module file for %{name}

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
%setup -n samtools-%{pkg_version}

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
module purge
%include ./include/%{PLATFORM}/compiler-load.inc
#%include ./include/%{PLATFORM}/mpi-load.inc
#%include ./include/%{PLATFORM}/mpi-env-vars.inc
##################################
# Manually load modules
##################################
module load zlib/1.2.8
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

export IPPROOT=/opt/intel/compilers_and_libraries_2017.4.196/linux/ipp
OPT="-O3 %{TACC_OPT} -ipo"
LZSTATIC="${TACC_ZLIB_LIB}/libz.a ${IPPROOT}/lib/intel64/libippdc.a ${IPPROOT}/lib/intel64/libipps.a ${IPPROOT}/lib/intel64/libippcore.a"

## Make HTSLIB
rm -rf htslib-%{version}/
cd .. && tar -xjf %{_sourcedir}/htslib-%{version}.tar.bz2
cd htslib-%{version}
./configure CFLAGS="${OPT} -I${IPPROOT}/include -I${TACC_ZLIB_INC}" --disable-libcurl --prefix=%{INSTALL_DIR}
# replace zlib
sed -i -e "s~\-lz~${LZSTATIC}~" -e "s~\-lm~-limf~" $(find . -type f | xargs -n 1 grep -lP "\-(lz|lm)")
make -j5 DESTDIR=${RPM_BUILD_ROOT} all
make DESTDIR=${RPM_BUILD_ROOT} install
cd .. && rm -rf htslib-%{version} && cd samtools-1.5
find ${RPM_BUILD_ROOT}

## Make Samtools
./configure CFLAGS="${OPT} -I${IPPROOT}/include -I${TACC_ZLIB_INC}" --with-htslib=${RPM_BUILD_ROOT}/%{INSTALL_DIR} --prefix=%{INSTALL_DIR}
# replace zlib
sed -i -e "s~\-lz~${LZSTATIC}~" -e "s~\-lm~-limf~" $(find . -type f | xargs -n 1 grep -lP "\-(lz|lm)")
make -j5 DESTDIR=${RPM_BUILD_ROOT} all
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

## Make bcftools
tar -xjf %{_sourcedir}/bcftools-%{version}.tar.bz2
cd bcftools-%{version} && rm -rf htslib-%{version}/
./configure CFLAGS="${OPT} -I${IPPROOT}/include -I${TACC_ZLIB_INC}" --with-htslib=${RPM_BUILD_ROOT}/%{INSTALL_DIR} --prefix=%{INSTALL_DIR}
# replace zlib
sed -i -e "s~\-lz~${LZSTATIC}~" -e "s~\-lm~-limf~" $(find . -type f | xargs -n 1 grep -lP "\-(lz|lm)")
make -j5 DESTDIR=${RPM_BUILD_ROOT} all
make DESTDIR=${RPM_BUILD_ROOT} install
cd .. && rm -rf bcftools-%{version}

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
This version of samtools has been optimized using the Intel IPP tuned zlib for extra performance.

The %{pkg_base_name} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN
 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_INC

for the location of the %{name} distribution.

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")

family("samtools")
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
# $RPM_INSTALL_PREFIX0 /tmpmod -> /opt/apps
# $RPM_INSTALL_PREFIX1 /tmprpm -> /opt/apps

%post %{MODULEFILE}
export MODULEFILE_POST=1
%include ./include/%{PLATFORM}/post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

