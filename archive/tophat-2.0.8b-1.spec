# $Id$

# Source
# http://tophat.cbcb.umd.edu/downloads/tophat-2.0.6.tar.gz

Summary: Fast splice junction mapper for RNA-Seq reads.
Name: tophat
Version: 2.0.8b
Release: 1
License: GPLv2
Group: Applications/Life Sciences
Source:  %{name}-%{version}.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu
#BuildRoot: /var/tmp/%{name}_%{version}-buildroot
#requires:   boost-gcc4_7 = 1.51.0

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
%define PNAME %{name}

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
# %description -n %{name}-%{comp_fam_ver}
TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons. 

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here

#%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
#%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%define MODULE_VAR TACC_TOPHAT

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------

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

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc
module load boost

# Build SAMtools first
export TOPHAT_DIR=`pwd`
wget http://downloads.sourceforge.net/project/samtools/samtools/0.1.18/samtools-0.1.18.tar.bz2
tar xjf samtools*
cd samtools*
MY_SAMTOOLS_DIR=$PWD
make
mkdir -p ./include/bam
cp ./*.h ./include/bam

cd $TOPHAT_DIR

./configure  --prefix=%{INSTALL_DIR} --enable-intel64 --with-boost=$TACC_BOOST_DIR --with-bam=$MY_SAMTOOLS_DIR --with-bam-libdir=$MY_SAMTOOLS_DIR LDFLAGS="-Wl,-rpath,$TACC_BOOST_LIB,-rpath,$GCC_LIB"

make BOOST_LDFLAGS="-L$TACC_BOOST_LIB -Wl,-rpath,$TACC_BOOST_LIB,-rpath,$GCC_LIB"

make DESTDIR=$RPM_BUILD_ROOT install

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_BIN for the location of the %{PNAME}
distribution.

Version %{version}
]]
)

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, RNAseq, Transcriptome profiling, Alignment")
whatis("URL: http://tophat.cbcb.umd.edu/")
whatis("Description: TopHat2 is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons.")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

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
#%files -n %{name}-%{comp_fam_ver}
%files 

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

