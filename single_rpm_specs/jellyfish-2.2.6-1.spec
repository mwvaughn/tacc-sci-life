%define	PNAME	jellyfish
Version:	2.2.6
Release:	1
License:	GPL
Source:		https://github.com/gmarcais/Jellyfish/releases/download/v2.2.6/jellyfish-2.2.6.tar.gz
URL:		http://www.genome.umd.edu/jellyfish.html
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	A fast, lock-free approach for efficient parallel counting of occurrences of k-mers.

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}JELLYFISH

## PACKAGE DESCRIPTION
%description
Jellyfish is a tool for fast, memory-efficient counting of k-mers in DNA. A k-mer is a substring of length k, and counting the occurrences of all such substrings is a central step in many analyses of DNA sequence. Jellyfish can count k-mers using an order of magnitude less memory and an order of magnitude faster than other k-mer counting packages by using an efficient encoding of a hash table and by exploiting the "compare-and-swap" CPU instruction to increase parallelism.

JELLYFISH is a command-line program that reads FASTA and multi-FASTA files containing DNA sequences. It outputs its k-mer counts in a binary format, which can be translated into a human-readable text format using the "jellyfish dump" command, or queried for specific k-mers with "jellyfish query". See the UserGuide provided on Jellyfish's home page for more details.

If you use Jellyfish in your research, please cite:

Guillaume Marcais and Carl Kingsford, A fast, lock-free approach for efficient parallel counting of occurrences of k-mers. Bioinformatics (2011) 27(6): 764-770 (first published online January 7, 2011) doi:10.1093/bioinformatics/btr011

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

## Install Steps Start
module purge
module load TACC

export LDFLAGS="-Wl,-rpath,$ICC_LIB" CC=icc CXX=icpc

# Set system specific variables
case %{PLATFORM} in
stampedeknl)
        # Login nodes are CORE-AVX2, compute nodes are MIC-AVX512
        export CFLAGS="-xCORE-AVX2 -axMIC-AVX512 -O3"
	pyv="python/2.7.13"
        ;;
ls5)
        # Compute nodes are CORE-AVX2 and largemem nodes are AVX
        export CFLAGS="-xAVX -axCORE-AVX2 -O3"
	pyv="python/2.7.12"
        ;;
wrangler)
        # Assume architecture is homogeneous throughout system.
        export CFLAGS="-xHOST -O3 -ipo"
	pyv="python/2.7.9"
        ;;
hikari)
        # Assume architecture is homogeneous throughout system.
        export CFLAGS="-march=native -O3"
	pyv="gcc/5.2.0 python/2.7.11"
	export LDFLAGS="-Wl,-rpath,$TACC_GCC_LIB -Wl,-rpath,$TACC_GCC_LIB64" CC=gcc CXX=g++
        ;;
*)
        # Assume architecture is homogeneous throughout system.
        export CFLAGS="-xHOST -O3 -ipo"
	pyv="python/2.7.12"
        ;;
esac
module load $pyv

## Configure
./configure --prefix=%{INSTALL_DIR} CXXFLAGS="$CFLAGS" \
	--enable-python-binding --with-sse --with-int128 
## Make
make -j 4

## Install Steps End
#--------------------------------------
make install DESTDIR=$RPM_BUILD_ROOT

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help (
[[
The %{PNAME} module file defines the following environment variables:

%{MODULE_VAR}_DIR
%{MODULE_VAR}_INC
%{MODULE_VAR}_LIB

The python bindings have been pre-built and already added to the
python path. This package was also compiled with sse and int128.
Documentation can be found online at %{url}.

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: kmer, k-mer, bloom")
whatis("Description: A fast, lock-free approach for efficient parallel counting of occurrences of k-mers.")
whatis("URL: %{url}")

local inst_dir = "%{INSTALL_DIR}"
%if "%{PLATFORM}" == "hikari"
always_load("gcc/5.2.0","python/2.7.11")
%else
always_load("$pyv")
%endif

setenv("%{MODULE_VAR}_DIR",	inst_dir)
setenv("%{MODULE_VAR}_INC",	pathJoin(inst_dir,"include"))
setenv("%{MODULE_VAR}_LIB",	pathJoin(inst_dir,"lib"))

prepend_path("PATH",		pathJoin(inst_dir,"bin"))
prepend_path("INCLUDE",		pathJoin(inst_dir,"include"))
prepend_path("LD_LIBRARY_PATH",	pathJoin(inst_dir,"lib"))
prepend_path("MANPATH",		pathJoin(inst_dir,"share/man"))
prepend_path("PYTHONPATH",      pathJoin(inst_dir,"lib/python2.7/site-packages"))

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
## version file for %{name}-%{version}
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
