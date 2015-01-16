Summary:    AMOS - A Modular, Open-Source whole genome assembler
Name:       amos
Version:    3.1.0
Release:    1
License:    Free
Vendor:     AMOS Consortium
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
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
%define PNAME amos

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
AMOS is a software infrastructure for developing assembly tools. If you are only interested in running an off-the-shelf assembler on your shotgun data, do not despair, AMOS provides two such assemblers: AMOScmp - a comparative assembler; and Minimus - a basic assembler for small datasets.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_AMOS

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/<version>
# %setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Temp FS method
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
cd                   %{INSTALL_DIR}

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc
module load boost
module load perl/5.12

#-----------------------------
# Build parallel version
#-----------------------------

tar xzvf %{_topdir}/SOURCES/%{name}-%{version}.tar.gz --strip-components 1

./configure --prefix=%{INSTALL_DIR} --with-Boost-dir=$TACC_BOOST_INC && make 'CXXFLAGS=-Wno-deprecated' && make install

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

cd %{INSTALL_DIR}
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf  $RPM_BUILD_ROOT/%{INSTALL_DIR}/src
chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd	$RPM_BUILD_ROOT
umount %{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with gcc. Full Documentation for is available online at the publisher's website:

http://sourceforge.net/apps/mediawiki/amos/

The AMOS executables can be found in %{MODULE_VAR}_BIN. Includes are in %{MODULE_VAR}_INC and libraries are in %{MODULE_VAR}_LIB. 

Dependencies: AMOS is a complex workflow system, with many potential dependencies. Some are taken care by loading additional modules before using AMOS:
* Perl 5.12: 'module load perl/5.12'
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

