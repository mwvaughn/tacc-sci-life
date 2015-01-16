#
# Spec file for quicktree
#
Summary:   QuickTree
Name:      quicktree
Version:   1.1
Release:   1
License:   GPL
Group: Applications/Life Sciences
Source:    quicktree_1.1.tar.gz
Packager:  TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   QuickTree neighbor joining method to reconstruct phylogenies.
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}
QuickTree allows the reconstruction of phylogenies for very large protein 
families that would be infeasible using other popular methods. 

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n quicktree_%{version}


%build

%include compiler-load.inc
make 

%install
rm    -rf          $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p           $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir              $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -p bin/quicktree    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*


## Module for quicktree
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The QuickTree modulefile defines the following environment variables,
TACC_QUICKTREE_DIR and TACC_QUICKTREE_BIN for the location of the 
QuickTree directory and binaries.

The modulefile also appends TACC_QUICKTREE_BIN directory to PATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: QuickTree")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Category: Biology, Phylogenics")
whatis("URL:  http://www.sanger.ac.uk/resources/software/quicktree/")
whatis("Description: Neighbor joining code to build trees ")

setenv("TACC_QUICKTREE_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_QUICKTREE_BIN"      ,"%{INSTALL_DIR}/bin")

prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for quicktree
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
