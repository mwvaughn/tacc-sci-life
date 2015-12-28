
# curl -skL -o "sickle-1.2.zip" "https://github.com/najoshi/sickle/archive/v1.2.zip"

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME sickle
Summary: A windowed adaptive trimming tool for FASTQ files using quality
Version: 1.2
Release: 2
License: Artistic
Group: Applications/Life Sciences
Source:  sickle-1.2.zip
Packager: TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}SICKLE

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Sickle is a tool that uses sliding windows along with quality and length thresholds to determine when quality is sufficiently low to trim the 3'-end of reads and also determines when the quality is sufficiently high enough to trim the 5'-end of reads. It will also discard reads based upon the length threshold.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start

module swap $TACC_FAMILY_COMPILER gcc
make
cp -R ./sickle ./sickle.xml $RPM_BUILD_ROOT/%{INSTALL_DIR}

## Install Steps End
#------------------------------------------------

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
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/

Version %{version}
]])

whatis("Name: Sickle")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing")
whatis("URL: https://github.com/ucdavis-bioinformatics/sickle")
whatis("Description: A windowed adaptive trimming tool for FASTQ files using quality")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

EOF

## Modulefile End
#------------------------------------------------

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
