%define PNAME bismark
Summary:    Bismark methylation mapper
Version: 0.14.5
License:    GPL
URL:        http://www.bioinformatics.babraham.ac.uk/projects/bismark/
Packager:   TACC - jawon@tacc.utexas.edu
Source:     http://www.bioinformatics.babraham.ac.uk/projects/bismark/bismark_v0.14.5.tar.gz
Vendor:     Babraham Institute
Group: Applications/Life Sciences
Release:   1

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}BISMARK

## PACKAGE DESCRIPTION
%description
Bismark is a program to map bisulfite treated sequencing reads to a genome of interest and perform methylation calls in a single step. The output can be easily imported into a genome viewer, such as SeqMonk, and enables a researcher to analyse the methylation levels of their samples straight away.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n %{PNAME}_v%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#--------------------------------------
## Install Steps Start

echo "%{PNAME} is being packaged from a vendor-supplied binary distribution"

## Install Steps End
#--------------------------------------

cp -R ./bismark ./bismark2report ./bismark_methylation_extractor  ./deduplicate_bismark ./bismark2bedGraph ./bismark_genome_preparation ./coverage2cytosine $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} This module makes available the bismark executable. Documentation for %{PNAME} is available online at the publisher's website: http://www.bioinformatics.bbsrc.ac.uk/projects/bismark/
The bismark executables can be found in %{MODULE_VAR}_DIR, including "bismark_genome_preparation","bismark", "methylation_extractor".

Version %{version}

]])

whatis("Name: bismark")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Methylation, Epigenomics, Bisulfite, Sequencing")
whatis("Description: bismark - A tool to map bisulfite converted sequence reads and determine cytosine")
whatis("URL: http://www.bioinformatics.bbsrc.ac.uk/projects/bismark/")

local bismark_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR", bismark_dir)

prepend_path("PATH",		pathJoin(bismark_dir,""))

EOF
## Modulefile End
#--------------------------------------

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
