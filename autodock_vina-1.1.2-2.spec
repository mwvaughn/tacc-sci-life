#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME autodock_vina
Version:  1.1.2
Release:  2
License:  Apache License V2.0
Group:    Applications/Life Sciences
Source0:  http://vina.scripps.edu/download/autodock_vina_1_1_2.tgz
Patch1:   %{PNAME}-%{version}.patch
Packager: TACC - wallen@tacc.utexas.edu
Summary:  An open-source program for doing molecular docking

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
#%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
#%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR %{MODULE_VAR_PREFIX}AUTODOCK_VINA

## PACKAGE DESCRIPTION
%description
AutoDock Vina is an open-source program for doing molecular docking. It was designed and implemented by Dr. Oleg Trott in the Molecular Graphics Lab at The Scripps Research Institute.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%setup -n %{PNAME}_1_1_2

# Made minor changes so vina would work with Blast filesystem version 3.
# There is precedent for these changes here: http://mgl.scripps.edu/forum/viewtopic.php?f=12&t=2153
%patch1 -p1

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

%if "%{PLATFORM}" == "stampede"
    # have not tested yet
%endif

%if "%{PLATFORM}" == "wrangler"
    # have not tested yet
%endif

%if "%{PLATFORM}" == "ls5"
    module swap $TACC_FAMILY_COMPILER gcc/4.9.3
    module load boost/1.59
%endif

export MY_BOOST_VERSION=$(basename $TACC_BOOST_DIR)
cd ./build/linux/release

%if "%{PLATFORM}" == "ls5"
    make \
        GPP=g++ \
        BASE=$TACC_BOOST_DIR \
        BOOST_VERSION=$MY_BOOST_VERSION \
        CPPFLAGS="$CPPFLAGS -MMD" \
        LDFLAGS="-L$TACC_BOOST_LIB" \
        LIBS="-lboost_system -lboost_thread -lboost_serialization -lboost_filesystem -lboost_program_options -lrt" \
        C_PLATFORM="-static -pthread" \
        CFLAGS="-march=sandybridge -mtune=haswell"
%endif

# Copy the binaries
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}/bin
cp ./vina ./vina_split $RPM_BUILD_ROOT%{INSTALL_DIR}/bin
chmod -R a+rx $RPM_BUILD_ROOT%{INSTALL_DIR}/bin

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This module loads %{PNAME} built with g++.
The following executables can be found in %{MODULE_VAR}_BIN:
    vina
    vina_split

Documentation for %{PNAME} is available online at: http://vina.scripps.edu/index.html

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: life sciences, computational biology, chemistry")
whatis("Keywords: Computational Biology, Chemistry, Structural Biology, Docking, Small Molecule, Protein")
whatis("Description: Open-source program for drug discovery, molecular docking, and virtual screening, offering multi-core capability, high performance and enhanced accuracy and ease of use.")
whatis("URL: http://vina.scripps.edu/")

prepend_path("PATH",                 "%{INSTALL_DIR}/bin")
setenv(      "%{MODULE_VAR}_DIR",    "%{INSTALL_DIR}/")
setenv(      "%{MODULE_VAR}_BIN",    "%{INSTALL_DIR}/bin/")

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
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

# In SPECS dir:
# ./build_rpm.sh autodock_vina-1.1.2-2.spec   # lonestar5 
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua
