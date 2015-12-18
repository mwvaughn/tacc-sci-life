%define PNAME soapdenovo2
Summary:    SOAP de novo 2 - Short Oligonucleotide Analysis Package
Version: r240
License:    GPL
URL:        http://soap.genomics.org.cn/soapdenovo.html
Packager:   TACC - jawon@tacc.utexas.edu
Source:     http://downloads.sourceforge.net/project/soapdenovo2/SOAPdenovo2/bin/r240/SOAPdenovo2-bin-LINUX-generic-r240.tgz
Vendor:     BGI
Group: Applications/Life Sciences
Release:   4

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}SOAPDENOVO2

## PACKAGE DESCRIPTION
%description
SOAPdenovo2, a short read de novo assembly tool, is a package for assembling short oligonucleotide into contigs and scaffolds.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n SOAPdenovo2-bin-LINUX-generic-%{version}

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

if [ "%{PLATFORM}" != "ls5" ]
then
	module purge
	module load TACC
fi

## Install Steps End
#--------------------------------------
cp -r SOAPdenovo-127mer SOAPdenovo-63mer $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME}. Resolves more repeat regions in contig assembly, increases coverage and length in scaffold construction, improves gap closing, and optimizes for large genome. 

Version %{version}

]])

whatis("Name: soapdenovo2")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly")
whatis("Description: soapdenovo2 - novel short-read assembly method that can build a de novo draft assembly for the human-sized genomes")
whatis("URL: http://soap.genomics.org.cn/soapdenovo.html")

local soap_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	soap_dir)

prepend_path("PATH",		pathJoin(soap_dir,""))

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
