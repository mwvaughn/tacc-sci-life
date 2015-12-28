#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME fastqc
Summary: FastQC - A quality control application for high throughput sequence data
Version:  0.10.1
Release:   3
Group:	Applications/Life Sceinces
License:  GPL
Source:  http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.10.1.zip
Packager:   TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}FASTQC

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
FastQC is an application which takes a FastQ file and runs a series
of tests on it to generate a comprehensive QC report.  This will
tell you if there is anything unusual about your sequence.  Each
test is flagged as a pass, warning or fail depending on how far it
departs from what you'd expect from a normal large dataset with no
significant biases.  It's important to stress that warnings or even
failures do not necessarily mean that there is a problem with your
data, only that it is unusual.  It is possible that the biological
nature of your sample means that you would expect this particular
bias in your results.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n FastQC

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

cp -R ./Help ./Contaminants ./uk ./Templates ./fastqc ./*bat ./*.txt ./*.jar $RPM_BUILD_ROOT/%{INSTALL_DIR}

## Install Steps End
#------------------------------------------------

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This is module %{PNAME}. Documentation is available online at the publisher\'s website: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
Executables can be found in %{MODULE_VAR}_DIR, including "fastqc".

Version %{version}
]])

whatis("Name: FastQC")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Sequencing, FastQ, Quality Control")
whatis("Description: fastqc - A Quality Control application for FastQ files")
whatis("URL: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/")
prepend_path("PATH",    "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")

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
