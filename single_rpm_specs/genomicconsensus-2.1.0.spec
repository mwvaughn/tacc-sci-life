%define		PNAME	genomicconsensus
Version:	2.1.0
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/GenomicConsensus
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	The GenomicConsensus package provides the variantCaller tool, which allows you to apply the Quiver or Arrow algorithm to mapped PacBio reads to get consensus and variant calls.

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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}GC

## PACKAGE DESCRIPTION
%description
The GenomicConsensus package provides the variantCaller tool, which allows you to apply the Quiver or Arrow algorithm to mapped PacBio reads to get consensus and variant calls.

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

case %{PLATFORM} in
wrangler)
	pyv="python/2.7.9"
	;;
*)
	pyv="python/2.7.12"
	;;
esac

# Load dependencies
module purge
module load TACC
module use $WORK/public/apps/modulefiles
module load $pyv hdf5 pbcore swig
module load boost/1.61.0

# Set up env
BI=$RPM_BUILD_ROOT/%{INSTALL_DIR}
PP=${BI}/lib/python2.7/site-packages
mkdir -p $PP
export PYTHONPATH=${PP}:$PYTHONPATH

# Build ConsensusCore
[ -d ConsensusCore ] && rm -rf ConsensusCore
git clone git@github.com:PacificBiosciences/ConsensusCore.git
cd ConsensusCore
#git checkout 28dbb199c1fdf85f4b3f7661a70bec496be19ab6
python setup.py install --prefix=$BI --boost=$TACC_BOOST_DIR/include

# Clone the repo
[ -d GenomicConsensus ] && rm -rf GenomicConsensus
git clone git@github.com:PacificBiosciences/GenomicConsensus.git
cd GenomicConsensus
git checkout c591976e28d1fb8043152f3772143a6786cd39d5
#git checkout e1f1661f0cc8be4dd5c0cb71631b46e20f8c00ab
python setup.py install --prefix $BI

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
whatis("Description: The GenomicConsensus package provides the variantCaller tool, which allows you to apply the Quiver or Arrow algorithm to mapped PacBio reads to get consensus and variant calls.")
whatis("URL: %{url}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("PYTHONPATH",	pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

always_load("${pyv}","pbcore","boost/1.61.0","swig")
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
