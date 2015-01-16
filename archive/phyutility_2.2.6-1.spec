Summary: phyutility is a java utility to analyze and modify phylogenetic trees
Name: phyutility
Version: 2.2.6
Release: 1
License: GPLv3
Vendor: Stephen Smith and Casey Dunn
Group: Applications/Life Sciences
Source: phyutility_2_2_6.tar.gz
Packager: TACC - mattcowp@tacc.utexas.edu
#Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include ../rpm-dir.inc
%include ../system-defines.inc

%define debug_package %{nil}

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_PHYUTILITY

%description
Phyutility is a command line program that performs simple analyses or modifications on both trees and data matrices. 
%prep
rm -rf  $RPM_BUILD_ROOT/%INSTALL_DIR

%setup -n phyutility

%build

%install

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT/%INSTALL_DIR/bin
pwd

cp -r * $RPM_BUILD_ROOT/%INSTALL_DIR/bin
### Edit phyutility to reflect installation directory

#sed -i -e 's@INSTALL_DIR@%{INSTALL_DIR}/bin@' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/phyutility
/bin/rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/phyutility
echo "java -Xmx2g -jar %{INSTALL_DIR}/bin/phyutility.jar \$\*" > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/phyutility

#
#
chmod -R a+rX $RPM_BUILD_ROOT/%INSTALL_DIR

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%MODULE_DIR
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
The phyutility modulefile defines the following environment variables,
TACC_PHYUTILITY_DIR and TACC_PHYUTILITY_BIN for the location of the 
phyutility directory and binary.  The modulefile also appends 
TACC_PHYUTILITY_BIN directory to PATH.

To load the phyutility module, use this command:

module load phyutility

Version %{version}
]])


whatis("Name: phyutility")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Genomics, Phylogentics")
whatis("URL:  http://code.google.com/p/phyutility/")
whatis("Description: phyutility - Program to manipulate phylogenetic trees")

setenv("%{MODULE_VAR}_DIR"       ,"%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN"      ,"%{INSTALL_DIR}/bin")

prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
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
rm -rf $RPM_BUILD_ROOT
