#
# siesta-3.1.spec, v3.1, 2011-09-08 11:59:00 carlos@tacc.utexas.edu
#
# See http://www.icmab.es/siesta/

Summary:    HMMER biosequence analysis using profile hidden Markov models
Name:       hmmer
Version:    3.0
Release:    1
License:    GPLv3
Vendor:     Howard Hughes Medical Institute
Group:      ComputationalBiology/genomics	
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jfonner@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
%include compiler-defines.inc
# MPI Family Definitions
%include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: HMMER biosequence analysis using profile hidden Markov models
Group:   Applications/Biology

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
HMMER is used for searching sequence databases for homologs of protein 
sequences, and for making protein sequence alignments. It implements 
methods using probabilistic models called profile hidden Markov models 
(profile HMMs).

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR TACC_HMMER

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/hmmer-3.0
%setup -n %{name}-%{version}

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
%include compiler-load.inc
# Load correct mpi stack
%include mpi-load.inc
%include mpi-env-vars.inc
# Load additional modules here (as needed)

./configure MPICC=mpicc CC=icc CXX=icpc --prefix=%{INSTALL_DIR} --enable-mpi CFLAGS=" -O3 -ansi_alias -fPIC"
make

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install
cp -r ./documentation $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r ./tutorial $RPM_BUILD_ROOT/%{INSTALL_DIR}


# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with Intel 11.1.
This module makes available the following executables:

hmmalign
hmmbuild
hmmconvert
hmmemit
hmmfetch
hmmpress
hmmscan
hmmsearch
hmmsim
hmmstat
jackhmmer
phmmer

Manual pages are available under %{MODULE_VAR}_MAN and tutorial files are can be found in %{MODULE_VAR}_DIR/tutorial

Version %{version}
]])

whatis("Name: HMMER")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Bioinformatics, Genomics")
whatis("Description: HMMER biosequence analysis using profile hidden Markov models") 
whatis("URL: http://hmmer.janelia.org/")

setenv("TACC_HMMER_DIR","%{INSTALL_DIR}/")
setenv("TACC_HMMER_BIN","%{INSTALL_DIR}/bin")
setenv("TACC_HMMER_MAN","%{INSTALL_DIR}/documentation/man")
prepend_path("PATH"    ,"%{INSTALL_DIR}/bin")
prepend_path("MANPATH" ,"%{INSTALL_DIR}/documentation/man")

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

