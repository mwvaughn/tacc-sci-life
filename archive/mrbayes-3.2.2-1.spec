#
# Spec file for MrBayes
#
Summary:   MrBayes - Bayesian Inference of Phylogeny
Name:      mrbayes
Version:   3.2.2
Release:   1
License:   GNU GPL
Group:     Applications/Life Sciences
Source:    %{name}-%{version}.tar.gz
Packager:  Matt Cowperthwait (TACC) - mattcowp@tacc.utexas.edu

%include ../rpm-dir.inc
%include ../system-defines.inc

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  TACC_MRBAYES

%package -n %{name}-%{version}
Summary:   MrBayes - a program for the Bayesian Inference of Phylogeny
Group: Applications/Life Sciences

%description
%description -n %{name}-%{version}

MrBayes is a program for Bayesian inference and model choice across a wide range of phylogenetic and evolutionary models. MrBayes uses Markov chain Monte Carlo (MCMC) methods to estimate the posterior distribution of model parameters.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n mrbayes_3.2.2

%build

%install
%include ../system-load.inc
module purge
module load TACC
module swap intel gcc/4.7.1

cd src/
autoconf
./configure --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR} --with-beagle=no
make 

cd ..

#make install
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp src/mb $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/

## Module for mrbayes
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
The MrBayes modulefile defines %{MODULE_VAR}_DIR, and %{MODULE_VAR}_BIN for mrbayes directory and executable, and prepends to PATH.

Version %{version}
]])

whatis("Name: MrBayes")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keyword: Biology, Application, Phylogenetics, Bayesian")
whatis("URL:  http://mrbayes.sourceforge.net/")
whatis("Description: Tool for Bayesian inference of phylogeny")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
prepend_path("PATH","%{INSTALL_DIR}")
prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for mrbayes
##
 
set     ModulesVersion      "%{version}"
EOF

%files 
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
