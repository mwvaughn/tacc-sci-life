%define PNAME perl
Version: 5.22.1
Release: 1
Summary: PERL
License: GPL
Group: Applications/Life Sciences
Source: http://www.cpan.org/src/5.0/perl-5.22.1.tar.gz
URL: http://www.cpan.org
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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}PERL

## PACKAGE DESCRIPTION
%description
Perl built with intel.

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

if [ "%{PLATFORM}" != "ls5" ]
then
	module purge
	module load TACC
fi

ml gcc

sed -i 's/dbmclose();/dbmclose(db);/' ext/ODBM_File/ODBM_File.xs
./Configure -Dcc=gcc -Dusethreads -des -Doptimize='-O3 -march=sandybridge -mtune=haswell' -Dprefix=%{INSTALL_DIR} -Duserelocatableinc
#./Configure -Dusethreads -des -Dcc=icc -Dld=icc -Dcxx=icpc -Accflags='-gcc -fPIC' -Doptimize='-O3 -xAVX -axCORE-AVX2' -Dprefix=%{INSTALL_DIR}
make -j 4
#export LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH
make test
make install DESTDIR=$RPM_BUILD_ROOT

## Make Samtools
# prefix with install_dir
# install destdir to rpm_build_root

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
Insert help
The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution
	%{MODULE_VAR}_BIN - the location of the %{PNAME} binaries
	%{MODULE_VAR}_LIB - the location of the %{PNAME} libraries
	%{MODULE_VAR}_LIBEXEC - the location of the %{PNAME} libexec files
	%{MODULE_VAR}_SHARE - the location of the %{PNAME} man files

Documentation can be found online at %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: ")
whatis("URL: %{url}")
whatis("Description: ")

family("perl")
prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",   "%{INSTALL_DIR}/lib")
prepend_path("MANPATH",           "%{INSTALL_DIR}/man")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")
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
