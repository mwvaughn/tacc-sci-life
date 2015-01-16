# $Id$

Name:       bwa
Summary:    Burrows-Wheeler Alignment Tool
Version:    0.7.12
Release:    1
License:    GPLv3
Vendor:     Heng Li at the Sanger Institute
Group: Applications/Life Sciences
Source:     http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.12.tar.bz2
Packager:   TACC - vaughn@tacc.utexas.edu

# Based off of John Fonner's spec file bowtie-2.1.0-2
# http://sourceforge.net/projects/bio-bwa

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn off building a debug package
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}BWA
%define PNAME       bwa

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
BWA is a software package for mapping low-divergent sequences against a large reference genome, such as the human genome. It consists of three algorithms: BWA-backtrack, BWA-SW and BWA-MEM. The first algorithm is designed for Illumina sequence reads up to 100bp, while the rest two for longer sequences ranged from 70bp to 1Mbp. BWA-MEM and BWA-SW share similar features such as long-read support and split alignment, but BWA-MEM, which is the latest, is generally recommended for high-quality queries as it is faster and more accurate. BWA-MEM also has better performance than BWA-backtrack for 70-100bp Illumina reads.

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{PNAME}-%{version}

##
## BUILD
##

%build

##
## INSTALL
##
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

## INSTALLSTART
module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc

# Since LDFLAGS is not used in compilation, we hijack EXTRA_FLAGS to carry the rpath payload
make EXTRA_FLAGS="-Wl,-rpath,$GCC_LIB"

## INSTALLEND

cp ./bwa *.pl $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
Documentation can be found online at http://bio-bwa.sourceforge.net/bwa.shtml
The bwa executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: bwa")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing")
whatis("Description: Burrows-Wheeler Alignment Tool")
whatis("URL: http://bio-bwa.sourceforge.net/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

EOF
## End Decorator

#--------------
#  Version file.
#--------------

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

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
