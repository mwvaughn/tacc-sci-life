#
# Jawon Song
# 2017-09-01
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

%define shortsummary The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name sratoolkit

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 8
%define patch_version 2

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc                  
#%include ./include/%{PLATFORM}/compiler-defines.inc
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
URL:       https://github.com/ncbi/sra-tools
Packager:  TACC - jawon@tacc.utexas.edu
Source:    http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/%{pkg_version}/%{pkg_base_name}.%{pkg_version}-1-centos_linux64.tar.gz

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
%setup -n %{pkg_base_name}.%{pkg_version}-1-centos_linux64

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
#%include ./include/%{PLATFORM}/compiler-load.inc
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

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}/

case $TACC_SYSTEM in
wrangler)
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/scratch_cache << 'EOS'
#!/bin/bash

# Make ncbi config folder
[ -e $HOME/.ncbi ] || mkdir $HOME/.ncbi

# Make ncbi cache folder on scratch
[ -e $DATA/ncbi ] || mkdir $DATA/ncbi

cat > $HOME/.ncbi/user-settings.mkfg << EOF
/repository/user/main/public/root = "$DATA/ncbi"
EOF

echo "$DATA/ncbi will now be used to cache sra files"
EOS
;;
*)
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/scratch_cache << 'EOS'
#!/bin/bash

# Make ncbi config folder
[ -e $HOME/.ncbi ] || mkdir $HOME/.ncbi

# Make ncbi cache folder on scratch
[ -e $SCRATCH/ncbi ] || mkdir $SCRATCH/ncbi

cat > $HOME/.ncbi/user-settings.mkfg << EOF
/repository/user/main/public/root = "$SCRATCH/ncbi"
EOF

echo "$SCRATCH/ncbi will now be used to cache sra files"
EOS
;;
esac
chmod +x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/scratch_cache

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
 - %{MODULE_VAR}_EXAMPLE - example files

To improve download speed, the prefetch command has been aliased to always
use aspera. We also suggest running

$ scratch_cache

to change your cache directory to use the scratch filesystem.

Documentation can be found online at https://github.com/ncbi/sra-tools/wiki

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, archive, ncbi")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

setenv("%{MODULE_VAR}_DIR",	"%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_EXAMPLE",	pathJoin("%{INSTALL_DIR}","example"))

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}","bin"))
set_alias("prefetch","prefetch -a \"$TACC_ASPERA_ASCP|$TACC_ASPERA_KEY\"")
always_load("aspera-connect")
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
