%define		PNAME	cutadapt
Version:	1.14
Release:	1
License:	BSD
URL:		https://cutadapt.readthedocs.io/en/stable/
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	trim adapters from high-throughput sequencing reads

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

#%define MODULE_VAR      %{MODULE_VAR_PREFIX}LZ4
# This was changed to automatically reflect PNAME
%define MODULE_VAR      %{MODULE_VAR_PREFIX}%(echo "%{PNAME}" | tr [:lower:] [:upper:])

## PACKAGE DESCRIPTION
%description
Cutadapt finds and removes adapter sequences, primers, poly-A tails and other types of unwanted sequence from your high-throughput sequencing reads.

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

# Purge environment and reload TACC defaults
module purge
module load TACC

# Create a valid python package directory
PP=$RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/python2.7/site-packages
mkdir -p $PP
# This is where pip will install --user packages
export PYTHONUSERBASE=$RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load the correct version of python. This will also be made a dependency of the module.
case %{PLATFORM} in
wrangler)
        pyv="python/2.7.9"
        ;;
stampedeknl)
        pyv="python/2.7.13"
        ;;
hikari)
        pyv="python/2.7.11"
	;;
*)
        pyv="python/2.7.12"
        ;;
esac

# Load python and add the build directory to the python path
module load $pyv
export PYTHONPATH=${PP}:$PYTHONPATH

pip --trusted-host pypi.python.org install --user cutadapt==1.14

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
Cutadapt finds and removes adapter sequences, primers, poly-A tails and other types of unwanted sequence from your high-throughput sequencing reads.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: biology, genomics, qc, qa")
whatis("Description: trim adapters from high-throughput sequencing reads")
whatis("URL: %{url}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("PYTHONPATH",	pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

always_load("${pyv}")
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
