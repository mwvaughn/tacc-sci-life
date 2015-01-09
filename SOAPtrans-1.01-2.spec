Summary:    SOAPdenovo-Trans
Name:       soaptrans
Version:    1.01
Release:    2
License:    Unknown
Vendor:     BGI
Group: Applications/Life Sciences
Source:     SOAPdenovo-Trans_1.01.tar
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
#BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

# work around ERROR: No build ID note found
%global debug_package %{nil}

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define PNAME %{name}

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_SOAPTRANS

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
%setup -n SOAPdenovo-Trans

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

cp -rp ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name}. SOAPdenovo-Trans is a de novo transcriptome assembler 
basing on the SOAPdenovo framework, adapt to alternative splicing and different 
expression level among transcripts.The assembler provides a more accurate, 
complete and faster way to construct the full-length transcript sets.

Please note:
- SOAPdenovo-Trans-31kmer supports kmers 31 in length or less
- SOAPdenovo-Trans-127mer supports kmers 127 in length or less but requires several fold more RAM

Version %{version}
]])

whatis("Name: SOAPdenovo-Trans")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly")
whatis("Description: de novo transcriptome assembler basing on the SOAPdenovo")
whatis("URL: http://soap.genomics.org.cn/SOAPdenovo-Trans.html")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

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

