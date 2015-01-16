Summary:    pedcheck - Program for detecting marker typing incompatibilities in pedigree data.
Name:       pedcheck
Version:    1.00
Release:    1
License:    Academic Use
Vendor:     Shaun Purcell
Group: Applications/Life Sciences
Source:     pedcheck_src.tgz
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME pedcheck

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
PedCheck is a program for identification of genotype incompatibilities in linkage analysis.

PedCheck will assist researchers in identifying all Mendelian inconsistencies in pedigree data and will provide them with useful and detailed diagnostic information to help resolve the errors. The program, which uses many of the algorithms implemented in VITESSE, handles large data sets quickly and efficiently, accepts a variety of input formats, and offers various error-checking algorithms that match the subtlety of the pedigree error. These algorithms range from simple parent-offspring-compatibility checks to a single-locus likelihood-based statistic that identifies and ranks the individuals most likely to be in error. 

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_PEDCHECK

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
%prep 

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/<source>
# Use -n <name> if source file different from <name>-<version>.tar.gz

%setup -n %{name}_src

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
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)
module unload $TACC_FAMILY_COMPILER

module purge
module load TACC

#-----------------------------
# Build parallel version
#-----------------------------

make CC=icc CXX=icpc

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

 cp ./pedcheck ./README.txt $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with icc.

This module makes available the pedcheck executable. Documentation for %{name} is available online at the publisher's website: http://watson.hgen.pitt.edu/register/docs/pedcheck.html
The pedcheck executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: pedcheck")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genetics, GWAS")
whatis("Description: pedcheck - Program for detecting marker typing incompatibilities in pedigree data")
whatis("URL: http://watson.hgen.pitt.edu/register/docs/pedcheck.html")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
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

