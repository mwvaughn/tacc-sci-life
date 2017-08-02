%define PNAME sparsehash
Version: 2.0.3.1
Release: 1
Summary: google-sparsehash library
License: GNU
Group: Applications/Life Sciences
Source: /work/03076/gzynda/rpmbuild/SOURCES/sparsehash-2.0.3.1.tar.gz
URL: https://github.com/sparsehash/sparsehash
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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}CHANGE

## PACKAGE DESCRIPTION
%description
An extremely memory-efficient hash_map implementation, with only 2 bits/entry of overhead. The SparseHash library has several C++ hash map implementations with different performance characteristics, including one that optimizes for memory use and another that optimizes for speed.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n %{PNAME}

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
	./configure CC=icc CXX=icpc CFLAGS="-O3 -xHOST" CXXFLAGS="-O3 -xHOST" --prefix=%{INSTALL_DIR}
else
	./configure CC=icc CXX=icpc CFLAGS="-O3 -xAVX -axCORE-AVX2" CXXFLAGS="-O3 -xAVX -axCORE-AVX2" --prefix=%{INSTALL_DIR}
fi

make -j4 DESTDIR=$RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution
	%{MODULE_VAR}_INC - the location of the %{PNAME} headers
		* prepended to CPATH
	%{MODULE_VAR}_LIB - the location of the %{PNAME} libraries
		* prepended to LD_LIBRARY_PATH
	%{MODULE_VAR}_SHARE - the location of the %{PNAME} doc files

Documentation can be found online at %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: library, hash table")
whatis("Keywords: google, sparsehash, hash, table")
whatis("URL: %{url}")
whatis("Description: ")

prepend_path("LD_LIBRARY_PATH",              "%{INSTALL_DIR}/lib")
prepend_path("CPATH",              "%{INSTALL_DIR}/include")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_INC", "%{INSTALL_DIR}/include")
setenv (     "%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")
setenv (     "%{MODULE_VAR}_SHARE", "%{INSTALL_DIR}/share")
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
