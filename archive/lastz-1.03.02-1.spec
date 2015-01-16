# $Id$

Summary: LASTZ - Fast, long sequence aligner
Name: lastz
Version: 1.03.02
Release: 1
License: Unknown
Group: Applications/Life Sciences
Source:  http://www.bx.psu.edu/~rsharris/lastz/newer/lastz-1.03.02.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

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

%define MODULE_VAR TACC_LASTZ

%description
LASTZ is a program for aligning DNA sequences, a pairwise aligner. Originally designed to handle sequences the size of human chromosomes and from different species, it is also useful for sequences produced by NGS sequencing technologies such as Roche 454.

%prep
rm   -rf $RPM_BUILD_ROOT

%setup -n %{name}-distrib-%{version}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC

make

cp -R bin tools test_data *.html test_results images $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp src/lastz $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

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

whatis("Name: LASTZ")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Aligner")
whatis("URL: http://www.bx.psu.edu/~rsharris/lastz/")
whatis("Description: An efficient pairwise aligner")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("PATH",              "%{INSTALL_DIR}/tools")
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
