Summary:    MUMmer - A modular system for the rapid whole genome alignment of finished or draft sequence
Name:       mummer
Version:    3.23
Release:    1
License:    OSI Certified Open Source Software
Group: Applications/Life Sciences
Source:     MUMmer%{version}.tar.gz
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
%define PNAME mummer

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
MUMmer is a system for rapidly aligning entire genomes, whether in complete or draft form. For example, MUMmer 3.0 can find all 20-basepair or longer exact matches between a pair of 5-megabase genomes in 13.7 seconds, using 78 MB of memory, on a 2.4 GHz Linux desktop computer. MUMmer can also align incomplete genomes; it can easily handle the 100s or 1000s of contigs from a shotgun sequencing project, and will align them to another set of contigs or a genome using the NUCmer program included with the system. If the species are too divergent for a DNA sequence alignment to detect similarity, then the PROmer program can generate alignments based upon the six-frame translations of both input sequences

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_MUMMER

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/bwa-VERSION
%setup -n MUMmer%{version}

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

module purge
module load TACC
module unload $TACC_FAMILY_COMPILER 
module load gcc

#-----------------------------
# Build parallel version
#-----------------------------

make

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

rm -rf src Makefile 
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with gcc. Documentation is available online at the publisher's website:

http://mummer.sourceforge.net/

The MUMmer executables can be found in %{MODULE_VAR}_DIR

Dependencies: MUMmer is a complex workflow system, with many potential dependencies. Some are taken care of via module prerequisites:
* Perl 5.12: 'module load perl/5.12'

Version %{version}
]])

whatis("Name: mummer")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Assembly")
whatis("Description: MUMmer - A modular system for the rapid whole genome alignment of finished or draft sequence")
whatis("URL: http://mummer.sourceforge.net/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")

prereq ("perl")

prepend_path("PATH"       ,"%{INSTALL_DIR}/")
prepend_path("PERL5LIB"       ,"%{INSTALL_DIR}/scripts")

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

