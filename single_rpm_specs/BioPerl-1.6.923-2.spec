%define PNAME bioperl
Version: 1.6.923
Release: 2
Summary: BioPerl is a toolkit of perl modules useful in bioinformatics solutions in Perl.
License: GPL
Group: Libraries/Life Sciences
Source0: http://search.cpan.org/CPAN/authors/id/C/CJ/CJFIELDS/BioPerl-1.6.923.tar.gz
Source1: /work/03076/gzynda/rpmbuild/SOURCES/db-6.1.26.NC.gz
URL: http://www.bioperl.org/wiki/Main_Page
Packager: TACC - gzynda@tacc.utexas.edu

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}BIOPERL

## PACKAGE DESCRIPTION
%description
BioPerl is a community effort to produce Perl code which is useful in biology.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n BioPerl-%{version} -a 1

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

if [ "%{PLATFORM}" != "ls5" ]
then
	module purge
	module load TACC
fi

module load perl

# Make sure to use cpan to install the build requirements beforehand
#cpan -i CPAN Module::Build Test::Harness Test::Most URI::Escape

# make Berkeley DB
cd db-6.1.26.NC/build_unix
../dist/configure --prefix=%{INSTALL_DIR}
make -j 4 DESTDIR=${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
cd ../../

# make BioPerl
BRID=${RPM_BUILD_ROOT}/%{INSTALL_DIR}
PATH="$BRID/bin${PATH+:}${PATH}"
PERL5LIB="$BRID/lib/perl5${PERL5LIB+:}/home1/03076/gzynda/perl5/lib/perl5${PERL5LIB+:}${PERL5LIB}"
PERL_LOCAL_LIB_ROOT="${BRID}{PERL_LOCAL_LIB_ROOT+:}${PERL_LOCAL_LIB_ROOT}"
PERL_MB_OPT="--install_base $BRID"
PERL_MM_OPT="INSTALL_BASE=$BRID"
export PERL_MB_OPT
export PERL_MM_OPT

DB_FILE_LIB=${BRID}/lib; export DB_FILE_LIB;
DB_FILE_INCLUDE=${BRID}/include; export DB_FILE_INCLUDE;

cpan -i IO::String DB_File Data::Stag Scalar::Util ExtUtils::Manifest
perl Build.PL --install_base $BRID
#./Build test
./Build install
#Build installdeps

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
BioPerl provides software modules for many of the typical tasks of bioinformatics programming. These include:
 * Accessing nucleotide and peptide sequence data from local and remote databases
 * Transforming formats of database/ file records
 * Manipulating individual sequences
 * Searching for similar sequences
 * Creating and manipulating sequence alignments
 * Searching for genes and other structures on genomic DNA
 * Developing machine readable sequence annotations

The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution
	%{MODULE_VAR}_BIN - the location of the %{PNAME} binaries
	%{MODULE_VAR}_LIB - the location of the %{PNAME} libraries
	%{MODULE_VAR}_INC - the location of the %{PNAME} headers

Documentation can be found online at %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics, library")
whatis("Keywords: genomics, bioinformatics, genomics")
whatis("URL: %{url}")
whatis("Description: %{summary}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",		"%{INSTALL_DIR}/man")
prepend_path("PERL5LIB",	"%{INSTALL_DIR}/lib/perl5")

setenv(     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv(     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv(     "%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")
setenv(     "%{MODULE_VAR}_INC", "%{INSTALL_DIR}/include")

always_load("perl")
EOF

## Module File End
#--------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
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
