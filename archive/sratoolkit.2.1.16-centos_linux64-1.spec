# $Id$

# SRA Toolkit is distributed compiled by NCBI and does not built easily
# http://ftp-private.ncbi.nlm.nih.gov/sra/sdk/2.1.16/sratoolkit.2.1.16-centos_linux64.tar.gz

Summary: SRA Toolkit
Name: sratoolkit
Version: 2.1.16
Release: 1
License: Public Domain
Vendor: National Center for Biotechnology Information
Group: Applications/Life Sciences
Source0:  %{name}.%{version}-centos_linux64.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME sratoolkit
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_SRATOOLKIT

%description
The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}.%{version}-centos_linux64

%build

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi


module purge
module load TACC

echo "SRA Toolkit is distributed as compiled binary for Centos 64bit. No compilation necessary."

%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
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

whatis("Name: NCBI SRA Toolkit")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing, NCBI, SRA")
whatis("URL: http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=software")
whatis("Description: The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.")

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

