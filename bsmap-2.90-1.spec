%define	PNAME	bsmap
Version:   2.90p1
Summary:   BSMAP for Methylation
Release:   1
License:   GPL
Vendor:    Brown University
Group:     Applications/Life Sciences
Source:    %{PNAME}-%{version}.tar.gz
Packager:  TACC - gzynda@tacc.utexas.edu

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
#%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}BSMAP

## PACKAGE DESCRIPTION
%description
BSMAP is a short reads mapping program for bisulfite sequencing in DNA methylation study.  Bisulfite treatment coupled with next generation sequencing could estimate the methylation ratio of every single Cytosine location in the genome by mapping high throughput bisulfite reads to the reference sequences.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{name}-%{version}

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
if [ "%{PLATFORM}" != "ls5" ]
then
	module purge
	module load TACC
fi

[ -d BSMAP ] && rm -rf BSMAP
git clone https://github.com/zyndagj/BSMAP.git
cd BSMAP
git checkout 3a6715a7cf9bd9b664c13c41a04d3bf5446676d2

sed -i "s/-march=native/-xAVX -axCORE-AVX2/g" Makefile

# Make and install
make -j 2 CC=icc CXX=icpc
make BIN=${RPM_BUILD_ROOT}/%{INSTALL_DIR} install

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
Documentation for %{PNAME} is available online at the publisher website: https://code.google.com/p/bsmap/

For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include %{PNAME}.

Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics, methylation, aligner")
whatis("Keywords: Biology, Genomics, Mapping")
whatis("Description: BSMAP - short reads mapping software for bisulfite sequencing reads")
whatis("URL: https://code.google.com/p/bsmap/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
prepend_path("PATH"       ,"%{INSTALL_DIR}")
prereq("samtools","python")
EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# VERSON FILE
#------------------------------------------------
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
%files 
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}
#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
