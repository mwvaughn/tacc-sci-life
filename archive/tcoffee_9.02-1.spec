#
# Spec file for T-Coffee
#
Summary:   T-Coffee A collection of tools for Computing, Evaluating and Manipulating Multiple Alignments of DNA, RNA, Protein Sequences and Structures 
Name:      tcoffee
Version:   9.02
Release:   1
License:   GNU Lesser GPL
Group: Applications/Life Sciences
Source:    T-COFFEE_distribution_Version_9.02.r1228.tar.gz
Packager:  TACC - gendlerk@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc
%define _unpack_name T-COFFEE_distribution_Version_9.02.r1228

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   T-Coffee - A collection of tools for Computing, Evaluating and Manipulating Multiple Alignments of DNA, RNA, Protein Sequences and Structures 
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

T-Coffee is a collection of tools for Computing, Evaluating and Manipulating Multiple Alignments of DNA, RNA, Protein Sequences and Structures 

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#%setup -n %{name}-%{version}
%setup -n T-COFFEE_distribution_Version_9.02.r1228

%build
%include compiler-load.inc
#./configure --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}
#make  

%install
#make install
./install all

## Module for tcoffee
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The TCoffee modulefile defines the following environment variables,
TACC_TCOFFEE_DIR, and TACC_TCOFFEE_BIN for the location of the tcoffee directory and 
binaries.

The modulefile also prepends TACC_TCOFFEE_BIN directory to PATH

Version %{version}
]]

help(help_message,"\n")

whatis("Name: TCOFFEE")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keyword: Biology, Application, Alignment, MSA, ")
whatis("URL:  http://tcoffee.org/")
whatis("Description: Tool for constructing multiple sequence alignments")

setenv("TACC_TCOFFEE_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_TCOFFEE_BIN"      ,"%{INSTALL_DIR}/bin")


prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for tcoffee
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
