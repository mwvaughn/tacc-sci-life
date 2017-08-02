%define		PNAME	gsnap
Version:	20170424
Release:	1
License:	A-NC-ND
Group:		Applications/Life Sciences
URL:		http://research-pub.gene.com/gmap
Source:		http://research-pub.gene.com/gmap/src/gmap-gsnap-2017-04-24.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Summary:	gsnap - Genomic Short-read Nucleotide Alignment Program

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
%define MODULE_VAR      %{MODULE_VAR_PREFIX}%(t=%{PNAME}; echo ${t^^})

## PACKAGE DESCRIPTION
%description
GMAP: A Genomic Mapping and Alignment Program for mRNA and EST Sequences, and
GSNAP: Genomic Short-read Nucleotide Alignment Program

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
%setup -n gmap-2017-04-24

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC

# Purge environment and reload TACC defaults
module purge
module load TACC

# Set system specific variables
case %{PLATFORM} in
stampedeknl)
	# Login nodes are CORE-AVX2, compute nodes are MIC-AVX512
	export CFLAGS="-xCORE-AVX2 -axMIC-AVX512 -O3"
	;;
ls5)
	# Compute nodes are CORE-AVX2 and largemem nodes are AVX
	export CFLAGS="-xAVX -axCORE-AVX2 -O3"
	;;
*)
	# Assume architecture is homogeneous throughout system.
	export CFLAGS="-xHOST -O3"
	;;
esac

# Gsnap requires you set the gmapdb location
# but fails if we set it to anywhere in RPM_BUILD_ROOT
export CC=icc
export CXX=icpc
./configure --with-gmapdb=/tmp --prefix=%{INSTALL_DIR}
make -j 16

make DESTDIR=$RPM_BUILD_ROOT install
cp COPYING ChangeLog AUTHORS NEWS NOTICE README VERSION ${RPM_BUILD_ROOT}/%{INSTALL_DIR}

## Install Steps End
#--------------------------------------

#--------------------------------------

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module makes available the GSNAP and GMAP executables.
Documentation for %{PNAME} is available online - %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing, gmap, gsnap")
whatis("Description: gsnap - Genomic Short-read Nucleotide Alignment Program")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")

setenv("%{MODULE_VAR}_DIR",	"%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")

always_load("samtools/1.3")
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
