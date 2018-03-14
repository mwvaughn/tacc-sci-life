%define		PNAME	falcon
Version:	1.8.6
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/FALCON-integrate
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	A set of tools for fast aligning long reads for consensus and assembly

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
export CC=icc
export falcon=`pwd`
export falcon_install=${RPM_BUILD_ROOT}/%{INSTALL_DIR}
export python_site=${falcon_install}/lib/python2.7/site-packages
export PATH=${falcon_install}/bin:${PATH}
export PYTHONPATH=${python_site}:${PYTHONPATH}

makeCores=2

export PYTHONUSERBASE=${falcon_install}
case "%{PLATFORM}" in
"ls5")
	pyv="python/2.7.12"
	#pyINSTALL="python setup.py install --prefix=${falcon_install}"
	pyINSTALL="pip -v --trusted-host pypi.python.org install --user"
	FLAGS="-O3 -xAVX -axCORE-AVX2"
	export ncores=24
	;;
"wrangler")
	pyv="python/2.7.9"
	pyINSTALL="pip install -U --user"
	FLAGS="-O3 -xHOST"
	export ncores=24
	;;
*)
	pyv="python/2.7.12"
	pyINSTALL="pip install -U --user"
	FLAGS="-O3 -xHOST"
	export ncores=16
	;;
esac
module load hdf5 $pyv

function pbgit {
	GIT=$WORK/rpmbuild/SOURCES/${1}-${2}.tar.gz
	[ -d $1 ] && rm -rf $1
	if [ -e $GIT ]
	then
		tar -xzf $GIT
	else
		git clone https://github.com/PacificBiosciences/${1}.git && cd $1
		[ -n "$2" ] && git checkout $2
		git submodule update --init --recursive
		cd .. && tar -czf $GIT $1
	fi
	cd $1
}

# Make python site-packages path
mkdir -p ${python_site}
#[ "%{PLATFORM}" = "stampede" ] && easy_install --user pyparsing==1.5.7

pbgit FALCON-integrate a72f47c4600fb31c993151c1d03c1787ba42b161
FF=$PWD

## Make pypeFLOW
$pyINSTALL networkx==1.10
$pyINSTALL ./pypeFLOW

## Make FALCON
$pyINSTALL ./FALCON

export PREFIX=${falcon_install}
#[ -d ${falcon_install}/bin ] || mkdir ${falcon_install}/bin
## Make DAZZ_DB
cd ${FF}/DAZZ_DB
make -j $makeCores CFLAGS="$FLAGS -no-ansi-alias"
make -j $makeCores CFLAGS="$FLAGS -no-ansi-alias" install

## Make DALIGNER
cd ${FF}/DALIGNER
make -j $makeCores CFLAGS="$FLAGS -fno-strict-aliasing"
make -j $makeCores CFLAGS="$FLAGS -fno-strict-aliasing" install

## Make DAMASKER
cd ${FF}/DAMASKER
make -j $makeCores CFLAGS="$FLAGS -fno-strict-aliasing"
make -j $makeCores CFLAGS="$FLAGS -fno-strict-aliasing" install

## Make DEXTRACTOR
cd ${FF}/DEXTRACTOR
make -j $makeCores CFLAGS="$FLAGS -fno-strict-aliasing"
make -j $makeCores CFLAGS="$FLAGS -fno-strict-aliasing" install

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
whatis("URL: %{url}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("PYTHONPATH",	pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("FALCON_PREFIX",		"%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_INC",	pathJoin("%{INSTALL_DIR}", "include"))
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))

EOF
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
always_load("${pyv}", "vq")
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
