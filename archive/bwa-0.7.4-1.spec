Summary:    bwa - Burrows-Wheeler Alignment Tool
Name:       bwa
Version:    0.7.4
Release:    1
License:    GPLv3
Vendor:     Heng Li at the Sanger Institute
Group: Applications/Life Sciences
Source:     http://iweb.dl.sourceforge.net/project/bio-bwa/bwa-0.7.4.tar.bz2
Packager:   TACC - vaughn@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BWA

%description
BWA is a fast light-weighted tool that aligns relatively short sequences (queries) to a sequence database (targe), such as the human reference genome. It implements two different algorithms, both based on Burrows-Wheeler Transform (BWT). The first algorithm is designed for short queries up to ~200bp with low error rate (<3%). It does gapped global alignment w.r.t. queries, supports paired-end reads, and is one of the fastest short read alignment algorithms to date while also visiting suboptimal hits. The second algorithm, BWA-SW, is designed for long reads with more errors. It performs heuristic Smith-Waterman-like alignment to find high-scoring local hits (and thus chimera). On low-error short queries, BWA-SW is slower and less accurate than the first algorithm, but on long queries, it is better.

For both algorithms, the database file in the FASTA format must be first indexed with the ‘index’ command, which typically takes a few hours. The first algorithm is implemented via the ‘aln’ command, which finds the suffix array (SA) coordinates of good hits of each individual read, and the ‘samse/sampe’ command, which converts SA coordinates to chromosomal coordinate and pairs reads (for ‘sampe’). The second algorithm is invoked by the ‘bwasw’ command. It works for single-end reads only.

# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{name}-%{version}

##
## BUILD
##

%build

##
## INSTALL
##
%install

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# %include compiler-load.inc
# %include mpi-load.inc

#make CC=icc CXX=icpc
make

cp ./bwa *.pl $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing")
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
rm -rf $RPM_BUILD_ROOT