%define		PNAME	pbalign
Version:	0.3.0
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/pbalign
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	The pbalign package maps PacBio reads to reference sequences

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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}PBALIGN

## PACKAGE DESCRIPTION
%description
The pbalign package maps PacBio reads to reference sequences.

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

module purge
module load TACC

commit=2dd2df2b89138833d4fb61e325057effc8fa0565

# Set up python paths
BI=$RPM_BUILD_ROOT/%{INSTALL_DIR}
PP=${BI}/lib/python2.7/site-packages
mkdir -p $PP
export PYTHONUSERBASE=${BI}

case %{PLATFORM} in
wrangler)
	module use $WORK/public/apps/modulefiles
	pyv="python/2.7.9"
	export PYTHONPATH=${PP}:$PYTHONPATH
	export HDF5_DIR=$TACC_HDF5_DIR
	pyINSTALL="pip install --user"
	$pyINSTALL h5py
	;;
*)
	module use $WORK/ls5/public/apps/modulefiles
	pyv="python/2.7.12"
	module load $pyv hdf5
	export PYTHONPATH=${PP}:$PYTHONPATH
	export HDF5_DIR=$TACC_HDF5_DIR
	pyINSTALL="pip -v --trusted-host pypi.python.org install --user"
	;;
esac
module load $pyv hdf5 pbcore
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

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, PacBio")
whatis("Description: The pbalign package maps PacBio reads to reference sequences")
whatis("URL: %{url}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("PYTHONPATH",	pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

always_load("${pyv}","pbcore","blasr","samtools/1.3")
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
