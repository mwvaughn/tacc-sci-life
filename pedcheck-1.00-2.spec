Summary:    pedcheck - Program for detecting marker typing incompatibilities in pedigree data.
Name:       pedcheck
Version:    1.00
Release:    2
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
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_PEDCHECK

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
PedCheck is a program for identification of genotype incompatibilities in linkage analysis.

PedCheck will assist researchers in identifying all Mendelian inconsistencies in pedigree data and will provide them with useful and detailed diagnostic information to help resolve the errors. The program, which uses many of the algorithms implemented in VITESSE, handles large data sets quickly and efficiently, accepts a variety of input formats, and offers various error-checking algorithms that match the subtlety of the pedigree error. These algorithms range from simple parent-offspring-compatibility checks to a single-locus likelihood-based statistic that identifies and ranks the individuals most likely to be in error. 

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
%prep 

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/<source>
# Use -n <name> if source file different from <name>-<version>.tar.gz

%setup -n %{name}_src

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC

make

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

