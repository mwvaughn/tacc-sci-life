Summary:    dizzy - chemical kinetics stochastic simulation software package written in Java
Name:       dizzy
Version:    1.11.4
Release:    2
License:    GNU Library Public License
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%include ../system-defines.inc
%define PNAME dizzy

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
Dizzy is a chemical kinetics stochastic simulation software package written in Java. It provides a model defin
ition environment and an implementation of the Gillespie, Gibson-Bruck, and Tau-Leap stochastic algorithms. Di
zzy is capable of importing and exporting the SBML model definition language, as well as displaying models gra
phically using the Cytoscape software system.

Dizzy was written by Stephen Ramsey in the laboratory of Hamid Bolouri at ISB. Dizzy is based on the ISBJava l
ibrary.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_DIZZY

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
# Unpack source
# This will unpack the source to /tmp/BUILD/***
#%setup -n %{name}-%{version}
%setup -n Dizzy

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install
#mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
#make DESTDIR=$RPM_BUILD_ROOT install

# Start with a clean environment

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
cp -rp ./bin ./config ./docs ./lib ./samples $RPM_BUILD_ROOT%{INSTALL_DIR}

# the runmodel.sh by default defines INSTALL_DIR=.. and lib is assumed in the path ${INSTAL_DIR}/lib. However when the module is loaded, pwd does not equal to the dir where the module is actually installed. Thus, the INSTALL_DIR has to be changed to the real install dir e.g. /opt/apps/

cd $RPM_BUILD_ROOT%{INSTALL_DIR}/bin
sed -e s'@INSTALL_DIR=..@INSTALL_DIR=%{INSTALL_DIR}@' -i runmodel.sh


rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with java.
This module makes available the dizzy executable. Documentation for %{name} is available online at the publisher\'s website: http://magnet.systemsbiology.net/software/Dizzy/
The dizzyexecutable can be found in %{MODULE_VAR}_DIR
Version %{version}
]])

whatis("Name: dizzy")
whatis("Version: %{version}")
whatis("Category: computational biology, chemical kinetics")
whatis("Keywords:  Biology, Genomics, chemical kinetics, stochastic simulation")
whatis("Description: dizzy -chemical kinetics stochastic simulation software package written in Java.")
whatis("URL: http://magnet.systemsbiology.net/software/Dizzy/")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")


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

