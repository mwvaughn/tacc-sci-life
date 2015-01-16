# $Id$

Summary: AutoDock Vina
Name: autodock_vina
Version: 1.1.2
Release: 1
License: Apache License V2.0
Group: Applications/Life Sciences 
Source0:  autodock_vina_1_1_2.tgz
Patch1:     %{name}-%{version}.patch
Packager: jfonner@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%include rpm-dir.inc
%include ../system-defines.inc

%define PNAME autodock_vina
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_AUTODOCK_VINA

%description

%prep

%setup -n %{PNAME}_1_1_2

# Made minor changes so vina would work with Blast filesystem version 3.
# There is precedent for these changes here: http://mgl.scripps.edu/forum/viewtopic.php?f=12&t=2153
%patch1 -p2

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER intel 
module load boost
MY_BOOST_VERSION=$(basename $TACC_BOOST_DIR)

cd ./build/linux/release

%if "%{PLATFORM}" == "stampede"
  # "makedepend" is not on Stampede.  I used "-MMD" in CPPFLAGS to try to make all the dependencies. It looks like it worked
  make GPP=icpc BASE=$TACC_BOOST_DIR BOOST_VERSION=$MY_BOOST_VERSION CPPFLAGS="$CPPFLAGS -MMD" LDFLAGS="-L$TACC_BOOST_LIB" LIBS="-Wl,-Bstatic -lboost_system -lboost_thread -lboost_serialization -lboost_filesystem -lboost_program_options -Wl,-Bdynamic" C_PLATFORM="-pthread"
%endif

%if "%{PLATFORM}" == "lonestar"
  make GPP=icpc BASE=$TACC_BOOST_DIR BOOST_VERSION=$MY_BOOST_VERSION CPPFLAGS="$CPPFLAGS -MMD" LDFLAGS="-L$TACC_BOOST_LIB" LIBS="-lboost_system -lboost_thread -lboost_serialization -lboost_filesystem -lboost_program_options" C_PLATFORM="-static -pthread"
%endif

%if %{undefined PLATFORM}
  make depend
  make
%endif

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}/bin
cp ./vina ./vina_split $RPM_BUILD_ROOT%{INSTALL_DIR}/bin
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
whatis("Category: life sciences, computational biology, structural biology")
whatis("Keywords: Biology, Chemistry, Structural Biology, Docking")
whatis("URL: http://vina.scripps.edu/")
whatis("Description: Open-source program for drug discovery, molecular docking and virtual screening, offering multi-core capability, high performance and enhanced accuracy and ease of use.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
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

