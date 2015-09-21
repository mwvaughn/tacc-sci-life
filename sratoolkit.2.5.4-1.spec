Name: sratoolkit
Version: 2.5.4
Release: 1
License: GPL
Source: http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.5.4/sratoolkit.2.5.4-centos_linux64.tar.gz
Packager: TACC - gzynda@tacc.utexas.edu
Summary: The NCBI SRA toolkit

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}SRATOOLKIT
%define PNAME       sratoolkit

%package %{PACKAGE}
Summary: The NCBI SRA toolkit
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: The NCBI SRA toolkit
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.

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
%setup -n %{PNAME}.%{version}-centos_linux64

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

## Install Steps End
#--------------------------------------
cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}
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
distribution. Documentation can be found online at https://github.com/ncbi/sra-tools/wiki

Version %{version}

]])

whatis("Name: sratools")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: archive, ncbi, utility, genomics")
whatis("Description: The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.")
whatis("URL: https://github.com/ncbi/sra-tools")

local sra_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	sra_dir)
setenv("%{MODULE_VAR}_EXAMPLES",	pathJoin(sra_dir,"examples"))

prepend_path("PATH",		pathJoin(sra_dir,"bin"))

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

