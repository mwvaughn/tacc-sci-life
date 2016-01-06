Name:     dock
Version:  6.7
Release:  1
License:  UCSF
Source:   dock-6.7.tar.gz
URL:      http://dock.compbio.ucsf.edu/
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Structure-based small molecule docking program

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}DOCK
%define PNAME       dock

%package %{PACKAGE}
Summary: Structure-based small molecule docking program
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: Structure-based small molecule docking program
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
DOCK is a structure-based molecular docking program that can facilitate the early stages of drug discovery through systematic prescreening of small molecule ligands for shape and energetic compatibility with, for example, a protein receptor. The DOCK 6.7 search strategy is called anchor-and-grow, a breadth-first method for small molecule conformational sampling that involves placing rigid components in the binding site, followed by iterative segment growing and energy minimization. Growth is guided by a wealth of different, user-defined scoring functions, including the DOCK grid energy which maps the protein receptor to a grid. DOCK 6.7 was released February 2015. 


## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif

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

#--------------------------------------
%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    ########### Do Not Remove #############

    ## Install Steps Start
    module purge
    module load TACC
    module swap $TACC_FAMILY_COMPILER intel 
    
    # The objective of this section is to install the compiled software into a virtual
    # directory structure so that it can be packaged up into an RPM
    #
    # install is also a macro that does many things, including creating appropriate
    # directories in $RPM_BUILD_ROOT and cd to the right place
    
    # Do the 6.7 bugfix
    cd $RPM_BUILD_DIR/%{PNAME}-%{version}
    patch -N -p0 < install/bugfix.1
    
    # Install serial version
    cd $RPM_BUILD_DIR/%{PNAME}-%{version}/install
    ./configure intel
    make
    
    # Install MPI version
    make clean
    ./configure intel.parallel
    make dock
    
    # Copy the binaries
    cp -r ../bin/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    cp -r ../parameters/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    #cp -r ../install/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
%endif


#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------

%if %{?BUILD_MODULEFILE}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
    ########### Do Not Remove #############


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


%endif

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
%defattr(-,root,install,)
%{INSTALL_DIR}
%endif # ?BUILD_PACKAGE

%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE}
%defattr(-,root,install,)
%{MODULE_DIR}
%endif # ?BUILD_MODULEFILE

## POST 
%post %{PACKAGE}
export PACKAGE_POST=1
%include include/post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include include/post-defines.inc

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

