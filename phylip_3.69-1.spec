#
# Spec file for PHYLIP
#
Summary:   PHYLIP package of programs for inferring phylogenies
Name:      phylip
Version:   3.69
Release: 1  
License:   GNU Lesser GPL
Group: Applications/Life Sciences
Source:    phylip-3.69.tar.gz
Packager:  TACC - gendlerk@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   PHYLIP - a package of programs for inferring phylogenies
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

PHYLIP (the PHYLogeny Inference Package) is a package of programs for inferring phylogenies (evolutionary trees). Methods that are available in the package include parsimony, distance matrix, and likelihood methods, including bootstrapping and consensus trees. Data types that can be handled include molecular sequences, gene frequencies, restriction sites and fragments, distance matrices, and discrete characters. 

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-%{version}


%build
%include compiler-load.inc
# ./configure --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}
cd src
make  

%install
cd src
export EXEDIR="$RPM_BUILD_ROOT/%{INSTALL_DIR}/bin"
make install

## Module for phylip
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The PHYLIP modulefile defines the following environment variables,
TACC_PHYLIP_DIR, and TACC_PHYLIP_BIN for the location of the phylip directory and 
binaries.

The modulefile also prepends TACC_PHYLIP_BIN directory to PATH

Version %{version}
]]

help(help_message,"\n")

whatis("Name: PHYLIP")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keyword: Biology, Application, Tree, Phylogenetics")
whatis("URL:  http://evolution.gs.washington.edu/phylip/")
whatis("Description: Tool for inferring phylogenies")

setenv("TACC_PHYLIP_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_PHYLIP_BIN"      ,"%{INSTALL_DIR}/bin")


prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for phylip
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
