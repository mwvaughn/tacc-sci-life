#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME tophat
Summary: Fast splice junction mapper for RNA-Seq reads.
Version: 2.0.9
Release: 3
License: GPLv2
Group: Applications/Life Sciences
Source:  http://tophat.cbcb.umd.edu/downloads/%{PNAME}-%{version}.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu
#Prefix: /opt/apps

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}TOPHAT

## PACKAGE DESCRIPTION
%description
TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons.

#------------------------------------------------

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

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

module swap $TACC_FAMILY_COMPILER gcc
module load boost

# Build SAMtools first
export TOPHAT_DIR=$(pwd)
wget http://downloads.sourceforge.net/project/samtools/samtools/0.1.19/samtools-0.1.19.tar.bz2
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

## Install Steps End
#------------------------------------------------

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
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

## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

## VERSION FILE
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
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}

## POST
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
