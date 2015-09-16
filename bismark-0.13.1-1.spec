Name:       bismark
Version:    0.13.1
Release:    1
License:    GPLv3
Group: Applications/Life Sciences
Source:     http://www.bioinformatics.babraham.ac.uk/projects/bismark/bismark_v0.13.1.tar.gz
Packager:   TACC - jawon@tacc.utexas.edu
Summary:    bismark - A tool to map bisulfite converted sequence reads and determine cytosine methylation states
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
%define MODULE_VAR  %{MODULE_VAR_PREFIX}BISMARK
%define PNAME       bismark

## PACKAGE DESCRIPTION
%description
Bismark is a program to map bisulfite treated sequencing reads to a genome of interest and perform methylation calls in a single step. The output can be easily imported into a genome viewer, such as SeqMonk, and enables a researcher to analyse the methylation levels of their samples straight away.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
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


#------------------------------------------------
## Install Steps Start
module purge
module load TACC
echo "Bismark is a script. No need to compile it."

## Install Steps End
#------------------------------------------------

cp -R ./bismark ./bismark2report ./bismark_methylation_extractor  ./deduplicate_bismark ./bismark2bedGraph ./bismark_genome_preparation ./coverage2cytosine $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
This module loads %{name} This module makes available the bismark executable. Documentation for %{name} is available online at the publisher\'s website: http://www.bioinformatics.bbsrc.ac.uk/projects/bismark/
The bismark executables can be found in %{MODULE_VAR}_DIR, including "bismark_genome_preparation","bismark", "methylation_extractor".

Version %{version}
]])

whatis("Name: bismark")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Methylation, Epigenomics, Bisulfite, Sequencing")
whatis("Description: bismark - A tool to map bisulfite converted sequence reads and determine cytosine")
whatis("URL: http://www.bioinformatics.bbsrc.ac.uk/projects/bismark/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

prereq("bowtie")

EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPECS_DIR/checkModuleSyntax ]; then
    $SPECS_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
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
