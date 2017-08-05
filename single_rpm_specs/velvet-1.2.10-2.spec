#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

%define PNAME velvet
Summary: Velvet - Sequence assembler for very short reads
Version: 1.2.10
Release: 2
License: GPLv2
Group: Applications/Life Sciences
Source:  https://www.ebi.ac.uk/~zerbino/velvet/velvet_%{version}.tgz
Packager: TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}VELVET

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------

%description
Velvet is a de novo genomic assembler specially designed for short read sequencing technologies, such as Solexa or 454, developed by Daniel Zerbino and Ewan Birney at the European Bioinformatics Institute (EMBL-EBI), near Cambridge, in the United Kingdom.

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

# Unpack source
#%setup -n %{PNAME}_%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------

%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start

[ -e velvet ] && rm -rf velvet
git clone https://github.com/dzerbino/velvet.git
cd velvet
git checkout 9adf09f7ded7fedaf6b0e5e4edf9f46602e263d3

[ %{PLATFORM} == "wrangler" ] && export TACC_ICC_LIB=${ICC_LIB}

case %{PLATFORM} in
"ls5")
	patch -p1 << "EOF"
diff --git a/Makefile b/Makefile
index a4b46e2..d470e6d 100644
--- a/Makefile
+++ b/Makefile
@@ -1,15 +1,17 @@
-CC = gcc
+CC = icc
 CFLAGS = -Wall
 DEBUG = -g
 LIBS = -lm
 OPT = -O3
-MAXKMERLENGTH?=31
-CATEGORIES?=2
+IOMP=/opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64_lin/
+LDFLAGS="-Wl,-rpath,$(TACC_ICC_LIB)"
+MAXKMERLENGTH?=64
+CATEGORIES?=4
 DEF = -D MAXKMERLENGTH=$(MAXKMERLENGTH) -D CATEGORIES=$(CATEGORIES)
 PDFLATEX_VERSION := $(shell pdflatex --version 2> /dev/null)
 
 # Mac OS users: uncomment the following lines
-CFLAGS = -Wall -m64
+CFLAGS = -Wall -m64 -openmp -xAVX -axCORE-AVX2
 
 # Sparc/Solaris users: uncomment the following line
 # CFLAGS = -Wall -m64
EOF
	;;
*)
	patch -p1 << "EOF"
diff --git a/Makefile b/Makefile
index a4b46e2..d470e6d 100644
--- a/Makefile
+++ b/Makefile
@@ -1,15 +1,17 @@
-CC = gcc
+CC = icc
 CFLAGS = -Wall
 DEBUG = -g
 LIBS = -lm
 OPT = -O3
-MAXKMERLENGTH?=31
-CATEGORIES?=2
+IOMP=/opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64_lin/
+LDFLAGS="-Wl,-rpath,$(TACC_ICC_LIB)"
+MAXKMERLENGTH?=64
+CATEGORIES?=4
 DEF = -D MAXKMERLENGTH=$(MAXKMERLENGTH) -D CATEGORIES=$(CATEGORIES)
 PDFLATEX_VERSION := $(shell pdflatex --version 2> /dev/null)
 
 # Mac OS users: uncomment the following lines
-CFLAGS = -Wall -m64
+CFLAGS = -Wall -m64 -openmp -xHOST
 
 # Sparc/Solaris users: uncomment the following line
 # CFLAGS = -Wall -m64
EOF
	;;
esac
	

make 'LONGSEQUENCES=1' -j3

## Install Steps End
#------------------------------------------------

mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp velvet[gh] $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -R tests data Columbus_manual.pdf Manual.pdf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} and makes available the Velvet assembler
Documentation is available online at http://www.ebi.ac.uk/~zerbino/velvet/
Velvet is configured as such: MAXKMERLENGTH=64 LONGSEQUENCES CATEGORIES=4 OPENMP

Version %{version}
]])

whatis("Name: velvet")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, Assembly")
whatis("Description: Velvet - Sequence assembler for very short reads")
whatis("URL: http://www.ebi.ac.uk/~zerbino/velvet/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/bin")

EOF
## Modulefile End
#------------------------------------------------

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
