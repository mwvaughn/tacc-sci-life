#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME rsem
Summary: Accurate quantification of gene and isoform expression from RNA-Seq data
Version: 1.2.20
Release: 1
License: GPLv3
Group: Applications/Life Sciences
# curl -skL -o rsem-v1.2.20.tar.gz https://github.com/deweylab/RSEM/archive/v1.2.20.tar.gz
Source:  rsem-v1.2.20.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}RSEM

## PACKAGE DESCRIPTION
%description
RSEM is a software package for estimating gene and isoform expression levels from RNA-Seq data. The RSEM package provides an user-friendly interface, supports threads for parallel computation of the EM algorithm, single-end and paired-end read data, quality scores, variable-length reads and RSPD estimation. In addition, it provides posterior mean and 95% credibility interval estimates for expression levels. For visualization, It can generate BAM and Wiggle files in both transcript-coordinate and genomic-coordinate. Genomic-coordinate files can be visualized by both UCSC Genome browser and Broad Institute's Integrative Genomics Viewer (IGV). Transcript-coordinate files can be visualized by IGV. RSEM also has its own scripts to generate transcript read depth plots in pdf format. The unique feature of RSEM is, the read depth plots can be stacked, with read depth contributed to unique reads shown in black and contributed to multi-reads shown in red. In addition, models learned from data can also be visualized. Last but not least, RSEM contains a simulator.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n RSEM-%{version}

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
make
# Cannot currently build on intel11
# make ebseq

# Executables
for E in rsem-* convert-sam-for-rsem extract-transcript-to-gene-map-from-trinity
do
    cp -R $E $RPM_BUILD_ROOT/%{INSTALL_DIR}
done

# Libraries
for L in rsem_perl_utils.pm
do
    cp -R $L $RPM_BUILD_ROOT/%{INSTALL_DIR}
done

# Documentation
for D in WHAT_IS_NEW README.md model_file_description.txt cnt_file_description.txt
do
    cp -R $D $RPM_BUILD_ROOT/%{INSTALL_DIR}
done

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the environment variable %{MODULE_VAR}_DIR.

Version %{version}
]]
)

whatis("Name: RSEM")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Transcriptome, Isoform, RNAseq")
whatis("URL: http://deweylab.github.io/RSEM/")
whatis("Description: A software package for estimating gene and isoform expression levels from RNA-Seq data.")

prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

prereq("perl/5.14")
prereq("Rstats/3.0.2")
prereq("bowtie/2.2.3")

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
