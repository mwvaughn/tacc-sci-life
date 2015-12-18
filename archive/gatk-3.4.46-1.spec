Name:     gatk
Version:  3.4.46
Release:  1
License:  Broad Institute Software License Agreement
Source:   GenomeAnalysisTK-3.4-46.tar.bz2
URL:      https://www.broadinstitute.org/gatk/download/
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Structure-based small molecule docking program

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}GATK
%define PNAME       gatk

%package %{PACKAGE}
Summary: GATK - Genome Analysis Toolkit
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: GATK - Genome Analysis Toolkit
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
The Genome Analysis Toolkit or GATK is a software package developed at the Broad Institute to analyze high-throughput sequencing data. The toolkit offers a wide variety of tools, with a primary focus on variant discovery and genotyping as well as strong emphasis on data quality assurance. Its robust architecture, powerful processing engine and high-performance computing features make it capable of taking on projects of any size.


## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif

# do this so GATK has somewhere to unpack
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
# Run the setup macro - this removes old copies, then unpackages the program zip file
# from ~SOURCES into ~BUILD
# the -c option creates a dir and changes to it before unpacking
%setup -c

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
    
    # GATK is pre-compiled, no install necessary
    
    # Copy the binaries
    cp -r ./resources/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    cp -r GenomeAnalysisTK.jar $RPM_BUILD_ROOT/%{INSTALL_DIR}/
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
Documentation for %{PNAME} is available online at: https://www.broadinstitute.org/gatk/download/

The executables can be found in %{MODULE_VAR}_DIR
Resources, including test files, can be found in %{MODULE_VAR}_RESOURCES

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Genotyping, Resequencing, SNP")
whatis("Description: The Genome Analysis Toolkit or GATK is a software package developed at the Broad Institute to analyze high-throughput sequencing data.")

whatis("URL: https://www.broadinstitute.org/gatk/download/")

setenv("%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_RESOURCES", "%{INSTALL_DIR}/resources/")
prepend_path("PATH", "%{INSTALL_DIR}")

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

