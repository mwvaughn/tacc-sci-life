Summary:    SSAKE is a genomics application for assembling millions of very short DNA sequences
Name:       ssake
Version:    3.8
Release:    2
License:    GPLv2
Vendor:     Michael Smith Genome Science Centre
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jfonner@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
%include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME ssake

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group:   Applications/Biology

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_SSAKE

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/maq-0.7.1
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
%include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)

#-----------------------------
# Build parallel version
#-----------------------------

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -rp ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install
#done. ssake's files need only be moved into place.


# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with the Intel 11.1 compiler.
This module makes available the SSAKE perl script. If you are 
using your own perl distribution, you should copy the SSAKE file
to your local directory and change the first line to point to your
perl installation.

Test files can be found in %{MODULE_VAR}_TEST and the tools that 
come with ssake are in the %{MODULE_VAR}_TOOLS directory

Version %{version}
]])

whatis("Name: ssake")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly")
whatis("Description: ssake - a genomics application for assembling millions of very short DNA sequences")
whatis("URL: http://www.bcgsc.ca/platform/bioinfo/software/ssake")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_TOOLS","%{INSTALL_DIR}/tools")
setenv("%{MODULE_VAR}_TEST","%{INSTALL_DIR}/test")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

EOF

#--------------
#  Version file.
#--------------

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
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

