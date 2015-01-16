# $Id$

Summary:    cufflinks - Transcript assembly, differential expression, and differential regulation for RNA-Seq
Name:       cufflinks
Version:    2.0.1
Release:    1
License:    Boost Software License
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot
requires:   boost-intel11_1 = 1.49.0


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME cufflinks

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Cufflinks assembles transcripts, estimates their abundances, and tests for differential expression and regulation in RNA-Seq samples. It accepts aligned RNA-Seq reads and assembles the alignments into a parsimonious set of transcripts. Cufflinks then estimates the relative abundances of these transcripts based on how many reads support each one, taking into account biases in library preparation protocols. 

Cufflinks is a collaborative effort between the Laboratory for Mathematical and Computational Biology, led by Lior Pachter at UC Berkeley, Steven Salzberg's computational genomics group at the Institute of Genetic Medicine at Johns Hopkins University, and Barbara Wold's lab at Caltech. 

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_CUFFLINKS

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
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)
module purge
module load TACC
module swap $TACC_FAMILY_COMPILER intel

# boost is in the required section at the top of the spec file
module load boost/1.49.0
module load samtools

#-----------------------------
# Build parallel version
#-----------------------------

./configure CC=icc CXX=icpc --prefix=%{INSTALL_DIR} --with-boost=$TACC_BOOST_DIR --with-bam=$TACC_SAMTOOLS_DIR LDFLAGS="-Wl,-rpath,$TACC_BOOST_LIB"
make CC=icc CXX=icpc

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with icc.
This module makes available the cufflinks executable. Documentation for %{name} is available online at the publisher\'s website: http://cufflinks.cbcb.umd.edu/
The cufflinks executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: cufflinks")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, RNAseq, Transcriptome profiling")
whatis("Description: cufflinks - Transcript assembly, differential expression, and differential regulation for RNA-Seq")
whatis("URL: http://cufflinks.cbcb.umd.edu/")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

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

