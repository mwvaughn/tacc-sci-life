%define		PNAME	boost
Version:	1.61.0
Release:	1
License:	GPL
URL:		http://www.boost.org
Source:		%{PNAME}_1_61_0.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Summary:	Boost provides free peer-reviewed portable C++ source libraries

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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}CCACHE

## PACKAGE DESCRIPTION
%description
Boost provides free peer-reviewed portable C++ source libraries

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
#%setup -n %{PNAME}_1_61_0

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

[ -e boost_1_61_0 ] && rm -rf boost_1_61_0
[ -e boost_1_61_0.tar.gz ] || zwget http://downloads.sourceforge.net/project/boost/boost/1.61.0/boost_1_61_0.tar.gz
tar -xzf boost_1_61_0.tar.gz
cd boost_1_61_0

module purge
module load TACC

mkdir local_install
CONFIGURE_FLAGS="--with-toolset=intel-linux --with-libraries=system,program_options,iostreams"
./bootstrap.sh --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR} ${CONFIGURE_FLAGS}
./b2 -j 2 -s NO_BZIP2=1 --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR} install
#./bootstrap.sh --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR} ${CONFIGURE_FLAGS}
#./b2 -j 2 -s NO_BZIP2=1

#mkdir -p              $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r ${ID}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

rm -f ~/tools/build/v2/user-config.jam

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

Documentation: %{URL}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: Applications")
whatis("URL: %{url}")
whatis("Keywords: System, Library, C++")
whatis("Description: Boost provides free peer-reviewed portable C++ source libraries %{BOOST_TYPE}.")

prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("INCLUDE",		pathJoin("%{INSTALL_DIR}", "include"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_INC",	pathJoin("%{INSTALL_DIR}", "include"))
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
