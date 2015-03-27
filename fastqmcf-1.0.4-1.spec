Name: fastqmcf
Version: 1.0.4
Release: 1
License: MIT
Group: Applications/Life Sciences
Source:  fastqmcf-1.0.4.zip
Packager: ARS - jun-wei.lin@ars.usda.gov
Summary: fastq-mcf sequence quality filter, clipping and processor.
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
%define MODULE_VAR  %{MODULE_VAR_PREFIX}FASTQMCF
%define PNAME       fastqmcf

## PACKAGE DESCRIPTION
%description
Scans a sequence file for adapters, and, based on a log-scaled threshold, determines a set of clipping parameters and performs clipping. Also does skewing detection and quality filtering.

## PREP
Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
module purge
module load TACC
module load perl
module load gsl

make CFLAGS="-O3 -I. -I$TACC_GSL_INC -L$TACC_GSL_LIB"

## Install Steps End
#------------------------------------------------

cp fastq-clipper $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp fastq-mcf $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp fastq-multx $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp fastq-join $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp fastq-stats $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp sam-stats $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp varcall $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
%{MODULE_VAR}_DIR for the location of the %{name}
distribution. Documentation can be found online at https://code.google.com/p/ea-utils/wiki/FastqMcf

NOTE: This module provides the fastq-mcf, fastq-multx, fastq-join, varcall binaries

Version %{version}

]])

whatis("Name: Fastqmcf")
whatis("Version: %{version}")
whatis("Category: Computational biology, Genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: https://code.google.com/p/ea-utils/wiki/FastqMcf")
whatis("Description: fastq-mcf sequence quality filter, clipping and processor")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

prereq("perl")
prereq("gsl")

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

