#
# $Id: metis.spec 507 2011-01-13 05:16:09Z karl $
#
 
Summary: Local Shrimp binary install
 
#
#
#

Name: shrimp 
Version: 2.0.2 
License: GPLv2
Release: 1
Group: Applications/Life Sciences 
Source: shrimp-2.0.2.tar.gz
Packager: TACC - bdkim@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc
%include compiler-defines.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary: Local Shrimp binary install
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

SHRiMP2 is a software package for mapping reads from a donor genome against a
target (refernce) genome. SHRiMP2  was primarily developed to work  with short
reads produced by Next Generation Sequencing (NGS)  machines.

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
 
##
## SETUP
##

%setup
 
##
## BUILD
##

%build

%include compiler-load.inc

%if "%{is_intel}" == "1" || "%{is_intel10}" == "1" || "%{is_intel11}" == "1"

	# environment used for configure with intel compiler

        # export OPTFLAGS="OPTFLAGS = -O3 -fPIC"

%endif

%if "%{is_gcc44}" == "1"

	# environment used for configure with intel compiler
        # export OPTFLAGS="OPTFLAGS = -O3"
%endif

make
cp -rp * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#mkdir %{INSTALL_DIR}/bin
#cp bin/* %{INSTALL_DIR}/bin/
#%install

 
## Module for Shrimp 

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[

The %{name} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_BIN for the location of
the %{name} distribution and binaries, respectively.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: SHRiMP")
whatis("Version: %{version}")
whatis("Category: Application, Biology")
whatis("Keywords: Biology, Genomics, Assembly")
whatis("URL: http://compbio.cs.toronto.edu/shrimp")
whatis("Description: a software package for mapping reads from a donor genome against a target genome.")

local shrimp_dir="%{INSTALL_DIR}"

setenv("TACC_SHRIMP_DIR",shrimp_dir)
setenv("TACC_SHRIMP_BIN",pathJoin(shrimp_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for GROMACS
##

set     ModulesVersion      "%version"
EOF


%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}


%post
%clean
rm -rf $RPM_BUILD_ROOT





