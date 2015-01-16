# $Id$

Summary: NCBI BLAST+ sequence alignment package. The program compares nucleotide or protein sequences to sequence databases and calculates the statistical significance of matches.
Name: blast
Version: 2.2.29
Release: 1 
License: GPL
Group: Applications/Life Sciences
Source: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.2.29+-x64-linux.tar.gz
Packager: vaughn@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME blast
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_BLAST

%description

%prep
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n ncbi-%{PNAME}-%{version}+

%build

%install

echo "ncbi-blast-%{version} was distributed as a compiled binary. We do not compile it from source."

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

%include ../system-load.inc
module purge
module load TACC

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
%{MODULE_VAR}_DIR and %{MODULE_VAR}_BIN, %{MODULE_VAR}_LIB and %{MODULE_VAR}_INC for the location of the %{PNAME}
distribution.

Version %{version}
]]
)

whatis("Name: NCBI BLAST+")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment")
whatis("URL: http://www.ncbi.nlm.nih.gov/BLAST")
whatis("Description: NCBI BLAST+ sequence alignment package. The program compares nucleotide or protein sequences to sequence databases and calculates the statistical significance of matches.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

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

