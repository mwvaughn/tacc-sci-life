# $Id$

%define PNAME bioperl
Summary: BioPerl is a toolkit of perl modules useful in building bioinformatics solutions in Perl.
Version: 1.6.901
Release: 2
License: GPL
Group: Libraries/Life Sciences
Source:  http://bioperl.org/DIST/BioPerl-1.6.1.tar.gz
Packager: vaughn@tacc.utexas.edu
Prefix: /opt/apps

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}BIOPERL

%description
BioPerl is a community effort to produce Perl code which is useful in biology.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%setup -n BioPerl-%{version}

%build


if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
module load TACC



mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

mkdir %{INSTALL_DIR}/Bio
cp -R Bio/* %{INSTALL_DIR}/Bio/

cp -rp %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

umount %{INSTALL_DIR}

%install
#done


#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables: %{MODULE_VAR}_DIR, PERL5LIB

Version %{version}
]]
)

whatis("Name: BioPerl")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics")
whatis("URL: http://www.bioperl.org/")
whatis("BioPerl is a toolkit of perl modules useful in building bioinformatics solutions in Perl.")


prepend_path("PATH",              "%{INSTALL_DIR}/bio")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "PERL5LIB",	  "%{INSTALL_DIR}")

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

