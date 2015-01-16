Summary:    autodock -- a suite of automated docking tool
Name:       autodock
#4.2.5 incorrectly calculates desolvation energy. corrected in 4.2.5.1
Version:    4.2.5.1
Release:    1
License:    GNU General Public License
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
#%include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
%include ../system-defines.inc
%define PNAME autodock

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
#%package -n %{name}-%{comp_fam_ver}
#Summary: HMMER biosequence analysis using profile hidden Markov models
#Group: Applications/Life Sciences

%description
#%description -n %{name}-%{comp_fam_ver}
Geant4 is a toolkit for simulating the passage of particles through matter. It includes a complete range of functionality including tracking, geometry, physics models and hits. The physics processes offered cover a comprehensive range, including electromagnetic, hadronic and optical processes, a large set of long-lived particles, materials and elements, over a wide energy range starting, in some cases, from  and extending in others to the TeV energy range. It has been designed and constructed to expose the physics models utilised, to handle complex geometries, and to enable its easy adaptation for optimal use in different sets of applications. The toolkit is the result of a worldwide collaboration of physicists and software engineers. It has been created exploiting software engineering and object-oriented technology and implemented in the C++ programming language. It has been used in applications in particle physics, nuclear physics, accelerator design, space engineering and medical physics.
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_AUTODOCK

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build   
          
#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

%include ../system-load.inc

module purge
module load TACC

cd autodock
./configure --prefix=%{INSTALL_DIR}
make CC=icc

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install


# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module makes available the autodock executable. Documentation for %{name} is available online at the publisher\'s website: http://autodock.scripps.edu/

Version %{version}
]])

whatis("Name: autodock")
whatis("Version: %{version}")
whatis("Category: computational chemistry, docking")
whatis("Keywords:  Docking, Virtual Screening, Drug Discovery, Ligand protein, Biology")
whatis("Description: autodock - a suite of automated docking tools. It is designed to predict how small molecules, such as substrates or drug candidates, bind to a receptor of known 3D structure.")
whatis("URL: http://autodock.scripps.edu/")

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
#%files -n %{name}-%{comp_fam_ver}
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

