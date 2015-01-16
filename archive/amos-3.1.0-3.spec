Summary:    AMOS - A Modular, Open-Source whole genome assembler
Name:       amos
Version:    3.1.0
Release:    3
License:    Free
Vendor:     AMOS Consortium
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jawon@tacc.utexas.edu
BuildRoot:  /scratch/02114/wonaya/tmp/%{name}-%{version}-buildroot

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
%define MODULE_VAR TACC_AMOS

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
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_AMOS

%description
AMOS is a software infrastructure for developing assembly tools. If you are only interested in running an off-the-shelf assembler on your shotgun data, do not despair, AMOS provides two such assemblers: AMOScmp - a comparative assembler; and Minimus - a basic assembler for small datasets.

## PREP
%prep
# Remove older attempts
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
module purge
module load TACC
module unload $TACC_FAMILY_COMPILER
module load gcc/4.4.5
module load boost
module load perl
module load mummer
module load blat

./configure --prefix=%{INSTALL_DIR} --with-Boost-dir=$TACC_BOOST_INC 
make 'CXXFLAGS=-Wno-deprecated'
make DESTDIR=$RPM_BUILD_ROOT install

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
This module loads %{name} built with gcc. Full Documentation for is available online at the publisher's website:

http://sourceforge.net/apps/mediawiki/amos/

The AMOS executables can be found in %{MODULE_VAR}_BIN. Includes are in %{MODULE_VAR}_INC and libraries are in %{MODULE_VAR}_LIB. 

Dependencies: AMOS is a complex workflow system, with many potential dependencies. Some are taken care by loading additional modules before using AMOS:
* Perl: 'module load perl'
* MUMmer: 'module load mummer'
* BLAT: 'module load blat'

Some Perl scripts in the AMOS package require additional modules 
that you should install:
* DBI
* Statistics::Descriptive
* XML::Parser

You should be able to install these in your local PERL5 directory via CPAN

Version %{version}
]])

whatis("Name: AMOS")
whatis("Version: %{version}")
whatis("Category: Computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Assembly")
whatis("Description: AMOS - A Modular, Open-Source whole genome assembler")
whatis("URL: http://sourceforge.net/apps/mediawiki/amos/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_INC","%{INSTALL_DIR}/include")
setenv("%{MODULE_VAR}_LIB","%{INSTALL_DIR}/lib")
setenv("%{MODULE_VAR}_MAN","%{INSTALL_DIR}/man")

prepend_path("PATH"       ,"%{INSTALL_DIR}/bin")
prepend_path("MANPATH"       ,"%{INSTALL_DIR}/man")

prereq ("boost")
prereq ("perl")
prereq ("mummer")
prereq ("blat")

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

