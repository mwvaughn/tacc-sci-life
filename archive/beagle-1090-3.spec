#
# beagle-1090.spec, v1090, 2012-09-18 11:59:00 carlos@tacc.utexas.edu
#
# See http://code.google.com/p/beagle-lib/

Summary:    High performance library for Bayesian and Maximum Likelihood phylogenetic packages
Name:       beagle
Version:    1090
Release:    3
License:    LGPD
Vendor:     Multiple
Group: Libraries/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - carlos@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and local build root
%include rpm-dir.inc
# Compiler and MPI Family Definitions
%include compiler-defines.inc
# Other definitions
%define APPS    /opt/apps
%define MODULES modulefiles

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
%package -n %{name}-%{comp_fam_ver}
Summary: Library for Bayesian and Maximum Likelihood phylogenetic packages
Group: Libraries/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}-%{comp_fam_ver}
BEAGLE is a high-performance library that can perform the core calculations at the heart of most Bayesian and Maximum Likelihood phylogenetics packages. It can make use of highly-parallel processors such as those in graphics cards (GPUs).

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/scalasca-1.1
%setup 

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

module purge
%include compiler-load.inc
module load jdk64 cuda

./autogen.sh
./configure --prefix=%{INSTALL_DIR} --with-cuda=$TACC_CUDA_DIR --with-jdk=$TACC_JDK64_DIR


 make

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

 mkdir -p     $RPM_BUILD_ROOT/%{INSTALL_DIR}
 make DESTDIR=$RPM_BUILD_ROOT install

# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
-- Module file for the beagle library
local help_message = [[
This module loads the Beagle library built with %{comp_fam} and %{mpi_fam}.

Beagle is a high-performance library that can perform the core calculations 
at the heart of most Bayesian and Maximum Likelihood phylogenetics packages. 
It can make use of highly-parallel processors such as those in graphics 
cards (GPUs).

The TACC_BEAGLE_DIR, TACC_BEAGLE_INC and TACC_BEAGLE_LIB environmental
variables have been defined for convenience.

For additional information go to http://code.google.com/p/beagle-lib/

Current build is based on the SVN revision %{version}.
]]

whatis("Name: Beagle")
whatis("Version: %{version}")
whatis("Category: library, biology, phylogenetics")
whatis("Keywords: Maximum Likelihood, Bayesian, Phylogenetics, GPU")
whatis("High performance library for Bayesian and Maximum Likelihood phylogenetic packages")
whatis("URL: http://code.google.com/p/beagle-lib/")

help(help_message,"\n")

--# Export environmental variables
setenv("TACC_BEAGLE_DIR","%{INSTALL_DIR}")
setenv("TACC_BEAGLE_INC","%{INSTALL_DIR}/include")
setenv("TACC_BEAGLE_LIB","%{INSTALL_DIR}/lib")

--# Prepend the scalasca directories to the adequate PATH variables
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

prereq("cuda","jdk64")

EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}-%{comp_fam_ver}

# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the source files from /tmp/BUILD
rm -rf /tmp/BUILD/%{name}-%{version}

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

