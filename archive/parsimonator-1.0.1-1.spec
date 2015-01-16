#
# Spec file for Parsimonator
#
Summary:   Parsimonator is a lightweight serial code to produce a starting tree using the parsimony technique
Name:      parsimonator
Version:   1.0.1
Release:   1
License:   GPL
Group: Applications/Life Sciences
Source:    %{name}-%{version}.tar.gz
Packager:  TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   Parsimonator is a lightweight serial code to produce a starting tree using the parsimony technique
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}
Parsimonator is a lightweight serial code to produce a starting tree using the parsimony technique.  The resulting tree may be used as input for RAxML-Light.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#Setup Parsimonator
%setup -n %{name}-%{version}

%build

%include compiler-load.inc

#Build Parsimonator
make -f Makefile.SSE3 clean
make -f Makefile.SSE3 

%install

rm    -rf                $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
mkdir                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
cp -p parsimonator-SSE3  $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -p *.pdf              $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc

chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*


## Module for parsimonator
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The parsimonator modulefile defines the following environment variables,
TACC_PARSIMONATOR_DIR, TACC_PARSIMONATOR_BIN, and TACC_PARSIMONATOR_DOC
for the location of the Parsimonator directory, binaries, and documentation.

The modulefile also appends TACC_PARSIMONATOR_BIN directory to PATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: Parsimonator")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Phylogentics, Genomics, Application")
whatis("URL:  http://wwwkramer.in.tum.de/exelixis/software.html")
whatis("Description: Parsimony Tree Creation Tool")

setenv("TACC_PARSIMONATOR_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_PARSIMONATOR_BIN"      ,"%{INSTALL_DIR}/bin")
setenv("TACC_PARSIMONATOR_DOC"      ,"%{INSTALL_DIR}/doc")

prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for parsimonator
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
