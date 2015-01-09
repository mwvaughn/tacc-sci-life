#
# Spec file for BEAST
#
Summary:   BEAST - a program for Bayesian MCMC of Evolution & Phylogenetics using Molecular Sequences
Name:      beast
Version:   1.7
Release:   1
License:   GNU Lesser GPL
Group: Applications/Life Sciences
Source:    BEASTv1.7.0.tgz
Packager:  TACC - gendlerk@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   BEAST - a program for Bayesian MCMC of Evolution & Phylogenetics using Molecular Sequences
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

BEAST is a a program for Bayesian MCMC of Evolution & Phylogenetics using Molecular Sequences

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#%setup -n %{name}-%{version}
%setup -n BEASTv1.7.0

%build
%include compiler-load.inc

# Use mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}

%install
%include compiler-load.inc

mkdir -p  $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r ./* %{INSTALL_DIR}
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount                                   %{INSTALL_DIR}


## Module for beast
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The BEAST modulefile defines the following environment variables,
TACC_BEAST_DIR, and TACC_BEAST_BIN for the location of the beast directory and 
binaries.

The modulefile also prepends TACC_BEAST_BIN directory to PATH

Version %{version}
]]

help(help_message,"\n")

whatis("Name: BEAST")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keyword: Biology, Application, Alignment, Phylogenetics")
whatis("URL:  http://code.google.com/p/beast-mcmc/")
whatis("Description: Tool for Bayesian MCMC analysis of molecular sequences")

-- Prerequisites
prereq("jdk64")

setenv("TACC_BEAST_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_BEAST_BIN"      ,"%{INSTALL_DIR}/bin")


prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for beast
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n %{name}-%{comp_fam_ver}
%defattr(755,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT
