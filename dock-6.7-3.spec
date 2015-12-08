#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME dock
Version:  6.7
Release:  3
License:  UCSF
Group:    Applications/Life Sciences
Source:   dock-6.7.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Structure-based small molecule docking program
Prefix:   /opt/apps

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR %{MODULE_VAR_PREFIX}DOCK

## PACKAGE DESCRIPTION
%description
DOCK is a structure-based molecular docking program that can facilitate the early stages of drug discovery through systematic prescreening of small molecule ligands for shape and energetic compatibility with, for example, a protein receptor. The DOCK 6.7 search strategy is called anchor-and-grow, a breadth-first method for small molecule conformational sampling that involves placing rigid components in the binding site, followed by iterative segment growing and energy minimization. Growth is guided by a wealth of different, user-defined scoring functions, including the DOCK grid energy which maps the protein receptor to a grid. DOCK 6.7 was released February 2015. 

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Run the setup macro - this removes old copies, then unpackages the program zip file
# from ~SOURCES into ~BUILD
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
module swap $TACC_FAMILY_COMPILER intel 

# Do the 6.7 bugfix
cd $RPM_BUILD_DIR/%{PNAME}-%{version}
patch -N -p0 < install/bugfix.1
    
# Install serial version
cd $RPM_BUILD_DIR/%{PNAME}-%{version}/install
./configure intel
make
    
# Install MPI version
make clean
export MPICH_HOME=` which mpicc | awk -F '/bin' '{print $1}' `
./configure intel.parallel
make dock

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
This module loads %{PNAME} built with %{comp_fam}.
Documentation for %{PNAME} is available online at: http://dock.compbio.ucsf.edu/

The executables can be found in %{MODULE_VAR}_BIN
The parameter files can be found in %{MODULE_VAR}_PARAMS

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Computational Biology, Chemistry, Structural Biology, Docking, Small Molecule, Protein")
whatis("Description: DOCK is a structure-based docking program used to predict the binding mode of small molecule ligands to target receptors, such as proteins.")
whatis("URL: http://dock.compbio.ucsf.edu/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin/")
setenv("%{MODULE_VAR}_PARAMS","%{INSTALL_DIR}/parameters/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/bin")

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

