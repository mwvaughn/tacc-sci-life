%define PNAME wgs
Summary:    WGS Assembler
Version: 8.3
License:    GPL
URL:        http://wgs-assembler.sourceforge.net/
Packager:   TACC - jawon@tacc.utexas.edu
Source:     http://sourceforge.net/projects/wgs-assembler/files/wgs-assembler/wgs-8.3/wgs-8.3rc2-Linux_amd64.tar.bz2
Vendor:     Celera Genomics
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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}WGS

## PACKAGE DESCRIPTION
%description
Celera Assembler is a de novo whole-genome shotgun (WGS) DNA sequence assembler.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n %{PNAME}-%{version}rc2

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
cp -R ./Linux-amd64/bin $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME}
distribution.

Version %{version}

]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Mapping")
whatis("Description: Celera assembler - de novo whole-genome shotgun (WGS) DNA sequence assembler")
whatis("URL: http://sourceforge.net/apps/mediawiki/wgs-assembler")

local wgs_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	wgs_dir)

prepend_path("PATH",		pathJoin(wgs_dir,"bin"))

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
