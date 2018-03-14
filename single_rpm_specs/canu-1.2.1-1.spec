%define		PNAME	canu
Version:	1.2.1
Release:	1
License:	BSD
URL:		https://github.com/marbl/canu
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	Celera assembler for long reads

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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}CANU

## PACKAGE DESCRIPTION
%description

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
#%setup -n %{PNAME}-%{version}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

if [ "%{PLATFORM}" != "ls5" ]
then
        module purge
        module load TACC
fi
module load boost python

[ -d %{PNAME} ] && rm -rf %{PNAME}
git clone git@github.com:marbl/canu.git
cd %{PNAME}
git checkout d64bca3dba89d0d7c7c6a056f93a3440edf77529
patch -p1 << "EOF"
diff --git a/src/Makefile b/src/Makefile
index 19f4511..037b01b 100644
--- a/src/Makefile
+++ b/src/Makefile
@@ -96,8 +96,8 @@ define ADD_TARGET_RULE
 
         $${TARGET_DIR}/${1}: $${${1}_OBJS} $${${1}_PREREQS}
 	    @mkdir -p $$(dir $$@)
-	    $$(strip $${${1}_LINKER} -o $$@ $${LDFLAGS} $${${1}_LDFLAGS} \
-	        $${${1}_OBJS} $${LDLIBS} $${${1}_LDLIBS})
+	    $$(strip $${${1}_LINKER} $${${1}_OBJS} -o $$@ $${LDFLAGS} $${${1}_LDFLAGS} \
+	        $${LDLIBS} $${${1}_LDLIBS})
 	    $${${1}_POSTMAKE}
     endif
     endif
@@ -370,22 +370,19 @@ endif
 # Set compiler and flags based on discovered hardware
 
 ifeq (${OSTYPE}, Linux)
-  CC        ?= gcc
-  CXX       ?= g++
-  CXXFLAGS  := -pthread -fPIC -Wno-write-strings -Wno-unused -Wno-char-subscripts -Wno-sign-compare # -Wformat -Wall -Wextra
-  LDFLAGS   := -pthread -lm
+  CC        := icc
+  CXX       := icpc
+  CXXFLAGS  := -xHOST -fPIC -Wno-write-strings -Wno-unused -Wno-char-subscripts -Wno-sign-compare -I${TACC_BOOST_INC}
+  LDFLAGS   := -lpthread -lm -L${TACC_BOOST_LIB} -Wl,-rpath=${ICC_LIB}
 
-  CXXFLAGS  += -D_GLIBCXX_PARALLEL -fopenmp
-  LDFLAGS   +=                     -fopenmp
+  CXXFLAGS  += -D_GLIBCXX_PARALLEL -openmp
+  LDFLAGS   +=                     -openmp
 
   CXXFLAGS  += -Wall -Wextra -Wno-write-strings -Wno-unused -Wno-char-subscripts -Wno-sign-compare -Wformat
 
   ifeq ($(BUILDPROFILE), 1)
     CXXFLAGS  +=
     LDFLAGS   += -pg
-  else
-    CXXFLAGS  += -D_GLIBCXX_PARALLEL
-    LDFLAGS   += -D_GLIBCXX_PARALLEL
   endif
 
   ifeq ($(BUILDDEBUG), 1)
@@ -394,7 +391,7 @@ ifeq (${OSTYPE}, Linux)
     ifeq ($(BUILDPROFILE), 1)
       CXXFLAGS   += -O4 -funroll-loops -fexpensive-optimizations -finline-functions
     else
-      CXXFLAGS   += -O4 -funroll-loops -fexpensive-optimizations -finline-functions -fomit-frame-pointer
+      CXXFLAGS   += -O3 -funroll-loops -finline-functions -fomit-frame-pointer
     endif
   endif
 endif
EOF

cd src
make -j 4

cp -r ../Linux-amd64/bin ${RPM_BUILD_ROOT}/%{INSTALL_DIR}

cd ../documentation
make man
mkdir -p ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/man
cp -r build/man ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/man/man1

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
The %{PNAME} module file defines the following environment variables: %{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME} distribution.

Documentation: http://canu.readthedocs.io/en/stable/

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, PacBio")
whatis("Description: Canu is a fork of the Celera Assembler designed for high-noise single-molecule sequencing.")
whatis("URL: %{URL}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("MANPATH",		pathJoin("%{INSTALL_DIR}", "man"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

prereq("java/1.8.74")
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
