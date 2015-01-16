#
# Spec file for muscle
#
Summary:   MUSCLE a sequence alignment code
Name:      muscle
Version:   3.8.31 
Release:   1
License:   ?
Group: Applications/Life Sciences
Source:    muscle_3.8.31.tar.gz
Packager:  TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   MUSCLE - a multiple sequence alignment program
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

MUSCLE is a program for creating multiple alignments of amino acid or nucleotide sequences. A range of options is provided that give you the choice of optimizing accuracy, speed, or some compromise between the two.
%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n muscle_%{version}


%build

%include compiler-load.inc
make clean
make  

%install
export PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR}
make install

## Module for muscle
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The muscle modulefile defines the following environment variables,
TACC_MUSCLE_DIR and TACC_MUSCLE_BIN for the location of the muscle 
directory and binaries.

The modulefile also appends TACC_MUSCLE_BIN directory to PATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: MUSCLE")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Application, Genomics, Alignment")
whatis("URL:  http://www.drive5.com/muscle")
whatis("Description: Multiple alignment program for amino acid or nucleotide sequences")

setenv("TACC_MUSCLE_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_MUSCLE_BIN"      ,"%{INSTALL_DIR}/bin")

prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for muscle
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
