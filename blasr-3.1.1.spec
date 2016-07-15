%define		PNAME	blasr
Version:	3.1.1
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/blasr
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

%define MODULE_VAR      %{MODULE_VAR_PREFIX}BLASR

## PACKAGE DESCRIPTION
%description
A PacificBiosciences tool for aligning very long sequencing reads.

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

if [ "%{PLATFORM}" != "ls5" ]
then
        module purge
        module load TACC
fi
module load python/2.7.9 hdf5

# Clone the repo
[ -d %{PNAME} ] && rm -rf %{PNAME}
git clone git@github.com:PacificBiosciences/blasr.git
cd blasr
git checkout 6fa6cc2ef893d4425131018e277e1406f3763c6c
git submodule update --init --recursive

./configure.py --shared --sub --no-pbbam HDF5_INCLUDE=${TACC_HDF5_INC} HDF5_LIB=${TACC_HDF5_LIB} CXX=icpc CXXFLAGS="-O3 -xHOST -Wl,-rpath,$TACC_HDF5_LIB"
export CXX=icpc
cd libcpp
NOPBBAM=1 HDF5_LIB=$TACC_HDF5_LIB HDF5_INC=$TACC_HDF5_INC ./configure.py CXX=icpc CXXFLAGS="-O3 -xHOST" EXTRA_LDFLAGS="-Wl,-rpath,$TACC_HDF5_LIB"
make -j 4

cd ..
make -j 4

mkdir $BI/{bin,lib}
for lib in `find . -name \*.so`
do
	mv $lib $BI/lib/
done
mv blasr $BI/bin/
for bin in `find utils -maxdepth 1 -executable -type f`
do
	mv $bin $BI/bin/
done
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
 - %{MODULE_VAR}_LIB

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, PacBio")
whatis("Description: blasr - A set of tools for fast aligning long reads")
whatis("URL: %{url}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
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
