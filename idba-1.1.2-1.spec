#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME idba
Version:      1.1.2
Release:      1
License:      GPL
Group:        Applications/Life Sciences
Source:       https://github.com/loneknightpy/idba/releases/download/1.1.2/idba-1.1.2.tar.gz
Packager:     TACC - vaughn@tacc.utexas.edu
Summary:      Iterative De Bruijn graph de novo assembler for short read sequencing data


## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}IDBA

## PACKAGE DESCRIPTION
%description
IDBA-UD is a iterative De Bruijn Graph De Novo Assembler for Short Reads Sequencing data with Highly Uneven Sequencing Depth.

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
module swap $TACC_FAMILY_COMPILER gcc

aclocal
autoconf
automake --add-missing
#./configure --prefix=%{INSTALL_DIR}
./configure
make clean
make -j 8
# Derp. make install is broken at least on Stampede
make install

## Install Steps End
#--------------------------------------

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines these environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS

It provides these applications:
idba, idba_ud, idba_hybrid and idba_tran

Basic IDBA is included only for comparison.
If you are assembling genomic data without reference, please use IDBA-UD.
If you are assembling genomic data with a similar reference genome, please use IDBA-Hybrid.
If you are assembling transcriptome data, please use IDBA-Tran.

Version %{version}

]])

whatis("Name: IDBA-UD")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, Sequencing")
whatis("URL: http://i.cs.hku.hk/~alse/hkubrg/projects/idba_ud/")
whatis("Description: De novo assembler for short read sequencing data")

setenv("%{MODULE_VAR}_DIR",              "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_SCRIPTS", pathJoin("%{INSTALL_DIR}","scripts"))
prepend_path("PATH",                     "%{INSTALL_DIR}/bin")

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

