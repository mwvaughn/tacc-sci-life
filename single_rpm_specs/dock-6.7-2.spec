#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME dock
Version:  6.7
Release:  2
License:  UCSF
Group:    Applications/Life Sciences
Source:   dock-6.7.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Structure-based small molecule docking program

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR %{MODULE_VAR_PREFIX}DOCK

## PACKAGE DESCRIPTION
%description
DOCK is a structure-based molecular docking program that can facilitate the early stages of drug discovery through systematic prescreening of small molecule ligands for shape and energetic compatibility with, for example, a protein receptor. The DOCK 6.7 search strategy is called anchor-and-grow, a breadth-first method for small molecule conformational sampling that involves placing rigid components in the binding site, followed by iterative segment growing and energy minimization. Growth is guided by a wealth of different, user-defined scoring functions, including the DOCK grid energy which maps the protein receptor to a grid. DOCK 6.7 was released February 2015.  

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
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
module purge
module load TACC

%if "%{PLATFORM}" == "stampede"
    module swap $TACC_FAMILY_COMPILER intel/15.0.2
    module swap $TACC_FAMILY_MPI mvapich2/2.1
%endif

%if "%{PLATFORM}" == "wrangler"
    module swap $TACC_FAMILY_COMPILER intel/15.0.3
    module swap $TACC_FAMILY_MPI mvapich2/2.1
%endif

%if "%{PLATFORM}" == "ls5"
    module swap $TACC_FAMILY_COMPILER intel/16.0.1
    module swap $TACC_FAMILY_MPI cray_mpich/7.3.0
    export LDFLAGS="-xAVX -axCORE-AVX2"
%endif

# Do the 6.7 bugfix
cd $RPM_BUILD_DIR/%{PNAME}-%{version}
patch -N -p0 < install/bugfix.1
    
# Install serial version
cd $RPM_BUILD_DIR/%{PNAME}-%{version}/install
./configure intel

%if "%{PLATFORM}" == "ls5"
    make CPPFLAGS="-xAVX -axCORE-AVX2"
%else
    make
%endif

    
# Install MPI version
make clean
export MPICH_HOME=` which mpicc | awk -F '/bin' '{print $1}' `
./configure intel.parallel

%if "%{PLATFORM}" == "ls5"
    make dock CPPFLAGS="-xAVX -axCORE-AVX2" 
%else
    make dock
%endif

# Copy the binaries
cp -r ../bin/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r ../parameters/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
#cp -r ../install/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This module loads %{PNAME} built with %{comp_fam} and %{mpi_fam}. The serial and mpi main executables are:

    dock6
    dock6.mpi

The executables can be found in %{MODULE_VAR}_BIN
The parameter files can be found in %{MODULE_VAR}_PARAMS

Documentation for %{PNAME} is available online at: http://dock.compbio.ucsf.edu/

NOTE: Kuntz Lab programs are available free of charge for academic institutions, but there is a
licensing fee for industrial organizations. Full terms of service here:

http://dock.compbio.ucsf.edu/Online_Licensing/index.htm

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Computational Biology, Chemistry, Structural Biology, Docking, Small Molecule, Protein")
whatis("Description: DOCK is a structure-based docking program used to predict the binding mode of small molecule ligands to target receptors, such as proteins.")
whatis("URL: http://dock.compbio.ucsf.edu/")

prepend_path("PATH",                 "%{INSTALL_DIR}/bin")
setenv(      "%{MODULE_VAR}_DIR",    "%{INSTALL_DIR}/")
setenv(      "%{MODULE_VAR}_BIN",    "%{INSTALL_DIR}/bin/")
setenv(      "%{MODULE_VAR}_PARAMS", "%{INSTALL_DIR}/parameters/")

EOF

%if "%{PLATFORM}" == "stampede"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("intel/15.0.2", "mvapich2/2.1")
EOF
%endif

%if "%{PLATFORM}" == "wrangler"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("intel/15.0.3", "mvapich2/2.1")
EOF
%endif

%if "%{PLATFORM}" == "ls5"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("intel/16.0.1", "cray_mpich/7.3.0")
EOF
%endif

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
# ./build_rpm.sh --intel=15 --mvapich2=2_1 dock-6.7-2.spec    #stampede; wrangler
# ./build_rpm.sh --intel=16 --cmpich=7_3 dock-6.7-2.spec      #ls5
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

