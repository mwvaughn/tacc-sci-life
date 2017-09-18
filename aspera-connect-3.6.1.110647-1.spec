#
# Name
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

%define shortsummary Aspera Connect client
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name aspera-connect

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 6
%define patch_version 1.110647

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

Release:   2
License:   IBM
Group:     Applications/Life Sciences
Url:       http://download.asperasoft.com/download/docs/ascp/3.5.2/html/index.html#dita/ascp_usage.html
Packager:  TACC - gzynda@tacc.utexas.edu
Source:    http://download.asperasoft.com/download/sw/connect/3.6.1/aspera-connect-3.6.1.110647-linux-64.tar.gz

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
%setup -n %{PNAME}-%{version}-linux-64 -c
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
#%include ./include/%{PLATFORM}/compiler-load.inc
#%include ./include/%{PLATFORM}/mpi-load.inc
#%include ./include/%{PLATFORM}/mpi-env-vars.inc
%define MODULE_VAR  %{MODULE_VAR_PREFIX}ASPERA
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

export PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR}

## Patch
patch aspera-connect-3.6.1.110647-linux-64.sh -i - <<'EOF'
11c11
< INSTALL_DIR=~/.aspera/connect
---
> INSTALL_DIR=$PREFIX
EOF

bash aspera-connect-3.6.1.110647-linux-64.sh

rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/etc/asperaconnect.path
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/var
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/res
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/localization
# comes with a libc that breaks things
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

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
 - %{MODULE_VAR}_ASCP - the location of the ascp program
 - %{MODULE_VAR}_OPENSSH - the location of the openssh key

for the location of the %{pkg_base_name} distribution.

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, transfer, ncbi, utility")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

setenv("%{MODULE_VAR}_DIR",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_ASCP",	"%{INSTALL_DIR}/bin/ascp")
setenv("%{MODULE_VAR}_KEY",	"%{INSTALL_DIR}/etc/asperaweb_id_dsa.openssh")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
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
