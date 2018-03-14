%define		PNAME	falcon_patched-mm
Version:	0.4.2
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/FALCON-integrate
Source:		%{PNAME}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	A set of tools for fast aligning long reads for consensus and assembly

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
%include ./include/name-defines.inc

%define MODULE_VAR      %{MODULE_VAR_PREFIX}FALCON

## PACKAGE DESCRIPTION
%description
The Falcon tool kit is a set of simple code collection which I use for studying efficient assembly algorithm for haploid and diploid genomes. It has some back-end code implemented in C for speed and some simple front-end written in Python for convenience.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
%setup -n %{PNAME}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

if [ "%{PLATFORM}" != "ls5" ]
then
        module purge
        module load TACC
fi
module load python
module load hdf5

export CC=icc
export ncores=16
export falcon=`pwd`
export falcon_install=${RPM_BUILD_ROOT}/%{INSTALL_DIR}
export python_site=${falcon_install}/lib/python2.7/site-packages
export PATH=${falcon_install}/bin:${PATH}
export PYTHONPATH=${python_site}:${PYTHONPATH}

# Make python site-packages path
mkdir -p ${python_site}

## Make pypeFLOW
cd ${falcon}/pypeFLOW
python setup.py install --prefix=${falcon_install}

## Make FALCON
cd ${falcon}/FALCON
python setup.py install --prefix=${falcon_install}

## Make DAZZ_DB
cd ${falcon}/DAZZ_DB
if [ "%{PLATFORM}" != "ls5" ]
then
	make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -xHOST -no-ansi-alias"
else
	make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -xAVX -axCORE-AVX2 -no-ansi-alias"
fi
[ -d ${falcon_install}/bin ] || mkdir ${falcon_install}/bin
cp fasta2DB DB2fasta quiva2DB DB2quiva DBsplit DBdust Catrack DBshow DBstats DBrm simulator fasta2DAM DAM2fasta ${falcon_install}/bin

## Make DALIGNER
cd ${falcon}/DALIGNER
make -j ${ncores} CFLAGS="-O3 -Wall -Wextra -Wno-unused-result -no-ansi-alias -xHOST"
cp daligner HPCdaligner HPCmapper LAsort LAmerge LAsplit LAcat LAshow LAcheck daligner_p LA4Falcon DB2Falcon  ${falcon_install}/bin

## Install Steps End
#--------------------------------------

#--------------------------------------

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables: %{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME} distribution.

Documentation: https://github.com/PacificBiosciences/FALCON/wiki/Manual

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, PacBio")
whatis("Description: FALCON - A set of tools for fast aligning long reads for consensus and assembly")
whatis("URL: %{URL}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("PYTHONPATH",	pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("FALCON_PREFIX",		"%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

prereq("python","hdf5")
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
