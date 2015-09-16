Name:     fastqc
Version:  0.11.3
Release:  1
License:  GPL
Source:   http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.3.zip
URL:      http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
Packager: TACC - jawon@tacc.utexas.edu
Summary:  FastQC - A quality control application for high throughput sequence data

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}FASTQC
%define PNAME       fastqc

%package %{PACKAGE}
Summary: A quality control application for high throughput sequence data
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: A quality control application for high throughput sequence data
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
FastQC is an application which takes a FastQ file and runs a series of tests on it to generate a comprehensive QC report.

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
%setup -n FastQC 

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
    module swap $TACC_FAMILY_COMPILER intel 
    
    # The objective of this section is to install the compiled software into a virtual
    # directory structure so that it can be packaged up into an RPM
    #
    # install is also a macro that does many things, including creating appropriate
    # directories in $RPM_BUILD_ROOT and cd to the right place
    
    mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
    
    cp -R ./Help ./uk ./Templates ./fastqc ./*.txt ./*.jar $RPM_BUILD_ROOT/%{INSTALL_DIR}

%endif


#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
# Clean up the old module directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

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
This module loads %{PNAME} built with %{comp_fam}.
Documentation for %{PNAME} is available online at http://www.bioinformatics.babraham.ac.uk/projects/fastqc
The executables are added on to path

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, FastQ, Quality Control")
whatis("Description: fastqc - A Quality Control application for FastQ files")
whatis("URL: http://www.bioinformatics.babraham.ac.uk/projects/fastqc")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

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
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}
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

