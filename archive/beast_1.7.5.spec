## BEAST
Summary: BEAST - a program for Bayesian MCMC of Evolution and Phylogenetics using Molecular Sequences
Name: beast
Version: 1.7.5
Release: 1
License: GNU Lesser GPL
Group: Applications/Life Sciences
Source: BEASTv1.7.5.tgz
Packager: TACC - mattcowp@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include ../rpm-dir.inc
%include ../system-defines.inc

%description
BEAST is a a program for Bayesian MCMC of Evolution & Phylogenetics using Molecular Sequences. This module provides the following binaries: beast, beauti, beastMC3, loganalyser, logcombiner, treeannotator, and treestat.

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BEAST

%prep
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n BEASTv1.7.5

%build
%include ../system-load.inc

module purge
module load TACC

# compile shared object file
# module load intel
echo "Compiling shared object file with icc."
cd native
rm *.so
export JAVA_HOME=/usr/java/latest
make -f Makefile.icc
cd ..

%install



#copy into install dir
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/native/*.c
rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/native/*.h

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The BEAST modulefile defines the following environment variables,
TACC_BEAST_DIR, and TACC_BEAST_BIN for the location of the beast directory and 
binaries.

The modulefile also prepends TACC_BEAST_BIN directory to PATH

Version %{version}
]]
)

whatis("Name: BEAST")
whatis("Version: %{version}")
whatis("Category: application, biology, phylogenetics")
whatis("Keyword: Biology, Application, Alignment, Phylogenetics, 2012Q3")
whatis("URL:  http://code.google.com/p/beast-mcmc/")
whatis("Description: Tool for Bayesian MCMC analysis of molecular sequences")

-- Prerequisites

setenv( "TACC_BEAST_DIR", "%{INSTALL_DIR}" )
setenv( "TACC_BEAST_BIN", "%{INSTALL_DIR}/bin" )

prepend_path("PATH","%{INSTALL_DIR}/bin")

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
