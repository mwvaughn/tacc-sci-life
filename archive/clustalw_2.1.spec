#
# Spec file for ClustalW
#
Summary:   ClustalW2 multiple sequence alignment program
Name:      clustalw2
Version:   2.1
Release:   0
License:   GNU Lesser GPL
Group: Applications/Life Sciences
Source:    clustalw-2.1.tar.gz
Packager:  TACC - gendlerk@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles
%define _unpack_name clustalw-2.1

%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   ClustalW2 - a general multiple sequence alignment program
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

ClustalW2 is a general purpose multiple sequence alignment program for DNA or proteins.


%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#%setup -n %{name}-%{version}
%setup -n clustalw-2.1


%build
%include compiler-load.inc
./configure --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}
make  

%install
make install

## Module for clustalw
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The ClustalW2 modulefile defines the following environment variables,
TACC_CLUSTALW2_DIR, and TACC_CLUSTALW2_BIN for the location of the clustalw2 directory and 
binaries.

The modulefile also prepends TACC_CLUSTALW2_BIN directory to PATH

Version %{version}
]]

help(help_message,"\n")

whatis("Name: ClustalW2")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keyword: Biology, Application, Alignment, Phylogenetics")
whatis("URL:  http://www.clustal.org/")
whatis("Description: Tool for multiple sequence alignment")

setenv("TACC_CLUSTALW2_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_CLUSTALW2_BIN"      ,"%{INSTALL_DIR}/bin")


prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for clustalw2
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
