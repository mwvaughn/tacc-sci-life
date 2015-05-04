Name:       dock
Version:    6.7
Summary:    DOCK v6.7
Release:    1
License:    UCSF
Group:      Applications/Life Sciences
Source:     /work/03439/wallen/stampede/local/tar-files/dock-6.7.zip
URL:        http://dock.compbio.ucsf.edu/
Packager:   TACC - wallen@tacc.utexas.edu
Prefix:     /opt/apps


#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc

# For the intel compiler
# ./build_rpm.sh --intel=15 dock-6.7-1.spec 
%include ./include/%{PLATFORM}/compiler-defines.inc

# Some other defines
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}DOCK
%define PNAME       dock

%description
DOCK is a structure-based molecular docking program that can facilitate the early stages of drug discovery through systematic prescreening of small molecule ligands for shape and energetic compatibility with, for example, a protein receptor. The DOCK 6.7 search strategy is called anchor-and-grow, a breadth-first method for small molecule conformational sampling that involves placing rigid components in the binding site, followed by iterative segment growing and energy minimization. Growth is guided by a wealth of different, user-defined scoring functions, including the DOCK grid energy which maps the protein receptor to a grid. DOCK 6.7 was released February 2015. 


#------------------------------------------------
# PREP SECTION
#------------------------------------------------
%prep

# Remove any old install files
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Run the setup macro - this removes old copies, then unpackages the program zip file
# from ~SOURCES into ~BUILD
%setup -n %{PNAME}-%{version}


#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
cd install/
./configure %{comp_fam}


#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

# The objective of this section is to install the compiled software into a virtual
# directory structure so that it can be packaged up into an RPM
#
# install is also a macro that does many things, including creating appropriate
# directories in $RPM_BUILD_ROOT and cd to the right place

# First start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

# Then make a directory for installing the software
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load the desired modules
module purge
module load TACC
%include ./include/compiler-load.inc

# Go back into the install directory
cd $RPM_BUILD_DIR/%{PNAME}-%{version}/install
make

# Copy the binaries
cp -r ../bin/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r ../parameters/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
#cp -r ../install/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/


#------------------------------------------------
# MODULEFILE SUBSECTION
#------------------------------------------------
# Clean up the old module directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

# Write the module file:
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} built with %{comp_fam}.
Documentation for %{PNAME} is available online at http://dock.compbio.ucsf.edu/
The executables can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: life sciences, computational biology, structural biology")
whatis("Keywords:  Biology, Chemistry, Structural Biology, Docking")
whatis("Description: DOCK is a structure-based docking program used to predict the binding mode of small molecule ligands to target receptors, including proteins.")
whatis("URL: http://dock.compbio.ucsf.edu/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin/")
setenv("%{MODULE_VAR}_PARAMS","%{INSTALL_DIR}/parameters/")
append_path("PATH"       ,"%{INSTALL_DIR}/bin")

EOF
# End of module file

# Lua sytax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

# Also write a version file:
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF


#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files

# Define file permissions
%defattr(755,root,root,-)

# Package all files within these directories, assumed located at $ROOT_BUILD_DIR:
%{INSTALL_DIR}
%{MODULE_DIR}

# Some final clean up:
%post
%clean
rm -rf $RPM_BUILD_ROOT

