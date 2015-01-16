# $Id$

Summary: libgtextutils - Gordon-Text_utils-Library
Name: libgtextutils
Version: 0.6
Release: 2
License: GPL
Group: Libraries/Life Sciences 
Source0:  libgtextutils-%{version}.tar.bz2
Packager: vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME libgtextutils
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_LIBGTEXTUTILS

%description

%prep
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version}

%build


if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
module load TACC

./configure --prefix=%{INSTALL_DIR}
make

%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install


CWD=`pwd`
cd $RPM_BUILD_ROOT%{INSTALL_DIR}/include/gtextutils/gtextutils
mv * ../
cd ../
rmdir gtextutils
cd $CWD

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_LIB, %{MODULE_VAR}_INC and %{MODULE_VAR}_SHARE for the location of the %{PNAME}
distribution.

Version %{version}
]]
)

whatis("Name: libgtextutils")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics")
whatis("URL: http://hannonlab.cshl.edu/fastx_toolkit/download.html")
whatis("Description: Gordon-Text_utils-Library")


prepend_path("LD_LIBRARY_PATH",              "%{INSTALL_DIR}/lib")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")
setenv (     "%{MODULE_VAR}_INC", "%{INSTALL_DIR}/include")
setenv (     "%{MODULE_VAR}_SHARE", "%{INSTALL_DIR}/share")

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

