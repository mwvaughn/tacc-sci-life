Name: rsem
Version: 1.2.19
Release: 1
License: GPL
Group: Applications/Life Sciences
Source: http://deweylab.biostat.wisc.edu/rsem/src/%{name}-%{version}.tar.gz 
Packager: NAL - chien-yueh.lee@ars.usda.gov
Summary: RSEM is a software package for estimating gene and isoform expression levels from RNA-Seq data.
Prefix: /opt/apps

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}RSEM
%define PNAME       rsem

## PACKAGE DESCRIPTION
%description
RSEM is a software package for estimating gene and isoform expression levels from RNA-Seq data. The RSEM package provides an user-friendly interface, supports threads for parallel computation of the EM algorithm, single-end and paired-end read data, quality scores, variable-length reads and RSPD estimation. In addition, it provides posterior mean and 95% credibility interval estimates for expression levels. For visualization, It can generate BAM and Wiggle files in both transcript-coordinate and genomic-coordinate. Genomic-coordinate files can be visualized by both UCSC Genome browser and Broad Institute.s Integrative Genomics Viewer (IGV). Transcript-coordinate files can be visualized by IGV. RSEM also has its own scripts to generate transcript read depth plots in pdf format. The unique feature of RSEM is, the read depth plots can be stacked, with read depth contributed to unique reads shown in black and contributed to multi-reads shown in red. In addition, models learned from data can also be visualized. Last but not least, RSEM contains a simulator.
## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
module purge
module load gcc
module load R
module load perl
module load bowtie
module swap $TACC_FAMILY_COMPILER gcc

# Since LDFLAGS is not used in bowtie's compilation, we hijack EXTRA_FLAGS to carry the rpath payload
make
make ebseq 
## Install Steps End
#------------------------------------------------

cp -R ./rsem-* ./rsem_perl_utils.pm ./WHAT_IS_NEW ./EBSeq $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_EBSeq for the location of the %{name}
distribution. Documentation can be found online at http://deweylab.biostat.wisc.edu/rsem/README.html

Version %{version}

]])

whatis("Name: RSEM")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Transcriptome, Sequencing, RNA-Seq, Gene Expression")
whatis("URL: http://deweylab.biostat.wisc.edu/rsem/")
whatis("Description: RSEM is a software package for estimating gene and isoform expression levels from RNA-Seq data.")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_EBSEQ","%{INSTALL_DIR}/EBSeq")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

prereq("perl")
prereq("R")
prereq("bowtie")

EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
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

## CLEAN UP
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

