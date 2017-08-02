#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME ray
Version:      2.3.1
Release:      1
License:      GPL
Group:        Applications/Life Sciences
Source:       https://sourceforge.net/projects/denovoassembler/files/Ray-2.3.1.tar.bz2
Packager:     TACC - gzynda@tacc.utexas.edu
Summary:      Distributed De Bruijn graph de novo assembler


## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
#%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
#%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}RAY

## PACKAGE DESCRIPTION
%description
Ray is a parallel software that computes de novo genome assemblies with next-generation sequencing data.

Ray is written in C++ and can run in parallel on numerous interconnected computers using the message-passing interface (MPI) standard.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n Ray-%{version}

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
module purge
module load TACC
module load impi

patch Makefile -li - << 'EOF'
29c29
< CXXFLAGS = -O3 -std=c++98 -Wall -g
---
> CXXFLAGS = -O3 -std=c++98 -Wall -g -xHOST
55c55
< MAXKMERLENGTH = 32
---
> MAXKMERLENGTH = 96
61c61
< HAVE_LIBZ = n
---
> HAVE_LIBZ = y
96c96
< MPI_IO=n
---
> MPI_IO = y
148c148
< LDFLAGS = $(LDFLAGS-y)
---
> LDFLAGS = $(LDFLAGS-y)
EOF

make -j 16 PREFIX=${RPM_BUILD_ROOT}/%{INSTALL_DIR}
make PREFIX=${RPM_BUILD_ROOT}/%{INSTALL_DIR} install

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

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_DOC

It provides these applications:
 - Ray

The maximum k-mer size is 96 bases.

Version %{version}
]])

whatis("Name: ray")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, Sequencing")
whatis("URL: http://denovoassembler.sourceforge.net/")
whatis("Description: Distributed De Bruijn graph de novo assembler")

setenv("%{MODULE_VAR}_DIR",              "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_DOC",              "%{INSTALL_DIR}/Documentation")
prepend_path("PATH",                     "%{INSTALL_DIR}")
always_load("impi")
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

