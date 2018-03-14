%define PNAME allpathslg
Summary:    ALLPATHS-LG - Broad Institute assembler for complex eukaryote genomes
Version: 52488
License:    GPL
URL:        http://www.broadinstitute.org/software/allpaths-lg/blog/
Packager:   TACC - jawon@tacc.utexas.edu
Source:     ftp://ftp.broadinstitute.org/pub/crd/ALLPATHS/Release-LG/latest_source_code/allpathslg-52488.tar.gz
Vendor:     Broad Institute
Group: Applications/Life Sciences
Release:   2

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}ALLPATHSLG

## PACKAGE DESCRIPTION
%description
ALLPATHS‐LG is a short‐read assembler. It has been designed to use reads produced by new sequencing technology machines such as the Illumina Genome Analyzer. The version described here has been optimized for, but not necessarily limited to, reads of length 100 bases. ALLPATHS is not designed to assemble Sanger or 454 FLX reads, or a mix of these with short reads.

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

#--------------------------------------
## Install Steps Start
if [ `hostname` == *.ls5.tacc.utexas.edu ]
then
	module swap $TACC_FAMILY_COMPILER gcc
else 
    module swap $TACC_FAMILY_COMPILER gcc
fi

./configure --prefix=%{INSTALL_DIR} 
make -j 12 LDFLAGS="-Wl,-rpath,$GCC_LIB"

# strip is important - otherwise the binaries sum to > 500 MB and packaging will fail
make DESTDIR=$RPM_BUILD_ROOT install-strip

## Install Steps End
#--------------------------------------
#cp -R bin $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with gcc.
This module makes available the ALLPATHS-LG assembler. Documentation for %{name} is available online at the publisher\'s website: http://www.broadinstitute.org/software/allpaths-lg/
The ALLPATHS-LG executables can be found in "$PATH". 

ALLPATHS-LG requires Picard tools for data preparation, and Graphviz dot for plotting assembly graphs. The former is provided as a module, the latter may be self-installed in the user's $HOME directory.
Version %{version}

]])

whatis("Name: ALLPATHS-LG")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Sequencing, Assembly")
whatis("Description: ALLPATHS-LG - Broad Institute assembler for complex eukaryote genomes")
whatis("URL: http://www.broadinstitute.org/software/allpaths-lg/")

local allpathslg_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	allpathslg_dir)

prepend_path("PATH",		pathJoin(allpathslg_dir,"bin"))

EOF
## Modulefile End
#--------------------------------------

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