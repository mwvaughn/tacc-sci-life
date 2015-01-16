Summary:    Trans-ABySS
Name:       trans-ABySS
Version:    1.4.4
Release:    1
License:    BCCA
Vendor:     BC Cancer Agency
Group: Applications/Life Sciences
Source:     trans-abyss-1.4.4.tar.gz
Packager:   TACC - wonaya@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_TRANSABYSS

%description
Trans-ABySS is a software pipeline for analyzing ABySS-assembled contigs from shotgun transcriptome data.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{PNAME}-v%{version}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
module purge
module load TACC
module unload $TACC_FAMILY_COMPILER
module load gcc
module load samtools
module load bwa
module load jdk64
module load abyss
module load python


cd kmer
gmake install
cd ../src
gmake
cd ..

module unload python

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
To startup this program, use go to %{MODULE_VAR}_DIR/Linux-amd64/bin/ in the command line to see all the available tools. 
Documentation for %{PNAME} is available online at the publisher website: http://sourceforge.net/apps/mediawiki/wgs-assembler/index.php?title=Main_Page
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include %{PNAME}.

Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Mapping")
whatis("Description: Celera assembler - de novo whole-genome shotgun (WGS) DNA sequence assembler")
whatis("URL: http://sourceforge.net/apps/mediawiki/wgs-assembler")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

prereq ("bwa")
prereq ("samtools")
prereq ("abyss")

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

