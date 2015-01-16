## http://www.broadinstitute.org/igv/projects/downloads/igvtools_2.3.9.zip

Summary: IGVTools
Name: igvtools
Version: 2.3.26
Release: 1
License: MIT License
Vendor: Broad Institute
Group: Applications/Life Sciences
Source: igvtools_2.3.26.zip
Packager: TACC - wonaya@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include ../rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME igvtools
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_IGVTOOLS

%description
The Integrative Genomics Viewer (IGV) is a high-performance visualization tool for interactive exploration of large, integrated genomic datasets. IGVtools is for preprocessing data files

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n IGVTools
%build
%install
%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

echo "IGVtools is distributed as compiled binary for Centos 64bit. No compilation necessary."

cp -R genomes igvtools igvtools.* igvtools_* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------
# Modules Section
#-----------------

module unload python

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
whatis("Keywords: Biology, Genomics, Viewer")
whatis("URL: http://www.broadinstitute.org/igv/home")
whatis("Description: The Integrative Genomics Viewer (IGV) is a high-performance visualization tool for interactive exploration of large, integrated genomic datasets. IGVtools is for preprocessing data files")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

prereq ("jdk64")

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