%define PNAME sratoolkit
Summary:    The NCBI SRA toolkit
Version: 2.5.5
License:    GPL
URL:        http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=software
Packager:   TACC - jawon@tacc.utexas.edu
Source:     http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.5.5/sratoolkit.2.7.0-centos_linux64.tar.gz
Vendor:     NCBI
Group: Applications/Life Sciences
Release:   1

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

## PACKAGE DESCRIPTION
%description
The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n %{PNAME}.2.7.0-centos_linux64

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

echo "%{PNAME} is being packaged from a vendor-supplied binary distribution"

## Install Steps End
#--------------------------------------
cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The SRA Toolkit module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME}
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
setenv("%{MODULE_VAR}_EXAMPLE",	pathJoin(sra_dir,"example"))

prepend_path("PATH",		pathJoin(sra_dir,"bin"))

EOF
## Modulefile End
#--------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

## VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
#%files -n %{name}-%{comp_fam_ver}
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
