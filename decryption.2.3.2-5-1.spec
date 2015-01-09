Summary: NCBI decryption tools
Name: decryption
<<<<<<< HEAD
Version: 2.3.2
Release: 5
=======
Version: 2.3.2-5
Release: 2
>>>>>>> d6c1cb5b22b254f6ee31c6ffe8d7d3f5d30772bf
License: Public Domain
Vendor: National Center for Biotechnology Information
Group: Applications/Life Sciences
Source: decryption.2.3.2-5-centos_linux64.tar.gz
<<<<<<< HEAD
#Source0:  %{name}.%{version}-%{release}-centos_linux64.tar.gz
=======
>>>>>>> d6c1cb5b22b254f6ee31c6ffe8d7d3f5d30772bf
Packager: TACC - wonaya@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include rpm-dir.inc
%include ../system-defines.inc

%define PNAME %{name}

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
<<<<<<< HEAD
%define MODULE_VAR TACC_SRATOOLKIT
=======
%define MODULE_VAR TACC_DECRYPTION
>>>>>>> d6c1cb5b22b254f6ee31c6ffe8d7d3f5d30772bf

%description
Subset of the SRA toolkit that includes only the utilities related to decryption

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n %{name}.%{version}-%{release}-centos_linux64

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

echo "Decryption Tool is distributed as compiled binary for Centos 64bit. No compilation necessary."

module unload python

cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME} distribution.

Version %{version}
]]
)

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing, NCBI, SRA")
whatis("URL: http://www.ncbi.nlm.nih.gov/Traces/sra/?view=software")
whatis("Description: Decryption tool is a subset of SRA Toolkit for decrypting the encrypted non-SRA data")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

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

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT