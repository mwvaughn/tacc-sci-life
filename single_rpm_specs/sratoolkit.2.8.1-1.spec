%define	  PNAME sratoolkit
Summary:  The NCBI SRA toolkit
Version:  2.8.1
License:  GPL
URL:      https://github.com/ncbi/sra-tools
Packager: TACC - jawon@tacc.utexas.edu
Source:	  http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/%{version}/%{PNAME}.%{version}-centos_linux64.tar.gz
Vendor:   NCBI
Group:    Applications/Life Sciences
Release:  1

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
%setup -n %{PNAME}.%{version}-centos_linux64

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

%{MODULE_VAR}_DIR - location of the %{PNAME} distribution
%{MODULE_VAR}_EXAMPLE - example files

To improve download speed, the prefetch command has been aliased to always
use aspera. We also suggest running

$ scratch_cache

to change your cache directory to use the scratch filesystem.

Documentation can be found online at https://github.com/ncbi/sra-tools/wiki

Version %{version}
]])

whatis("Name: sratools")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: archive, ncbi, utility, genomics")
whatis("Description: The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.")
whatis("URL: %{url}")

local sra_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	sra_dir)
setenv("%{MODULE_VAR}_EXAMPLE",	pathJoin(sra_dir,"example"))

prepend_path("PATH",		pathJoin(sra_dir,"bin"))
set_alias("prefetch","prefetch -a \"$TACC_ASPERA_ASCP|$TACC_ASPERA_KEY\"")
always_load("aspera-connect")
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
