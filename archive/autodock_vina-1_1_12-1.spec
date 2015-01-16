# $Id$

Summary: AutoDock Vina
Name: autodock_vina
Version: 1_1_2
Release: 1
License: Apache License V2.0
Group: Applications/Life Sciences 
Source0:  autodock_vina_%{version}.tgz
Packager: jfonner@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%include rpm-dir.inc

%define PNAME autodock_vina
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_AUTODOCK_VINA

%description

%prep

%setup -n %{PNAME}_%{version}

%build


if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER intel 
module load boost

#./configure CC=gcc --prefix=%{INSTALL_DIR}
cd ./build/linux/release
make depend
make
#make DESTDIR=$RPM_BUILD_ROOT install

%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}/bin
cp ./build/linux/release/vina ./build/linux/release/vina_split $RPM_BUILD_ROOT%{INSTALL_DIR}/bin
chmod -R a+rx $RPM_BUILD_ROOT%{INSTALL_DIR}/bin

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_BIN for the location of the %{PNAME}
distribution.

Version %{version}
]]
)

whatis("Name: AutoDock Vina")
whatis("Version: %{version}")
whatis("Category: computational biology, structural biology")
whatis("Keywords: Biology, Chemistry, Structural Biology, Docking")
whatis("URL: http://vina.scripps.edu/")
whatis("Description: Open-source program for drug discovery, molecular docking and virtual screening, offering multi-core capability, high performance and enhanced accuracy and ease of use.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

prereq ("boost", "intel")

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

