#
# Spec file for phyutility
#
Summary: phyutility is java utility to analyze and modify phylogenetic trees
Name: phyutility
Version: 2.2.4
Release: 1
License: GPL3
Group: Applications/Life Sciences
Source: phyutility_2_2_4.tar.gz
Packager: TACC - gendlerk@tacc.utexas.edu

%include rpm-dir.inc
%define _unpack_name phyutility_2_2_4

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%define PKG_INSTALL_DIR /opt/apps/%{name}/%{version}
%define MOD_INSTALL_DIR /opt/apps/modulefiles/%{name}

# %define licenses ddt-license
# BuildRoot: /tmp/%{name}-%{version}-buildroot
%description

Phyutility is a command line program that performs simple analyses or modifications on both trees and data matrices. 

%package -n %{name}-modulefile
Summary: Module file for %{name}
Group: Applications/Life Sciences
%description -n %{name}-modulefile
Module file for %{name}

%prep
rm -rf  $RPM_BUILD_ROOT/%INSTALL_DIR
mkdir -p $RPM_BUILD_ROOT/%INSTALL_DIR/bin
pwd

%setup -n phyutility_2_2_4

%build

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
### Edit phyutility to reflect installation directory

sed -i -e 's@INSTALL_DIR@%{INSTALL_DIR}/bin@' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/phyutility

#
#
chmod -R a+rX $RPM_BUILD_ROOT/%INSTALL_DIR

## Module for phyutility
rm -rf  $RPM_BUILD_ROOT/%MODULE_DIR
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The phyutility modulefile defines the following environment variables,
TACC_PHYUTILITY_DIR and TACC_PHYUTILITY_BIN for the location of the 
phyutility directory and binary.  The modulefile also appends 
TACC_PHYUTILITY_BIN directory to PATH.

Since this utility is based on Java, it requires the 64-bit Java 
module to be loaded. To load the phyutility module, use this command:

module load jdk64 phyutility

Version %{version}
]]

help(help_message,"\n")

whatis("Name: phyutility")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Genomics, Phylogentics, ")
whatis("URL:  http://code.google.com/p/phyutility/")
whatis("Description: Program to manipulate phylogenetic trees")

-- Prerequisites
prereq("jdk64")

setenv("TACC_PHYUTILITY_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_PHYUTILITY_BIN"      ,"%{INSTALL_DIR}/bin")

prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for phyutility
##
 
set     ModulesVersion      "%{version}"
EOF

%files
%defattr(-,root,root)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
