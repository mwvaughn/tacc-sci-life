#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME coreutils
Version:      8.24
Release:      1
License:      GPL
Group:        Applications/Life Sciences
Source:       http://ftp.gnu.org/gnu/coreutils/coreutils-8.24.tar.xz
Packager:     TACC - vaughn@tacc.utexas.edu
Summary:      GNU Core Utilities are the basic file, shell and text manipulation utilities of the GNU operating system.

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}COREUTILS

## PACKAGE DESCRIPTION
%description
The GNU Core Utilities are the basic file, shell and text manipulation utilities of the GNU operating system. These are the core utilities which are expected to exist on every operating system.

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

configure --prefix=%{INSTALL_DIR} CPPFLAGS="-fgnu89-inline"
make

## Install Steps End
#--------------------------------------

make DESTDIR=$RPM_BUILD_ROOT install

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_LIB for the location of the %{name}
distribution. Documentation can be found online at http://www.gnu.org/software/coreutils/manual/

Version %{version}

]])

whatis("Name: coreutils")
whatis("Version: %{version}")
whatis("Category: Utilities")
whatis("Keywords: Scripting, Utilities")
whatis("URL: http://www.gnu.org/software/coreutils/")
whatis("Description: Basic file, shell and text manipulation utilities of the GNU operating system.")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("MANPATH",              "%{INSTALL_DIR}/man")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

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
