Summary:    bismark - A tool to map bisulfite converted sequence reads and determine cytosine methylation states
Name:       bismark
Version:    0.10.1
Release:    1
License:    GPLv3
Group: Applications/Life Sciences
Source:     %{name}_v%{version}.tar.gz
Packager:   TACC - wonaya@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot
#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
%include ../rpm-dir.inc
%include ../system-defines.inc
%define PNAME bismark

# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Bismark is a program to map bisulfite treated sequencing reads to a genome of interest and perform methylation calls in a single step. The output can be easily imported into a genome viewer, such as SeqMonk, and enables a researcher to analyse the methylation levels of their samples straight away.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BISMARK

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}_v%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install


# Start with a clean environment
%include ../system-load.inc
# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc

module purge
module load TACC
#-----------------------------
# Build parallel version
#-----------------------------

echo "Bismark is a script. No need to compile it."

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} This module makes available the bismark executable. Documentation for %{name} is available online at the publisher\'s website: http://www.bioinformatics.bbsrc.ac.uk/projects/bismark/
The bismark executables can be found in %{MODULE_VAR}_DIR, including "bismark_genome_preparation","bismark", "methylation_extractor".

Version %{version}
]])

whatis("Name: bismark")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Methylation, Epigenomics, Bisulfite, Sequencing")
whatis("Description: bismark - A tool to map bisulfite converted sequence reads and determine cytosine")
whatis("URL: http://www.bioinformatics.bbsrc.ac.uk/projects/bismark/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

prereq ("bowtie")

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


