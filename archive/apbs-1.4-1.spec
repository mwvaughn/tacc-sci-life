Summary:    Adaptive Poisson-Boltzmann Solver (APBS) -- Software for evaluating the electrostatic properties of nanoscale biomolecular systems
Name:       apbs
Version:    1.4
Release:    1
License:    Copyright (c) 2010.  Pacific Northwest National Laboratory
Vendor:     Pacific Northwest National Laboratory
Group:      ComputationalBiology/Chemistry
Source:     http://downloads.sourceforge.net/project/apbs/apbs/apbs-1.4.0/APBS-%{version}-source.tar.gz
Packager:   TACC - jfonner@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
#%include compiler-defines.inc
# MPI Family Definitions
#%include mpi-defines.inc
# Other defs

%define PNAME apbs
%define MODULE_VAR TACC_APBS

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: Adaptive Poisson-Boltzmann Solver (APBS) -- Software for evaluating the electrostatic properties of nanoscale biomolecular systems 
Group:   Applications/Biology

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
APBS is a software package for modeling biomolecular solvation through solution 
of the Poisson-Boltzmann equation (PBE), one of the most popular continuum 
models for describing electrostatic interactions between molecular solutes in 
salty, aqueous media.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
#%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
#%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}
%define INSTALL_DIR %{APPS}/intel13/mvapich2_1_9/%{name}/%{version}
%define MODULE_DIR  %{APPS}/intel13/mvapich2_1_9/%{MODULES}/%{name}

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
#%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load correct compiler
#%include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)
module purge
module load TACC
module load python
module load cmake

# I don't think I have to do the tmpfs trink since APBS moved to cmake
# I have to use the tmpfs trick.  Destdir is broken for some reason. Bad source code.
#mkdir -p             %{INSTALL_DIR}
#tacctmpfs -m         %{INSTALL_DIR}
# mount -t tmpfs tmpfs %{INSTALL_DIR}
#cd                   %{INSTALL_DIR}


# this may not be the most graceful way to do it, but I don't want the compiled
# executables and libraries to get mixed in with the source code. I make a 
# directory called foo and specify it as the prefix.
#mkdir ./foo

#./configure --with-mpich2=$MPICH_HOME --prefix=%{INSTALL_DIR}/foo --enable-python CC=mpicc CXX=mpixx
cd build
CC=icc CXX=icpc cmake .. -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} -DENABLE_MPI=ON
make CC=icc CXX=icpc
make DESTDIR=$RPM_BUILD_ROOT install

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------


#cp -r %{INSTALL_DIR}/doc      $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r %{INSTALL_DIR}/examples $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r %{INSTALL_DIR}/tools    $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cd                                            %{INSTALL_DIR}/foo
#cp   -rp ./*                  $RPM_BUILD_ROOT/%{INSTALL_DIR}
#chmod -Rf u+rwX,g+rwX,o=rX    $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cd                            $RPM_BUILD_ROOT
#tacctmpfs -u                                  %{INSTALL_DIR}


# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads an MPI-compiled version of APBS built with intel11 and 
mvapich2.  Python wrappers were also built and require the python module to 
run correctly.

The directory %{MODULE_VAR}_BIN is added to the path, and %{MODULE_VAR}_DIR, 
%{MODULE_VAR}_DOC,  and %{MODULE_VAR}_TOOLS are added to the environment for 
convenience. Example files are also in %{MODULE_VAR}_DIR.

More information on APBS is available at http://www.poissonboltzmann.org/apbs.

Version %{version}
]])

whatis("Name: APBS")
whatis("Version: %{version}")
whatis("Category: computational biology, chemistry,")
whatis("Keywords: Chemistry, Biology")
whatis("Description: Adaptive Poisson-Boltzmann Solver (APBS) -- Software for evaluating the electrostatic properties of nanoscale biomolecular systems") 
whatis("URL: http://www.poissonboltzmann.org/apbs")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_DOC","%{INSTALL_DIR}/doc")
setenv("%{MODULE_VAR}_TOOLS","%{INSTALL_DIR}/tools")
prepend_path("PATH"    ,"%{INSTALL_DIR}/bin")

EOF

#------------------------------------------------
#  Version file.
#------------------------------------------------

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
%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}

# Define files permisions, user and group
%defattr(-,root,root,-)
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

