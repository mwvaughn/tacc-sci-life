#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME star
Version:  2.5.0a
Release:  1
License:  GPL
Group:    Applications/Life Sciences
Source:   https://github.com/alexdobin/STAR/archive/STAR_2.5.0a.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Spliced Transcripts Alignment to a Reference

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}STAR

## PACKAGE DESCRIPTION
%description
Paraphrasing from the STAR manual, the basic STAR workflow consists of 2 steps: (1) Generating genome indexes files. In this step user supplied the reference genome sequences (FASTA files) and annotations (GTF file), from which STAR generate genome indexes that are utilized in the 2nd (map-ping) step. The genome indexes are saved to disk and need only be generated once for each genome/annotation combination. (2) Mapping reads to the genome. In this step user supplies the genome files generated in the 1st step, as well as the RNA-seq reads (sequences) in the form of FASTA or FASTQ files. STAR maps the reads to the genome, and writes several output files, such as alignments (SAM/BAM), mapping summary statistics, splice junctions, unmapped reads, signal (wiggle) tracks etc.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%setup -n STAR-STAR_%{version}

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
module purge
module load TACC

%if "%{PLATFORM}" == "stampede"
    module swap $TACC_FAMILY_COMPILER gcc/4.9.1
%endif

%if "%{PLATFORM}" == "wrangler"
    module swap $TACC_FAMILY_COMPILER gcc/4.9.1
%endif

%if "%{PLATFORM}" == "ls5"
    module swap $TACC_FAMILY_COMPILER gcc/5.2.0
    export CFLAGS="-march=sandybridge -mtune=haswell"
    export LDFLAGS="-march=sandybridge -mtune=haswell"
%endif

export CC=`which gcc`
export CXX=`which g++`

cd source/
make STAR
make STARlong

# Copy the binaries
mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp ./STAR $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
cp ./STARlong $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
cp -r ../extras/ $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

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

prepend_path("PATH", "%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin/")
setenv("%{MODULE_VAR}_EXTRAS", "%{INSTALL_DIR}/extras/")

EOF

%if "%{PLATFORM}" == "stampede"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("gcc/4.9.1")
EOF
%endif

%if "%{PLATFORM}" == "wrangler"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("gcc/4.9.1")
EOF
%endif

%if "%{PLATFORM}" == "ls5"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("gcc/5.2.0")
EOF
%endif


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

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
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



# In SPECS dir:
# ./build_rpm.sh --gcc=49 star-2.5.0a-1.spec
# ./build_rpm.sh --gcc=52 star-2.5.0a-1.spec
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

