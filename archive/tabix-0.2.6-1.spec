# $Id$

Summary: Tabix - Indexes a tab-delimited genome position file in.tab.bgz and creates an index file
Name: tabix
Version: 0.2.6
Release: 1
License: GPL
Group: Applications/Life Sciences
Source0:  tabix-%{version}.tar.bz2
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%include rpm-dir.inc

%define PNAME tabix
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_SAMTOOLS

%description
Indexes a tab-delimited genome position file in.tab.bgz and creates an index file.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include

%setup -n %{PNAME}-%{version}

%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC

#-----------------------------
# Build parallel version
#-----------------------------

make CC=icc CXX=icpc

%install

cp -R perl/ python/ tabix tabix.py TabixReader.java bgzip NEWS $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_INC, and %{MODULE_VAR}_LIB 
associated with %{PNAME}

Version %{version}
]]
)

whatis("Name: Tabix")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Quality Control, Utility, Sequencing, Genotyping, Resequencing, SNP")
whatis("URL: http://samtools.sourceforge.net/")
whatis("Description: Indexes a tab-delimited genome position file in.tab.bgz and creates an index file.")


prepend_path("PATH",              "%{INSTALL_DIR}")
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

