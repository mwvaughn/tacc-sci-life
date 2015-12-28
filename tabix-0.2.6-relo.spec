#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME tabix
Summary: Tabix - Indexes a tab-delimited genome position file in.tab.bgz and creates an index file
Version: 0.2.6
Release: 3
License: GPL
Group: Applications/Life Sciences
Source0:  tabix-%{version}.tar.bz2
Packager: TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}TABIX

## PACKAGE DESCRIPTION
%description
Indexes a tab-delimited genome position file in.tab.bgz and creates an index file.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include

#------------------------------------------------
## Install Steps Start

module swap $TACC_FAMILY_COMPILER gcc
make

cp -R perl/ python/ tabix tabix.py TabixReader.java bgzip NEWS $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_INC, and %{MODULE_VAR}_LIB
associated with %{PNAME}

Version %{version}
]]
)

whatis("Name: Tabix")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Quality Control, Utility, Sequencing, Genotyping, Resequencing, SNP")
whatis("URL: http://samtools.sourceforge.net/")
whatis("Description: Indexes a tab-delimited genome position file in.tab.bgz and creates an index file.")

prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

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
