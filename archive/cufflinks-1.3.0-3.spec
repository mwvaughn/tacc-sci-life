# $Id$

Summary:    Transcript assembly, differential expression, and differential regulation for RNA-Seq
Name:       cufflinks
Version:    1.3.0
Release:    3
License:    Boost Software License
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
requires:   boost-gcc4_4 = 1.45.0

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
%define PNAME %{name}

# Compiler-specific packages
# %package -n %{name}-%{comp_fam_ver}
# Group: Applications/Life Sciences
# Summary: Transcript assembly, differential expression, and differential regulation for RNA-Seq

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
# %description -n %{name}-%{comp_fam_ver}
Cufflinks assembles transcripts, estimates their abundances, and tests for differential expression and regulation in RNA-Seq samples. It accepts aligned RNA-Seq reads and assembles the alignments into a parsimonious set of transcripts. Cufflinks then estimates the relative abundances of these transcripts based on how many reads support each one, taking into account biases in library preparation protocols. 

Cufflinks is a collaborative effort between the Laboratory for Mathematical and Computational Biology, led by Lior Pachter at UC Berkeley, Steven Salzberg's computational genomics group at the Institute of Genetic Medicine at Johns Hopkins University, and Barbara Wold's lab at Caltech. 

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
#%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
#%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
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

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc/4.4.5
# boost is in the required section at the top of the spec file
module load boost/1.45.0

#-----------------------------
# Build parallel version
#-----------------------------

export CUFFLINKS_DIR=`pwd`

# aha, after several frustrating hours, I think they screwed up how they link to samtools include files.  They insert an extra "bam" directory when calling the headers... idiots.
wget http://downloads.sourceforge.net/project/samtools/samtools/0.1.18/samtools-0.1.18.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fsamtools%2Ffiles%2Fsamtools%2F0.1.18%2F
tar xjf samtools*
cd samtools*
MY_SAMTOOLS_DIR=$PWD
make
mkdir -p ./include/bam
cp ./*.h ./include/bam

cd $CUFFLINKS_DIR

./configure CC=gcc CXX=g++ --prefix=%{INSTALL_DIR} --with-boost=$TACC_BOOST_DIR --with-bam=$MY_SAMTOOLS_DIR --with-bam-libdir=$MY_SAMTOOLS_DIR LDFLAGS="-Wl,-rpath,$TACC_BOOST_LIB,-rpath,/opt/apps/gcc/4.4.5/lib64/"

# Since LDFLAGS is not used in compilation, we hijack BOOST_LDFLAGS to carry the rpath payload
make BOOST_LDFLAGS="-L$TACC_BOOST_LIB -Wl,-rpath,$TACC_BOOST_LIB,-rpath,/opt/apps/gcc/4.4.5/lib64/"

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install
cp -r LICENSE README AUTHORS $MY_SAMTOOLS_DIR $RPM_BUILD_ROOT%{INSTALL_DIR} 

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
whatis("Description: Transcript assembly, differential expression, and differential regulation for RNA-Seq")
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
# %files -n %{name}-%{comp_fam_ver}

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

