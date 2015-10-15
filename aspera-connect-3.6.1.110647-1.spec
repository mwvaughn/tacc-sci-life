Name: aspera-connect
Version: 3.6.1.110647
Release: 1
License: IBM License
Vendor: IBM
Packager: TACC - gzynda@tacc.utexas.edu
Source: http://download.asperasoft.com/download/sw/connect/3.6.1/aspera-connect-3.6.1.110647-linux-64.tar.gz
Summary: Aspera Connect

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}ASPERA
%define PNAME       aspera-connect

%package %{PACKAGE}
Summary: Aspera Connect client
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: Aspera Connect client
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
The ascp (Aspera secure copy) executable is a command-line fasp transfer program.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif

## SETUP
%setup -n %{PNAME}-%{version}-linux-64 -c

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

#--------------------------------------
%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    ########### Do Not Remove #############

#--------------------------------------
## Install Steps Start
module purge
module load TACC python

export PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR}

## Patch
patch aspera-connect-3.6.1.110647-linux-64.sh -i - <<'EOF'
11c11
< INSTALL_DIR=~/.aspera/connect
---
> INSTALL_DIR=$PREFIX
EOF

## Install Steps End
#--------------------------------------
bash aspera-connect-3.6.1.110647-linux-64.sh

rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/etc/asperaconnect.path
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/var
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/res
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/localization
touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

%endif
#--------------------------------------

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
%if %{?BUILD_MODULEFILE}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
    ########### Do Not Remove #############

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{name}
distribution. Documentation can be found online at http://download.asperasoft.com/download/docs/ascp/3.5.2/html/index.html#dita/ascp_usage.html

Version %{version}

]])

whatis("Name: aspera-connect")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: transfer, ncbi, utility, genomics")
whatis("Description: Aspera Connect client")
whatis("URL: http://asperasoft.com/software/transfer-clients/")

local mod_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	mod_dir)

prepend_path("PATH",		pathJoin(mod_dir,"bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin(mod_dir,"lib"))

EOF
## Modulefile End
#--------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

%endif
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
%defattr(-,root,install,)
%{INSTALL_DIR}
%endif # ?BUILD_PACKAGE

%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE}
%defattr(-,root,install,)
%{MODULE_DIR}
%endif # ?BUILD_MODULEFILE

## POST 
%post %{PACKAGE}
export PACKAGE_POST=1
%include include/post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include include/post-defines.inc

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

