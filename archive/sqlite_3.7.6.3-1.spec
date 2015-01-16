#
# Spec file for sqlite3
#
Summary:   SQLite sql database engine
Name:      sqlite
Version:   3.7.6.3
Release:   2
License:   open
Group:     library/database
Source:    sqlite_3.7.6.3.tar.gz
Packager:  TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   SQLite - an sql database engine
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

SQLite is a in-process library that implements a self-contained, 
serverless, zero-configuration, transactional SQL database engine.


%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n sqlite_%{version}


%build
%include compiler-load.inc
./configure --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}
make  

%install
make install

## Module for sqlite
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The sqlite modulefile defines the following environment variables,
TACC_SQLITE_DIR, TACC_SQLITE_BIN, TACC_SQLITE_INC, TACC_SQLITE_LIB, 
and TACC_SQLITE_MAN for the location of the sqlite directory and 
binaries.

The modulefile also prepends TACC_SQLITE_BIN directory to PATH, 
TACC_SQLITE_LIB to LD_LIBRARY_PATH, and TACC_SQLITE_MAN to MANPATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: SQLITE")
whatis("Version: %{version}")
whatis("Category: SQL Database")
whatis("Keyword: SQL Database, Library")
whatis("URL:  http://www.sqlite.org/")
whatis("Description: Library for implementing an sql database engine")

setenv("TACC_SQLITE_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_SQLITE_BIN"      ,"%{INSTALL_DIR}/bin")
setenv("TACC_SQLITE_INC"      ,"%{INSTALL_DIR}/include")
setenv("TACC_SQLITE_LIB"      ,"%{INSTALL_DIR}/lib")
setenv("TACC_SQLITE_MAN"      ,"%{INSTALL_DIR}/share/man")

prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("MANPATH","%{INSTALL_DIR}/share/man")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for sqlite
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
