# $Id$

Summary:    cufflinks - Transcript assembly, differential expression, and differential regulation for RNA-Seq
Name:       cufflinks
Version:    2.0.2
Release:    2
License:    Boost Software License
Group: Applications/Life Sciences
Source:     cufflinks-%{version}.tar.gz
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot
requires:   boost-gcc4_6 = 1.51.0

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
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}-%{version}

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

# looks like the install is broken for new versions of gcc
%if "%{PLATFORM}" == "lonestar"
  module swap $TACC_FAMILY_COMPILER gcc/4.7.1
%endif

%if "%{PLATFORM}" == "stampede"
  module swap $TACC_FAMILY_COMPILER gcc/4.6.3
%endif
# boost is in the required section at the top of the spec file
module load boost/1.51.0
module load cmake

export CUFFLINKS_DIR=`pwd`
# apparently I'm getting lazy in my old age.  I'm just using wget for the Eigen sourcecode
wget http://bitbucket.org/eigen/eigen/get/3.1.0.tar.gz
tar xvzf 3.1.0.tar.gz 
rm ./3.1.0.tar.gz
cd eigen*
export EIGEN_SRC=`pwd`
mkdir build
cd build

#building with gcc to be consistent with cufflinks
CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX=$CUFFLINKS_DIR/eigen
make install
#have to move eigen out of the Eigen3 dir
mv $CUFFLINKS_DIR/eigen/include/eigen3/* $CUFFLINKS_DIR/eigen/include/
rmdir $CUFFLINKS_DIR/eigen/include/eigen3

cd $CUFFLINKS_DIR

# aha, after several frustrating hours, I think they screwed up how they link to samtools include files.  They insert an extra "bam" directory when calling the headers... idiots.
wget http://downloads.sourceforge.net/project/samtools/samtools/0.1.18/samtools-0.1.18.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fsamtools%2Ffiles%2Fsamtools%2F0.1.18%2F
tar xjf samtools*
cd samtools*
MY_SAMTOOLS_DIR=$PWD
make
mkdir -p ./include/bam
cp ./*.h ./include/bam

cd $CUFFLINKS_DIR

#%if "%{PLATFORM}" == "lonestar"
  ./configure CC=gcc CXX=g++ --prefix=%{INSTALL_DIR} --with-boost=$TACC_BOOST_DIR --with-eigen=$CUFFLINKS_DIR/eigen --with-bam=$MY_SAMTOOLS_DIR --with-bam-libdir=$MY_SAMTOOLS_DIR LDFLAGS="-Wl,-rpath,$TACC_BOOST_LIB,-rpath,$GCC_LIB -L$TACC_BOOST_LIB -lboost_system"
#%endif

#%if "%{PLATFORM}" == "stampede"
#  ./configure CC=gcc CXX=g++ --prefix=%{INSTALL_DIR} --with-boost=$TACC_BOOST_DIR --with-eigen=$CUFFLINKS_DIR/eigen --with-bam=$MY_SAMTOOLS_DIR --with-bam-libdir=$MY_SAMTOOLS_DIR LDFLAGS="-Wl,-rpath,$TACC_BOOST_LIB"
#%endif

# Patch to fix error
# common.h:25:25: error: 'boost::BOOST_FOREACH' has not been declared

cd $CUFFLINKS_DIR/src && mv common.h common.h.prot && for x in *.cpp *.h; do sed 's/foreach/for_each/' $x > x; mv x $x; done && mv common.h.prot common.h && cd $CUFFLINKS_DIR

cd $CUFFLINKS_DIR
make
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install
cp -r LICENSE README AUTHORS ./eigen $MY_SAMTOOLS_DIR $RPM_BUILD_ROOT%{INSTALL_DIR} 

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with gcc.
This module makes available the cufflinks executable. Documentation for %{name} is available online at the publisher website: http://cufflinks.cbcb.umd.edu/
The cufflinks executable can be found in %{MODULE_VAR}_BIN

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

