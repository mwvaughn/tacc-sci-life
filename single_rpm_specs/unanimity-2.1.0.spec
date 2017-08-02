%define		PNAME	unanimity
Version:	2.1.0
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/unanimity
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	C++ library and its applications to generate and process accurate consensus sequences

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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}UN

## PACKAGE DESCRIPTION
%description
C++ library and its applications to generate and process accurate consensus sequences

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
BR=${RPM_BUILD_ROOT}
ID=${INSTALL_DIR}
mkdir -p ${BI}/{bin,lib}
TOP=$PWD

module purge
module load TACC

case %{PLATFORM} in
wrangler)
	module load python/2.7.9 hdf5 cmake
	module use $WORK/public/apps/modulefiles
	module load ccache googletest blasr genomicconsensus boost/1.61.0 swig pbcopper
#	export CC=icc
#	export CXX=icpc
#	export CFLAGS="-O3 -xHOST"
#	export CXXFLAGS="-O3 -xHOST"
	export CC=gcc
	export CXX=g++
	export CFLAGS="-fPIC -O3 -march=native"
	export CXXFLAGS="-fPIC -O3 -march=native"
	export BOOST_ROOT=$TACC_BOOST_DIR
	;;
ls5)
	bver="boost/1.59"
	module load python/2.7.12 hdf5 cmake samtools/1.3 $bver
	module use $WORK/ls5/public/apps/modulefiles
	module load ccache
	export CC=icc
	export CXX=icpc
	export CFLAGS="-fPIC -O3 -xAVX -axCORE-AVX2"
	export CXXFLAGS="-fPIC -O3 -xAVX -axCORE-AVX2 -D_GNU_SOURCE"
	export BOOST_ROOT=$TACC_BOOST_DIR
	;;
*)
	module load python/2.7.12 hdf5 cmake samtools/1.3 boost/1.61.0
	module use $WORK/public/apps/modulefiles
	module load ccache googletest
	;;
esac

function pbgit {
	GIT=/work/03076/gzynda/rpmbuild/SOURCES/${1}-${2}.tar.gz
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

####################################################
# seqan
####################################################
pbgit seqan
tar -chf - include | tar -xf - -C $BI
cd $TOP

####################################################
# unanimity
####################################################
pbgit unanimity
mkdir build && cd build

export HTS_INC=${TACC_BLASR_DIR}/local/pb_htslib/include
export HTS_LIB=${TACC_BLASR_DIR}/local/pb_htslib/lib

cmake \
	-DUNY_build_tests=OFF \
	-DZLIB_INCLUDE_DIRS=/usr/include \
	-DZLIB_LIBRARIES=/usr/lib64/libz.so \
	-DBoost_INCLUDE_DIRS=${TACC_BOOST_INC} \
	-DPacBioBAM_INCLUDE_DIRS=${TACC_BLASR_INC} \
	-DPacBioBAM_LIBRARIES=$TACC_BLASR_LIB/libpbbam.so \
	-DHTSLIB_INCLUDE_DIRS=$HTS_INC \
	-DHTSLIB_LIBRARIES=$HTS_LIB/libhts.a \
	-DSEQAN_INCLUDE_DIRS=${BI}/include \
	-Dpbcopper_INCLUDE_DIRS=${TACC_PBC_INC} \
	-Dpbcopper_LIBRARIES=${TACC_PBC_LIB}/libpbcopper.a \
	..
make -j 4
cp ccs ${BI}/bin/
export PYTHONUSERBASE=${BI}
pyINSTALL="pip install -U --user"
cd $TOP
	     CMAKE_COMMAND=cmake \
        Boost_INCLUDE_DIRS=$TACC_BOOST_INC \
              SWIG_COMMAND=$(which swig) \
     pbcopper_INCLUDE_DIRS=$TACC_PBC_INC \
        pbcopper_LIBRARIES=$TACC_PBC_LIB/libpbcopper.a \
                   VERBOSE=1 \
        $pyINSTALL --no-deps ./unanimity

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
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, PacBio")
whatis("Description: C++ library and its applications to generate and process accurate consensus sequences")
whatis("URL: %{url}")

prepend_path("PATH",			pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",		pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("PYTHONPATH",		pathJoin("%{INSTALL_DIR}", "lib/python2.7/site-packages"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))
setenv("%{MODULE_VAR}_INC",	pathJoin("%{INSTALL_DIR}", "include"))
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))

always_load("swig","python","blasr")
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
