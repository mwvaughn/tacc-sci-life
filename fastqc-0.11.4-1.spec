%define PNAME fastqc
Summary:    FastQC - A quality control application for high throughput sequence data
Version: 0.11.4
License:    GPL
URL:        http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
Packager:   TACC - jawon@tacc.utexas.edu
Source:     http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.4.zip
Vendor:     Babraham Institute
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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}FASTQC

## PACKAGE DESCRIPTION
%description
FastQC is an application which takes a FastQ file and runs a series of tests on it to generate a comprehensive QC report.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n FastQC

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
chmod 755 fastqc
cp -R ./Templates ./fastqc  ./*.jar $RPM_BUILD_ROOT/%{INSTALL_DIR}


#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} built with %{comp_fam}.
Documentation for %{PNAME} is available online at http://www.bioinformatics.babraham.ac.uk/projects/fastqc
The executables are added on to path

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, FastQ, Quality Control")
whatis("Description: fastqc - A Quality Control application for FastQ files")
whatis("URL: http://www.bioinformatics.babraham.ac.uk/projects/fastqc")

local fastqc_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	fastqc_dir)

prepend_path("PATH",		fastqc_dir)

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
