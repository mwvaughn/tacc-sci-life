%define PNAME macs2
Summary:    MACS2 peak caller
Version: 2.1.0.20150731
License:    GPL
URL:        https://github.com/taoliu/MACS/releases
Packager:   TACC - jawon@tacc.utexas.edu
Source:     https://pypi.python.org/packages/source/M/MACS2/MACS2-2.1.0.20150731.tar.gz
Vendor:     DFCI
Group: Applications/Life Sciences
Release:   1

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}MACS2

## PACKAGE DESCRIPTION
%description
MACS2 empirically models the length of the sequenced ChIP fragments and uses it to improve the spatial resolution of predicted binding sites

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n MACS2-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#--------------------------------------
## Install Steps Start

## Install Steps End
#--------------------------------------
module load python
#mkdir -p $PWD/lib/python2.7/site-packages
#export PYTHONPATH=$PWD/lib/python2.7/site-packages:$PYTHONPATH
#python setup.py build 
python setup.py install --prefix $PWD
cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}

if [ `hostname` == *.ls5.tacc.utexas.edu ]
then
	module load python
	python setup_w_cython.py install --prefix $PWD
	cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}
else 
    module load python
    #module swap $TACC_FAMILY_COMPILER gcc
    python setup_w_cython.py install --prefix $PWD
    cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}
    
fi

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME}.
To call this function, type %{PNAME} on the command line.
Documentation for %{PNAME} is available online at the publisher website: https://github.com/taoliu/MACS/
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PYTHONPATH has been prepended to include the MACS2 library.

Version %{version}

]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, High-throughput Sequencing")
whatis("Description: MACS2 - Model-based Analysis of ChIP-Seq")
whatis("URL: https://github.com/taoliu/MACS")

local macs2_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	macs2_dir)

prepend_path("PYTHONPATH",		pathJoin(macs2_dir,"lib/python2.7/site-packages"))
prepend_path("PYTHONPATH",		pathJoin(macs2_dir,""))
prepend_path("PATH",		pathJoin(macs2_dir,"bin"))

EOF
## Modulefile End
#--------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

## VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
#%files -n %{name}-%{comp_fam_ver}
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
