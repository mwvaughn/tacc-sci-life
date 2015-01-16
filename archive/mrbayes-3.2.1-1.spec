#
# Spec file for MrBayes
#
Summary:   MrBayes - Bayesian Inference of Phylogeny
Name:      mrbayes
Version:   3.2.1
Release:   1
License:   GNU GPL
Group: Applications/Life Sciences
Source:    mrbayes-3.2.1.tar.gz
Packager:  TACC - gendlerk@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles
%define _unpack_name mrbayes_3.2.1

%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   MrBayes - a program for the Bayesian Inference of Phylogeny
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

MrBayes is a program for Bayesian inference and model choice across a wide range of phylogenetic and evolutionary models. MrBayes uses Markov chain Monte Carlo (MCMC) methods to estimate the posterior distribution of model parameters.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#%setup -n %{name}-%{version}
%setup -n mrbayes_3.2.1

%build
%include compiler-load.inc
cd src/
autoconf
./configure --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR} --with-beagle=no
make  

%install
#make install
mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp src/mb $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/

## Module for mrbayes
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The MrBayes modulefile defines the following environment variables,
TACC_MRBAYES_DIR, and TACC_MRBAYES_BIN for the location of the mrbayes directory and 
binaries.

The modulefile also prepends TACC_MRBAYES_BIN directory to PATH

Version %{version}
]]

help(help_message,"\n")

whatis("Name: MrBayes")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keyword: Biology, Application, Phylogenetics, Bayesian")
whatis("URL:  http://mrbayes.sourceforge.net/")
whatis("Description: Tool for Bayesian inference of phylogeny")

setenv("TACC_MRBAYES_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_MRBAYES_BIN"      ,"%{INSTALL_DIR}/bin")


prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for mrbayes
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
