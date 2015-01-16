# $Id$

Name: bowtie
Version: 2.1.0
Release: 1
License: GPL
Group: Applications/Life Sciences
Source:  bowtie2-2.1.0-source.zip
Packager: TACC - jfonner@tacc.utexas.edu
Summary: Memory-efficient short read (NGS) aligner

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%define debug_package %{nil}
%include rpm-dir.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define APPS    /opt/apps
%define MODULES modulefiles
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BOWTIE
%define PNAME bowtie

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. It is particularly good at aligning reads of about 50 up to 100s or 1,000s of characters, and particularly good at aligning to relatively long (e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM Index to keep its memory footprint small: for the human genome, its memory footprint is typically around 3.2 GB. Bowtie 2 supports gapped, local, and paired-end alignment modes.

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{PNAME}2-%{version}

##
## BUILD
##

%build

##
## INSTALL
##
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/xsede/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc

# Since LDFLAGS is not used in compilation, we hijack EXTRA_FLAGS to carry the rpath payload
make EXTRA_FLAGS="-Wl,-rpath,$GCC_LIB"

cp -R ./bowtie2 ./bowtie2-align ./bowtie2-build ./bowtie2-inspect ./doc ./scripts $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{name} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{name}
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/bowtie2/

NOTE: Bowtie2 indexes are not backwards compatible with Bowtie1 indexes. 

This module provides the bowtie2, bowtie2-align, bowtie2-build, and bowtie2-inspect binaries + scripts

Version %{version}

]])

whatis("Name: Bowtie")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: http://bowtie-bio.sourceforge.net/bowtie2/")
whatis("Description: Ultrafast, memory-efficient short read aligner")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_SCRIPTS","%{INSTALL_DIR}/scripts")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

EOF

#--------------
#  Version file.
#--------------

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

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

