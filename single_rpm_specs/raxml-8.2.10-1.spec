%define		PNAME	raxml
Version:	8.2.10
Release:	1
License:	BSD
URL:		https://github.com/stamatak/standard-RAxML
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Summary:	A tool for Phylogenetic Analysis and Post-Analysis of Large Phylogenies

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

#%define MODULE_VAR      %{MODULE_VAR_PREFIX}LZ4
# This was changed to automatically reflect PNAME
%define MODULE_VAR      %{MODULE_VAR_PREFIX}%(t=%{PNAME}; echo ${t^^})

## PACKAGE DESCRIPTION
%description
RAxML Version 8: A tool for Phylogenetic Analysis and Post-Analysis of Large Phylogenies

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

# Edit the commit variable to build a set version of the code.
# Commit can be left empty to build the latest version of the code.
repo=$(basename %{url})
commit=9f786d6dab327149fd08cc0ce2c9f7ac66327541

# Remove previous versions of the directory if they exist
[ -e $repo ] && rm -rf $repo

# Download and checkout
git clone %{url}.git && cd $repo
[ -n $commit ] && git checkout $commit

# Purge environment and reload TACC defaults
module purge
module load TACC

# Set system specific variables
case %{PLATFORM} in
stampedeknl)
	# Login nodes are CORE-AVX2, compute nodes are MIC-AVX512
	export CFLAGS="-xCORE-AVX2 -axMIC-AVX512 -O3"
	;;
ls5)
	# Compute nodes are CORE-AVX2 and largemem nodes are AVX
	export CFLAGS="-xAVX -axCORE-AVX2 -O3"
	;;
*)
	# Assume architecture is homogeneous throughout system.
	export CFLAGS="-xHOST -O3"
	;;
esac

# CFLAGS are already exported.
# Compile on 4 cores. Drop this number to troubleshoot.
# The ICC_LIB directory is rpathed so this code will work even with GCC loaded
for f in Makefile.AVX.*.gcc;
do
	make -f $f -j 2
	rm *.o
done

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -p raxmlHPC* $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

# Clean up BUILD direcotry
cd ../ && rm -rf $repo

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
whatis("Category: application, biology")
whatis("Keywords: Biology, Application, Phylogenetics")
whatis("URL: %{url}")
whatis("Description: Maximum Likelihood Tree Inference Tool")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
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
