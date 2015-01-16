#export RPM_BUILD_DIR=/home1/0000/build/rpms/
Summary:    root - set of OO frameworks which help analyze large data efficiently 
Name:       root
Version:    5.34.14
Release:    1
License:    LGPL License
Group: Applications/Life Sciences
Source:     %{name}_v5.34.13.source.tar.gz
Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
%include ../system-defines.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define PNAME root

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
MAKER is a portable and easily configurable genome annotation pipeline. It's purpose is to allow smaller eukaryotic and prokaryotic genome projects to independently annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab-initio gene predictions and automatically synthesizes these data into gene annotations having evidence-based quality values. 
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_ROOT
#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}

%build   
%install
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include ../system-load.inc          
    
# Load additional modules here (as needed)
module purge 
module load TACC
module swap intel gcc

CWD=`pwd`
unset ROOTSYS
#./configure --prefix=%{INSTALL_DIR} --etcdir=%{INSTALL_DIR}/etc/root --disable-rfio --disable-ldap --disable-xrootd --disable-krb5 --disable-ssl
./configure --prefix=%{INSTALL_DIR} --etcdir=%{INSTALL_DIR}/etc/root --all
make -j4
make DESTDIR=$RPM_BUILD_ROOT install

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The ROOT system provides a set of OO frameworks with all the functionality needed to handle and analyze large amounts of data in a very efficient way. Having the data defined as a set of objects, specialized storage methods are used to get direct access to the separate attributes of the selected objects, without having to touch the bulk of the data. 

To run it, no need to source thisroot.sh beforehand, since all the relevant paths are loaded. 
Version %{version}
]])

whatis("Name: root")
whatis("Version: %{version}")
whatis("Category: imaging")
whatis("Keywords:  OO, simulation, data analysis, libraries")
whatis("Description: Root -- a set of OO frameworks with all the functionality needed to handle and analyze large amounts of data in a very efficient way") 
whatis("http://root.cern.ch/drupal/")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv ("ROOTSYS",                "%{INSTALL_DIR}")
prepend_path("LD_LIBRARY_PATH",   "%{INSTALL_DIR}/lib/root")
prepend_path("DYLD_LIBRARY_PATH", "%{INSTALL_DIR}/lib/root")
prepend_path("SHLIB_PATH",        "%{INSTALL_DIR}/lib/root")
prepend_path("LIBPATH",           "%{INSTALL_DIR}/lib/root")
prepend_path("PYTHONPATH",        "%{INSTALL_DIR}/lib/root")
prepend_path("MANPATH",           "%{INSTALL_DIR}/share/man/man1")

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

