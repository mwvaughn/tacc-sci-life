Name: plink
Summary: Whole genome association analysis toolset
Version: 1.07
Release: 3
License: GPLv2
Vendor: Shaun Purcell
Group: Applications/Life Sciences
Source: http://pngu.mgh.harvard.edu/~purcell/plink/dist/plink-1.07-src.zip
Packager: TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_PLINK
%define PNAME plink

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
PLINK is a free, open-source whole genome association analysis toolset, designed to perform a range of basic, large-scale analyses in a computationally efficient manner.

The focus of PLINK is purely on analysis of genotype/phenotype data, so there is no support for steps prior to this (e.g. study design and planning, generating genotype or CNV calls from raw data). Through integration with gPLINK and Haploview, there is some support for the subsequent visualization, annotation and storage of results.
PLINK (one syllable) is being developed by Shaun Purcell at the Center for Human Genetic Research (CHGR), Massachusetts General Hospital (MGH), and the Broad Institute of Harvard & MIT, with the support of others

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n %{name}-%{version}-src

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
module load $TACC_FAMILY_COMPILER intel

# The Makefile doesn't like overrides of CXXFLAGS needed to build with MKL
# so need to force all the macros like DUNIX, etc to be sent in
# Have not confirmed that plink is able to take advantage of the MKL linkage
make CC=icc CXX=icpc 'LIBS=-ldl' CXXFLAGS='-O3 -I. -DUNIX -DWITH_R_PLUGINS -DWITH_ZLIB -Wl,-rpath,${TACC_MKL_LIB} -L${TACC_MKL_LIB} -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread'

cp ./plink ./README.txt $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
This module loads %{name} built with icc.

This module makes available the plink executable.
Documentation is available online at the publisher's website:
http://pngu.mgh.harvard.edu/~purcell/plink/

The plink executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: plink")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing, Genetics, GWAS")
whatis("Description: plink - Whole genome association analysis toolset")
whatis("URL: http://pngu.mgh.harvard.edu/~purcell/plink/")

--- do not touch this lua code
local thisFile = myFileName()
local moduleName = myModuleFullName()
local  basePath = string.sub(thisFile,1,thisFile:find(moduleName,1,true)-2)
local appPath = pathJoin(string.gsub(basePath, "(.*/).*", "%1"),moduleName)
--- do not touch this lua code

setenv("%{MODULE_VAR}_DIR", appPath)
prepend_path("PATH"     , appPath)

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

# Define files permissions, user, and group
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
