#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME eman
Version:  1.9
Release:  2
License:  GPLv2
Group:    Applications/Life Sciences
Source:   eman-linux-x86_64-cluster-1.9.tar.gz
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
From the developers: EMAN is a suite of scientific image processing tools aimed primarily at the transmission electron microscopy community, though it is beginning to be used in other fields as well. For example it can do an admirable job aligning images for amateur astronomers. EMAN has a particular focus on performing a task known as single particle reconstruction. In this method, images of nanoscale molecules and molecular assemblies embedded in vitreous (glassy) ice are collected on a transmission electron microscope, then processed using EMAN to produce a complete 3-D recosntruction at resolutions now approaching atomic resolution. For low resolution structures (~2 nm), this may require ~8 hours of computer processing and a few thousand particles. For structures aimed at ~0.5 nm or better resolution, hundreds of thousands of particles and hundreds of thousands of CPU-hours (on large computational clusters) may be required. Indeed, EMAN is often used in supercomputing facilities as a test application for large-scale computing.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%setup -n EMAN

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

# Rather than run the built-in installer script...
#./eman-installer

# ... Do this instead:
ln -s ./libpyEM.so.ucs4.py2.6 lib/libpyEM.so

# Two python scripts (boxunboxed.py and fpdump.py) point to /bin/env instead of /usr/bin/env.
sed -i "s|^\#\!\/bin\/env python|\#\!\/usr\/bin\/env python|" ./python/boxunboxed.py
sed -i "s|^\#\!\/bin\/env python|\#\!\/usr\/bin\/env python|" ./python/fpdump.py

# Note this version of eman uses the system version of python on LS5 (2.6).

# Copy the relevant files
cp -r $RPM_BUILD_DIR/EMAN/bin $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN/chimeraext $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN/doc $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN/include $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN/lib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/EMAN/python $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This module loads %{PNAME} version %{version}. This is the pre-compiled binary.
It should be used with the Lonestar5 system version of Python, version 2.6.9,
located here: /usr/bin/python
Documentation for %{PNAME} is available online at: http://blake.bcm.edu/emanwiki/EMAN1

Loading this module defines the following environment variables:
    %{MODULE_VAR}_DIR
    %{MODULE_VAR}_BIN
    %{MODULE_VAR}_DOC
    %{MODULE_VAR}_INCLUDE
    %{MODULE_VAR}_LIB
    %{MODULE_VAR}_PYTHON

Loading this module also has the effect of sourcing the eman.bashrc, which sets the following:
    EMANDIR=%{MODULE_VAR}_DIR
    PATH=${EMANDIR}/bin:$PATH
    LD_LIBRARY_PATH=${EMANDIR}/lib:$LD_LIBRARY_PATH
    PYTHONPATH=${EMANDIR}/lib:$PYTHONPATH

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, electron microscopy")
whatis("Keywords: Biology, Cryo-EM, Image Processing, Reconstruction")
whatis("Description: A scientific image processing suite for single particle reconstruction from cryoEM.")
whatis("URL: http://blake.bcm.edu/emanwiki/EMAN1")

prepend_path("PATH",               "%{INSTALL_DIR}/bin")
prepend_path("PATH",               "%{INSTALL_DIR}/python")
prepend_path("LD_LIBRARY_PATH",    "%{INSTALL_DIR}/lib")
prepend_path("PYTHONPATH",         "%{INSTALL_DIR}/lib")

setenv("EMANDIR",                "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_DIR",      "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN",      "%{INSTALL_DIR}/bin/")
setenv("%{MODULE_VAR}_DOC",      "%{INSTALL_DIR}/doc/")
setenv("%{MODULE_VAR}_INCLUDE",  "%{INSTALL_DIR}/include/")
setenv("%{MODULE_VAR}_LIB",      "%{INSTALL_DIR}/lib/")
setenv("%{MODULE_VAR}_PYTHON",   "%{INSTALL_DIR}/python/")

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
# ./build_rpm.sh eman-1.9-2.spec
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

