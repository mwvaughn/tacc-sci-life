#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

%define PNAME Rstats
Summary:    R is a free software environment for statistical computing and graphics.
Version:    3.0.2
Release:    1
License:    GPLv2
Vendor:     R Foundation for Statistical Computing
Group:      Applications/Statistics
Source:     https://cran.r-project.org/src/base/R-3/R-3.0.2.tar.gz
Packager:   TACC - vaughn@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}R

## PACKAGE DESCRIPTION
%description
R provides a wide variety of statistical (linear and nonlinear
modelling, classical statistical tests, time-series analysis,
classification, clustering, etc.) and graphical techniques, and
is highly extensible.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n R-%{version}

## BUILD
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

module swap $TACC_FAMILY_COMPILER gcc

./configure --prefix=%{INSTALL_DIR} \
  --enable-R-shlib --enable-shared \
  --with-blas --with-lapack --with-pic \
  --without-readline

mkdir -p $PWD/tmpinstall

make
make install

## Install Steps End

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
This is the R statistics (Rstats) package built on %(date +'%B %d, %Y').
The R modulefile defines the environment variables TACC_R_DIR, TACC_R_BIN,
TACC_R_LIB and extends the PATH and LD_LIBRARY_PATH paths as appropriate.

Version %{version}
]]
)

whatis("Name: R")
whatis("Version: %{version}")
whatis("Category: Applications, Statistics, Graphics")
whatis("Keywords: Applications, Statistics, Graphics, Scripting Language")
whatis("URL: http://www.r-project.org/")
whatis("Description: statistics package")

--
-- Create environment variables.
--
local r_dir   = "%{INSTALL_DIR}"
local r_bin   = "%{INSTALL_DIR}/bin"
local r_inc   = "%{INSTALL_DIR}/include"
local r_lib   = "%{INSTALL_DIR}/lib64"
local r_man   = "%{INSTALL_DIR}/share/man"

setenv("TACC_R_DIR", r_dir)
setenv("TACC_R_BIN", r_bin)
setenv("TACC_R_INC", r_inc)
setenv("TACC_R_LIB", r_lib)
setenv("TACC_R_MAN", r_man)

append_path("PATH", r_bin)
append_path("MANPATH", r_man)
append_path("LD_LIBRARY_PATH", r_lib)
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
