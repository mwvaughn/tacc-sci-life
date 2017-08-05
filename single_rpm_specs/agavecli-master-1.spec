Name: agavecli
Version: master
Release: 1
License: Custom - Redistribution allowed
Group: Applications/Life Sciences
Packager: TACC - jfonner@tacc.utexas.edu
Summary: The Agave Platform is an open source, science-as-a-service API platform for powering your digital lab
Prefix: /opt/apps

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

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}AGAVECLI
%define PNAME       agavecli

## PACKAGE DESCRIPTION
%description
The Agave Platform (http://agaveapi.co) is an open source, science-as-a-service API platform for powering your digital lab. Agave allows you to bring together your public, private, and shared high performance computing (HPC), high throughput computing (HTC), Cloud, and Big Data resources under a single, web-friendly REST API.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
# no setup section.  I'm using github to pull this down...
# %setup -n %{PNAME}2-%{version}

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
module purge
module load TACC
module load git

git clone https://bitbucket.org/taccaci/foundation-cli.git agave-cli
## Install Steps End
#------------------------------------------------

cp -a  ./agave-cli/. $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{name}
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/bowtie2/

NOTE: Bowtie2 indexes are not backwards compatible with Bowtie1 indexes. 

This module provides the bowtie2, bowtie2-align, bowtie2-build, and bowtie2-inspect binaries + scripts

Version %{version}

]])

whatis("Name: agavecli")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, API, iPlant")
whatis("URL: http://agaveapi.co/")
whatis("Description: An open source, science-as-a-service API platform for powering your digital lab")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
prepend_path("PATH"       ,"%{INSTALL_DIR}/bin")

EOF
## Modulefile End
#------------------------------------------------

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

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
#%files -n %{name}-%{comp_fam_ver}
%files 

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

## CLEAN UP
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

