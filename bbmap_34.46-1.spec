Name:       bbmap
Summary:    BBMap short read aligner, and other bioinformatic tools
Version:    34.46
Release:    1
License:    Free for non-commercial use.. Contact the author for more information
Vendor:     Brian Bushnell (LBL, JGI) 
Group:      Applications/Life Sciences
Source:     http://downloads.sourceforge.net/project/bbmap/BBMap_34.46.tar.gz
Packager:   ARS - christopher.childers@ars.usda.gov
Prefix:     /opt/apps

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}BBMAP
%define PNAME       bbmap

## PACKAGE DESCRIPTION
%description
This package includes BBMap, a short read aligner, as well as various other bioinformatic tools. It is written in pure Java, can run on any platform, and has no dependencies other than Java being installed (compiled for Java 6 and higher). All tools are efficient and multithreaded. BBMap: Short read aligner for DNA and RNA-seq data. Capable of handling arbitrarily large genomes with millions of scaffolds. Handles Illumina, PacBio, 454, and other reads; very high sensitivity and tolerant of errors and numerous large indels. Very fast. BBNorm: Kmer-based error-correction and normalization tool. Dedupe: Simplifies assemblies by removing duplicate or contained subsequences that share a target percent identity. Reformat: Reformats reads between fasta/fastq/scarf/fasta+qual/sam, interleaved/paired, and ASCII-33/64, at over 500 MB/s. BBDuk: Filters, trims, or masks reads with kmer matches to an artifact/contaminant file. ...and more! 

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n %{PNAME}

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
module load TACC 

echo "BBmap is distributed as compiled Java. No compilation necessary."



## Install Steps End
#------------------------------------------------
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp ./bbmap *.pl $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
Documentation can be found online at http://sourceforge.net/projects/bbmap/
The bbmap executable can be found in %{MODULE_VAR}_DIR

Version %{version}

]])

whatis("Name: BBMap")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing")
whatis("Description: BBMap short read aligner, and other bioinformatic tools")
whatis("URL: http://sourceforge.net/projects/bbmap/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

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
