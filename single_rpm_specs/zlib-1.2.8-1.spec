%define		PNAME	zlib
Version:	1.2.8
Release:	1
License:	BSD
URL:		http://zlib.net
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Source:		zlib-%{version}.tar.gz
Summary:	A Massively Spiffy Yet Delicately Unobtrusive Compression Library

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

#%define MODULE_VAR      %{MODULE_VAR_PREFIX}LZ4
# This was changed to automatically reflect PNAME
%define MODULE_VAR      %{MODULE_VAR_PREFIX}%(echo "%{PNAME}" | tr [:lower:] [:upper:])

## PACKAGE DESCRIPTION
%description
zlib: A Massively Spiffy Yet Delicately Unobtrusive Compression Library

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
%setup -n %{PNAME}-%{version}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

# Source IPP
tar -xzf $IPPROOT/examples/components_and_examples_lin_ps.tgz ./components/interfaces/ipp_zlib/zlib-1.2.8.patch
source /opt/intel/compilers_and_libraries_2017.4.196/linux/ipp/bin/ippvars.sh intel64

# Patch zlib
patch -p1 < components/interfaces/ipp_zlib/zlib-%{version}.patch

# Compile zlib
source /opt/intel/compilers_and_libraries_2017.4.196/linux/bin/compilervars.sh intel64
export CFLAGS="%{TACC_OPT} -m64 -DWITH_IPP -I$IPPROOT/include"
export LDFLAGS="-L$IPPROOT/lib/intel64 -lippdc -lipps -lippcore"
export CC=icc
export CXX=icpc
export LD=xild
export AR=xiar
./configure --prefix=%{INSTALL_DIR}
make shared
make DESTDIR=${RPM_BUILD_ROOT} install

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
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_INC

for the location of the %{PNAME} distribution.

For static linking to Intel IPP on Linux* OS, 

  gcc -O3 -o zpipe_ipp.out zpipe.c -I$IPPROOT/include $%{MODULE_VAR}_LIB/libz.a $IPPROOT/lib/intel64/libippdc.a $IPPROOT/lib/intel64/libipps.a $IPPROOT/lib/intel64/libippcore.a

For dynamic linking to Intel IPP on Linux* OS,

  gcc -O3 -o zpipe_ipp.out zpipe.c -I$IPPROOT/include $%{MODULE_VAR}_LIB/libz.a -L$IPPROOT/lib/intel64 -lippdc -lipps -lippcore

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: applications, compression")
whatis("Keywords: compression, deflate")
whatis("Description: LZ4 is a fast compression algorithm")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",		"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")

prereq("intel/17.0.4")
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
