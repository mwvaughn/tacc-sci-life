%define PNAME htseq
Summary:    HTseq : Analysing high-throughput sequencing data with Python
Version: 0.6.1p1
License:    GPL
URL:        http://www-huber.embl.de/HTSeq/doc/overview.html
Packager:   TACC - jawon@tacc.utexas.edu
Source:     https://pypi.python.org/packages/source/H/HTSeq/HTSeq-0.6.1p1.tar.gz
Vendor:     EMBL
Group: Applications/Life Sciences
Release:   2

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}HTSEQ

## PACKAGE DESCRIPTION
%description
HTSeq is a Python package that provides infrastructure to process data from high-throughput sequencing assays

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n HTSeq-%{version}

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

module load python

mkdir -p $PWD/lib/python2.7/site-packages/
python setup.py install --user
cp -r ~/.local/lib/python2.7/site-packages/HTSeq-%{version}-py2.7-linux-x86_64.egg $PWD/lib/python2.7/site-packages/.
chmod a+rx $PWD/scripts/*

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME}, which depends on python and numpy.
To call this function, use htseq-count
Documentation for %{PNAME} is available online at the publisher website: http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PYTHONPATH has been prepended to include the HTSeq library.

Version %{version}

]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, High-throughput Sequencing")
whatis("Description: HTSeq - Analysing high-throughput sequencing data with Python")
whatis("URL: https://pypi.python.org/pypi/HTSeq")

local htseq_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	htseq_dir)

prepend_path("PATH",		pathJoin(htseq_dir,"scripts"))
prepend_path("PYTHONPATH",  pathJoin(htseq_dir,"lib/python2.7/site-packages/HTSeq-%{version}-py2.7-linux-x86_64.egg/"))

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

module unload python


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
