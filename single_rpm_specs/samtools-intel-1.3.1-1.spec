%define PNAME samtools
Version: 1.3.1
Release: 2
Summary: Samtools is a suite of programs for interacting with high-throughput sequencing data.
License: GPL
Group: Applications/Life Sciences
Source: https://github.com/samtools/samtools/releases/download/%{version}/%{PNAME}-%{version}.tar.bz2
Packager: TACC - vaughn@tacc.utexas.edu, jfonner@tacc.utexas.edu, gzynda@tacc.utexas.edu

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}SAMTOOLS

## PACKAGE DESCRIPTION
%description
Samtools is a suite of programs for interacting with high-throughput sequencing data. It consists of three separate repositories:

	Samtools - Reading/writing/editing/indexing/viewing SAM/BAM/CRAM format
	BCFtools - Reading/writing BCF2/VCF/gVCF files and calling/filtering/summarising SNP and short indel sequence variants
	HTSlib - A C library for reading/writing high-throughput sequencing data

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

# Set system specific variables
case %{PLATFORM} in
stampede2)
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

## Make Samtools
./configure CC=icc CFLAGS="$CFLAGS" --prefix=%{INSTALL_DIR}
make -j 6 DESTDIR=${RPM_BUILD_ROOT} install
cd ..
## Make bcftools
tar -xjf %{_sourcedir}/bcftools-%{version}.tar.bz2
cd bcftools-%{version}
make -j 6 CC=icc CFLAGS="$CFLAGS" prefix=%{INSTALL_DIR} DESTDIR=${RPM_BUILD_ROOT} all install
cd ..
## Make htslib
tar -xjf %{_sourcedir}/htslib-1.3.2.tar.bz2 && cd htslib-1.3.2
./configure CC=icc CFLAGS="$CFLAGS" --prefix=%{INSTALL_DIR}
make -j 6 DESTDIR=${RPM_BUILD_ROOT} install
cd ..

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
Samtools is a suite of programs for interacting with high-throughput sequencing data. It consists of three separate repositories:

	Samtools - Reading/writing/editing/indexing/viewing SAM/BAM/CRAM format
	BCFtools - Reading/writing BCF2/VCF/gVCF files and calling/filtering/summarising SNP and short indel sequence variants
	HTSlib - A C library for reading/writing high-throughput sequencing data

The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution
	%{MODULE_VAR}_BIN - the location of the %{PNAME} binaries
	%{MODULE_VAR}_LIB - the location of the %{PNAME} libraries
	%{MODULE_VAR}_LIBEXEC - the location of the %{PNAME} libexec files
	%{MODULE_VAR}_SHARE - the location of the %{PNAME} man files

Documentation can be found online at http://www.htslib.org/ or with
	man samtools
	man bcftools

Version %{version}
]])

whatis("Name: samtools")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing, Genotyping, Resequencing, SNP, SAM, BCF, VCF, TABIX, BAM")
whatis("URL: http://www.htslib.org/")
whatis("Description: Samtools is a suite of programs for interacting with high-throughput sequencing data.")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",              "%{INSTALL_DIR}/lib")
prepend_path("MANPATH",           "%{INSTALL_DIR}/share/man")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")
setenv (     "%{MODULE_VAR}_LIBEXEC", "%{INSTALL_DIR}/libexec")
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
