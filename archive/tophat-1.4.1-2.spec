# $Id$

# Edited SeqAn-1.2/seqan/platform.h and repackaged as tophat-1.4.1.patched.tar.gz
# Back out the edits, package using GCC and make available under gcc4_4 only

Summary: TopHat - fast splice junction mapper for RNA-Seq reads
Name: tophat
Version: 1.4.1
Release: 2
License: GPLv2
Group: Applications/Life Sciences
Source:  %{name}-%{version}.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu
#BuildRoot: /var/tmp/%{name}_%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# %define debug-package %{nil}
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
#%package -n %{name}-%{comp_fam_ver}
#Group: Applications/Life Sciences
#Summary: Fast splice junction mapper for RNA-Seq reads

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------

%description
#%description -n %{name}-%{comp_fam_ver}
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

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version}

%build

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi


module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc/4.4.5

# SAMtools first
export TOPHAT_DIR=`pwd`

# aha, after several frustrating hours, I think they screwed up how they link to samtools include files.  They insert an extra "bam" directory when calling the headers... idiots.
wget http://downloads.sourceforge.net/project/samtools/samtools/0.1.18/samtools-0.1.18.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fsamtools%2Ffiles%2Fsamtools%2F0.1.18%2F
tar xjf samtools*
cd samtools*
MY_SAMTOOLS_DIR=$PWD
make
mkdir -p ./include/bam
cp ./*.h ./include/bam

cd $TOPHAT_DIR

# Since LDFLAGS is not used in compilation, we hijack BAM_LDFLAGS to carry the rpath payload
./configure --prefix=%{INSTALL_DIR} --with-bam=$MY_SAMTOOLS_DIR --with-bam-libdir=$MY_SAMTOOLS_DIR
make BAM_LDFLAGS="-L$MY_SAMTOOLS_DIR -Wl,-rpath,/opt/apps/gcc/4.4.5/lib64/"

%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
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

whatis("Name: TopHat")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, RNAseq, Transcriptome profiling, Alignment")
whatis("URL: http://tophat.cbcb.umd.edu/")
whatis("Description: TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
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
# %files -n %{name}-%{comp_fam_ver}
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

