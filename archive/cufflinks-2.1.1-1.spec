# $Id$

Summary:    cufflinks - Transcript assembly, differential expression, and differential regulation for RNA-Seq
Name:       cufflinks
Version:    2.1.1
Release:    1
License:    Boost Software License
Group: Applications/Life Sciences
Source:     http://cufflinks.cbcb.umd.edu/downloads/%{name}-%{version}.Linux_x86_64.tar.gz
Packager:   TACC - jfonner@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%define debug_package %{nil}
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME cufflinks
%define MODULE_VAR TACC_CUFFLINKS

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}


#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Cufflinks assembles transcripts, estimates their abundances, and tests for differential expression and regulation in RNA-Seq samples. It accepts aligned RNA-Seq reads and assembles the alignments into a parsimonious set of transcripts. Cufflinks then estimates the relative abundances of these transcripts based on how many reads support each one, taking into account biases in library preparation protocols. 

Cufflinks is a collaborative effort between the Laboratory for Mathematical and Computational Biology, led by Lior Pachter at UC Berkeley, Steven Salzberg's computational genomics group at the Institute of Genetic Medicine at Johns Hopkins University, and Barbara Wold's lab at Caltech. 


#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack tarball
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}-%{version}.Linux_x86_64

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include ../system-load.inc

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC

# Installing from source is so broken, I've resorted to using the binaries
# see version 2.0.X for a spec file that built from source

cp -r ./* $RPM_BUILD_ROOT%{INSTALL_DIR} 

#------------------------------------------------
# MODULE SECTION
#------------------------------------------------

# I keep both TACC_CUFFLINKS_DIR and TACC_CUFFLINKS_BIN for backward compatibility

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads the %{PNAME} software package.
Documentation for %{PNAME} is available online at the publisher website: http://cufflinks.cbcb.umd.edu/
The cufflinks executable can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, RNAseq, Transcriptome profiling")
whatis("Description: cufflinks - Transcript assembly, differential expression, and differential regulation for RNA-Seq")
whatis("URL: http://cufflinks.cbcb.umd.edu/")

prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}")

EOF

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

