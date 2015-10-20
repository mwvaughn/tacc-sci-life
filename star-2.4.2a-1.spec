Name:     STAR
Version:  2.4.2a
Release:  1
License:  GPL
Source:   https://github.com/alexdobin/STAR/archive/STAR_2.4.2a.tar.gz
URL:      https://github.com/alexdobin/STAR
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Spliced Transcripts Alignment to a Reference

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
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}STAR
%define PNAME       STAR

%package %{PACKAGE}
Summary: STAR - Spliced Transcripts Alignment to a Reference
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: STAR - Spliced Transcripts Alignment to a Reference
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
Paraphrasing from the STAR manual, the basic STAR workflow consists of 2 steps: (1) Generating genome indexes files. In this step user supplied the reference genome sequences (FASTA files) and annotations (GTF file), from which STAR generate genome indexes that are utilized in the 2nd (map-ping) step. The genome indexes are saved to disk and need only be generated once for each genome/annotation combination. (2) Mapping reads to the genome. In this step user supplies the genome files generated in the 1st step, as well as the RNA-seq reads (sequences) in the form of FASTA or FASTQ files. STAR maps the reads to the genome, and writes several output files, such as alignments (SAM/BAM), mapping summary statistics, splice junctions, unmapped reads, signal (wiggle) tracks etc.


## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif


## SETUP
# Run the setup macro - this removes old copies, then unpackages the program zip file
# from ~SOURCES into ~BUILD
%setup -n %{PNAME}-%{PNAME}_%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL 
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

#--------------------------------------
%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    ########### Do Not Remove #############

    ## Install Steps Start
    module purge
    module load TACC
    module swap intel gcc
    
    cd source/
    make STAR
    make STARlong

    # Copy the binaries
    mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
    cp -r ./STAR $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
    cp -r ./STARlong $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
%endif


#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------

%if %{?BUILD_MODULEFILE}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
    ########### Do Not Remove #############


#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} version %{version}
Documentation for %{PNAME} is available online at: https://github.com/alexdobin/STAR/

The executables can be found in %{MODULE_VAR}_DIR/bin/

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Genotyping, Resequencing, SNP")
whatis("Description: STAR - Spliced Transcripts Alignment to a Reference.")

whatis("URL: https://github.com/alexdobin/STAR/")

setenv("%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin/")
prepend_path("PATH", "%{INSTALL_DIR}/bin")

EOF
## Modulefile End
#--------------------------------------


    # Lua sytax check
    if [ -f $SPEC_DIR/checkModuleSyntax ]; then
        $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
    fi


#--------------------------------------
## VERSION FILE
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
## VERSION FILE END
#--------------------------------------


%endif

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
%defattr(-,root,install,)
%{INSTALL_DIR}
%endif # ?BUILD_PACKAGE

%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE}
%defattr(-,root,install,)
%{MODULE_DIR}
%endif # ?BUILD_MODULEFILE

## POST 
%post %{PACKAGE}
export PACKAGE_POST=1
%include include/post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include include/post-defines.inc

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

