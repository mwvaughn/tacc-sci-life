%define		PNAME	pbcore
Version:	1.2.9
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/pbcore
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	The pbcore package provides Python APIs for interacting with PacBio data files and writing bioinformatics applications.

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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}PBCORE

## PACKAGE DESCRIPTION
%description
The pbcore package provides Python APIs for interacting with PacBio data files and writing bioinformatics applications.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
#%setup -n %{PNAME}-%{version}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
BI=$RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load TACC

commit=282f0d93bf898f02dadf7809f04f170ad9aec011

# Set up python paths
PP=${BI}/lib/python2.7/site-packages
mkdir -p $PP
export PYTHONUSERBASE=${BI}

case %{PLATFORM} in
wrangler)
	pyv="python/2.7.9"
	module load $pyv hdf5
	export HDF5_DIR=$TACC_HDF5_DIR
	pyINSTALL="pip install --user"
	$pyINSTALL h5py
	;;
*)
	pyv="python/2.7.12"
	module load $pyv hdf5
	export HDF5_DIR=$TACC_HDF5_DIR
	export PYTHONPATH=${PP}:$PYTHONPATH
	pyINSTALL="pip -v --trusted-host pypi.python.org install --user"
	;;
esac

$pyINSTALL git+https://github.com/PacificBiosciences/%{PNAME}.git@${commit}

## Install Steps End
#--------------------------------------

#--------------------------------------

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help (
[[
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN
 - %{MODULE_VAR}_LIB

for the location of the %{PNAME} distribution.

Documentation: %{URL}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, PacBio")
whatis("Description: The pbcore package provides Python APIs for interacting with PacBio data files and writing bioinformatics applications.")
whatis("URL: %{URL}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
--prepend_path("LD_LIBRARY_PATH",	pathJoin("${TACC_HDF5_LIB}"))
prepend_path("PYTHONPATH",	pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

always_load("${pyv}","hdf5")
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
