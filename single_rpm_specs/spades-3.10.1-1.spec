%define		PNAME	spades
Version:	3.10.1
Release:	1
License:	GPL
URL:		http://cab.spbu.ru/software/spades
Source:		http://cab.spbu.ru/files/release%{version}/SPAdes-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Summary:	SPAdes – St. Petersburg genome assembler

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

#%define MODULE_VAR      %{MODULE_VAR_PREFIX}LZ4
# This was changed to automatically reflect PNAME
%define MODULE_VAR      %{MODULE_VAR_PREFIX}%(echo "%{PNAME}" | tr [:lower:] [:upper:])

## PACKAGE DESCRIPTION
%description
SPAdes – St. Petersburg genome assembler – is an assembly toolkit containing various assembly pipelines. This manual will help you to install and run SPAdes. SPAdes version 3.10.1 was released under GPLv2 on March 1, 2017 and can be downloaded from http://cab.spbu.ru/software/spades/.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
%setup -n SPAdes-%{version}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Purge environment and reload TACC defaults
module purge
module load TACC cmake

# Set system specific variables
case %{PLATFORM} in
ls5)
	# Compute nodes are CORE-AVX2 and largemem nodes are AVX
	export CFLAGS="-march=sandybridge -mtune=haswell"
	export CXXFLAGS="-march=sandybridge -mtune=haswell"
	pyv="python/2.7.12"
	gv="gcc/5.2.0"
	;;
stampedeknl)
	# Assume architecture is homogeneous throughout system.
	export CFLAGS="-march=knl"
	export CXXFLAGS="-march=knl"
	pyv="python/2.7.13"
	gv="intel/17.0.0"
	;;
wrangler)
	# Assume architecture is homogeneous throughout system.
	export CFLAGS="-march=native"
	export CXXFLAGS="-march=native"
	pyv="python/2.7.13"
	gv="intel/15.0.3"
	;;
stampede)
	# Assume architecture is homogeneous throughout system.
	export CFLAGS="-march=native"
	export CXXFLAGS="-march=native"
	pyv="python/2.7.12"
	gv="gcc/4.9.3"
	;;
hikari)
	# Assume architecture is homogeneous throughout system.
	export CFLAGS="-march=native"
	export CXXFLAGS="-march=native"
	pyv="python/2.7.11"
	gv="gcc/5.2.0"
	;;
esac

module load $gv $pyv

export CC=gcc CXX=g++
PREFIX=${RPM_BUILD_ROOT}/%{INSTALL_DIR} ./spades_compile.sh
rm -rf ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/share/spades/pyyaml3

## Install Steps End
#--------------------------------------

#--------------------------------------

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help (
[[
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, Assembly")
whatis("Description: SPAdes – St. Petersburg genome assembler")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")

always_load("$gv","$pyv")
EOF

## Modulefile End
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
