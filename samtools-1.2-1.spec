# $Id$

Name: samtools
Version: 1.2
Release: 1
Summary: Utilities for manipulating alignments in the SAM format.
License: GPL
Group: Applications/Life Sciences
Source:  http://downloads.sourceforge.net/project/samtools/samtools/1.2/samtools-1.2.tar.bz2
Packager: TACC - vaughn@tacc.utexas.edu, jfonner@tacc.utexas.edu

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
%define MODULE_VAR  %{MODULE_VAR_PREFIX}SAMTOOLS
%define PNAME       samtools

## PACKAGE DESCRIPTION
%description
Samtools is a set of utilities that manipulate alignments in the BAM format. It imports from and exports to the SAM (Sequence Alignment/Map) format, does sorting, merging and indexing, and allows to retrieve reads in any regions swiftly.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

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

#------------------------------------------------
## Install Steps Start
module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc

make
make prefix=%{INSTALL_DIR} DESTDIR=$RPM_BUILD_ROOT install
## Install Steps End
#------------------------------------------------

# cp -R ./samtools ./bcftools ./misc ./examples $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p         $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
cp -R ./libbam.a $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
mkdir -p  $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
cp -R *.h $RPM_BUILD_ROOT/%{INSTALL_DIR}/include

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{name} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_INC, and %{MODULE_VAR}_LIB
associated with %{name}

Version %{version}
]])

whatis("Name: samtools")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing, Genotyping, Resequencing, SNP")
whatis("URL: http://samtools.sourceforge.net/")
whatis("Description: SAM Tools provide various utilities for manipulating alignments in the SAM format, including sorting, merging, indexing and generating alignments in a per-position format.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("PATH",              "%{INSTALL_DIR}/bcftools")
prepend_path("PATH",              "%{INSTALL_DIR}/misc")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_INC", "%{INSTALL_DIR}/include")
setenv (     "%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")

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
## version file for %{name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files

# Define files permissions, user, and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

## CLEAN UP
%post
%clean
rm -rf $RPM_BUILD_ROOT

