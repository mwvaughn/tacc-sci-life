#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME eman
Version:  2.12
Release:  1
License:  GPLv2
Group:    Applications/Life Sciences
Source:   eman2.12.linux64.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  A scientific image processing suite for single particle reconstruction from cryoEM

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
#%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
#%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc
#prevent stripping of binaries
%define __spec_install_post %{nil}

%define MODULE_VAR %{MODULE_VAR_PREFIX}EMAN

## PACKAGE DESCRIPTION
%description
From the developers: EMAN2 is a scientific image processing suite with a particular focus on single particle reconstruction from cryoEM images. EMAN2 is a complete refactoring of the original EMAN1 library. The new system offers an easily extensible infrastructure, better documentation, easier customization, etc. EMAN2 was designed to happily coexist with EMAN1 installations, for users wanting to experiment, but not ready to completely switch from EMAN1 to EMAN2. 

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%setup -n EMAN2

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

# Loading Python/2.7.3 removes some python syntax warnings, but nothing of consequence

%if "%{PLATFORM}" == "stampede"
    module load python/2.7.3-epd-7.3.2
%endif

%if "%{PLATFORM}" == "ls5"
    module load python/2.7.10
%endif

# Rather than run the built-in installer script...
#./eman2-installer

# ... Do this instead:
%define EMAN2DIR %{INSTALL_DIR}
%define EMAN2PYTHON %{EMAN2DIR}/extlib/bin/python
find ./extlib/bin -name "ipython" -exec sed -i "s|^\#\!.*python.*$|\#\!%{EMAN2PYTHON}|" {} \;
find ./test ./bin ./lib ./examples -name "*.py" -exec sed -i "s|^\#\!.*python.*$|\#\!%{EMAN2PYTHON}|" {} \;

# Copy the relevant files
cp -r $RPM_BUILD_DIR/EMAN2/bin $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/doc $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/examples $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/extlib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/fonts $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/images $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/include $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/lib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN2/test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

cd $RPM_BUILD_ROOT/%{INSTALL_DIR}/
ln -s extlib/ Python

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This module loads %{PNAME} version %{version}. Threading is enabled, but MPI is not.
Documentation for %{PNAME} is available online at: http://blake.bcm.edu/emanwiki/EMAN2

Loading this module defines the following environment variables:
    %{MODULE_VAR}_DIR
    %{MODULE_VAR}_BIN
    %{MODULE_VAR}_DOC
    %{MODULE_VAR}_EXAMPLES
    %{MODULE_VAR}_EXTLIB
    %{MODULE_VAR}_FONTS
    %{MODULE_VAR}_IMAGES
    %{MODULE_VAR}_INCLUDE
    %{MODULE_VAR}_LIB
    %{MODULE_VAR}_TEST

Loading this module also has the effect of sourcing the eman2.bashrc, which sets the following:
    EMAN2DIR=%{MODULE_VAR}_DIR
    PATH=${EMAN2DIR}/bin:${EMAN2DIR}/extlib/bin:$PATH
    PYTHONPATH=${EMAN2DIR}/lib:${EMAN2DIR}/bin:$PYTHONPATH
    alias sparx=sx.py

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, electron microscopy")
whatis("Keywords: Biology, Cryo-EM, Image Processing, Reconstruction")
whatis("Description: EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM.")
whatis("URL: http://blake.bcm.edu/emanwiki/EMAN2")

prepend_path("PATH",               "%{INSTALL_DIR}/extlib/bin")
prepend_path("PATH",               "%{INSTALL_DIR}/bin")
prepend_path("PYTHONPATH",         "%{INSTALL_DIR}/bin")
prepend_path("PYTHONPATH",         "%{INSTALL_DIR}/lib")

setenv("EMAN2DIR",               "%{INSTALL_DIR}/")
setenv("EMAN2PYTHON",            "%{INSTALL_DIR}/extlib/bin/python")
setenv("%{MODULE_VAR}_DIR",      "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN",      "%{INSTALL_DIR}/bin/")
setenv("%{MODULE_VAR}_DOC",      "%{INSTALL_DIR}/doc/")
setenv("%{MODULE_VAR}_EXAMPLES", "%{INSTALL_DIR}/examples/")
setenv("%{MODULE_VAR}_EXTLIB",   "%{INSTALL_DIR}/extlib/")
setenv("%{MODULE_VAR}_FONTS",    "%{INSTALL_DIR}/fonts/")
setenv("%{MODULE_VAR}_IMAGES",   "%{INSTALL_DIR}/images/")
setenv("%{MODULE_VAR}_INCLUDE",  "%{INSTALL_DIR}/include/")
setenv("%{MODULE_VAR}_LIB",      "%{INSTALL_DIR}/lib/")
setenv("%{MODULE_VAR}_TEST",     "%{INSTALL_DIR}/test/")

set_alias("sparx", "sx.py")

EOF

## Modulefile End
#--------------------------------------

# Lua sytax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#--------------------------------------
## VERSION FILE
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
## VERSION FILE END
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}

## POST 
#prevent stripping of binaries
#%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

# In SPECS dir:
# ./build_rpm.sh eman-2.12-1.spec
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

