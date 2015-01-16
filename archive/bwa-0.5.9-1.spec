Summary:    bwa - Burrows-Wheeler Alignment Tool
Name:       bwa
Version:    0.5.9
Release:    1
License:    GPLv3
Vendor:     Sanger Institute
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.bz2
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
%include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME bwa

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group:   Applications/Biology

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
BWA is a fast light-weighted tool that aligns relatively short sequences (queries) to a sequence database (targe), such as the human reference genome. It implements two different algorithms, both based on Burrows-Wheeler Transform (BWT). The first algorithm is designed for short queries up to ~200bp with low error rate (<3%). It does gapped global alignment w.r.t. queries, supports paired-end reads, and is one of the fastest short read alignment algorithms to date while also visiting suboptimal hits. The second algorithm, BWA-SW, is designed for long reads with more errors. It performs heuristic Smith-Waterman-like alignment to find high-scoring local hits (and thus chimera). On low-error short queries, BWA-SW is slower and less accurate than the first algorithm, but on long queries, it is better.

For both algorithms, the database file in the FASTA format must be first indexed with the ‘index’ command, which typically takes a few hours. The first algorithm is implemented via the ‘aln’ command, which finds the suffix array (SA) coordinates of good hits of each individual read, and the ‘samse/sampe’ command, which converts SA coordinates to chromosomal coordinate and pairs reads (for ‘sampe’). The second algorithm is invoked by the ‘bwasw’ command. It works for single-end reads only.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BWA

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/bwa-0.5.9
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
%include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)

#-----------------------------
# Build parallel version
#-----------------------------

make

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

 cp ./bwa $RPM_BUILD_ROOT/%{INSTALL_DIR}


# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with gcc.
This module makes available the bwa executable. Documentation for %{name} is available online at the publisher\'s website: http://bio-bwa.sourceforge.net/bwa.shtml
The bwa executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: bwa")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment")
whatis("Description: bwa - Burrows-Wheeler Alignment Tool")
whatis("URL: http://bio-bwa.sourceforge.net/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

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

