# $Id$

Summary: BioPerl is a toolkit of perl modules useful in building bioinformatics solutions in Perl.
Name: bioperl
Version: 1.6.901
Release: 1
License: GPL
Group: Libraries/Life Sciences 
Source0:  BioPerl-%{version}.tar.gz
Packager: vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME bioperl
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_BIOPERL

%description

%prep
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

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

