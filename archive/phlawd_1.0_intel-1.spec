#
# Spec file for PHLAWD
#
Summary: PHLAWD
Name: phlawd
Version: 1.0
Release: 1
License: Open
Group: Applications/Life Sciences
Packager: cazes@tacc.utexas.edu
Source: phlawd-1.0_intel.tar.gz
Buildroot: /var/tmp/%{name}-%{version}-intel-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}

Summary: PHLAWD
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}
PHLAWD

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n phlawd-%{version}_intel

%build
%include compiler-load.inc
module load sqlite
export SQLITE3="$TACC_SQLITE_DIR"
make clean
make

%install
pwd
mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp PHLAWD $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r man $RPM_BUILD_ROOT/%{INSTALL_DIR}/
#Stupid rpm
#  Have to change permissions on the directory I created
chmod a+rX $RPM_BUILD_ROOT/%{INSTALL_DIR}
# and the children
chmod -R a+rX $RPM_BUILD_ROOT/%{INSTALL_DIR}

## Module for PHLAWD
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_message = [[
The PHLAWD module file makes available the PHLAWD executable 
used to build phylogeny assemblies. The associated modules 
jdk64, mafft, muscle, phyutility, quicktree, and sqlite must
also be loaded. To load the PHLAWD module, use this command :

  module load jdk64 mafft muscle phyutility quicktree sqlite phlawd

The module defines the following environment variables: 

TACC_PHLAWD_DIR, TACC_PHLAWD_BIN, TACC_PHLAWD_LIB, " 
and TACC_PHLAWD_MAN for the location of the PHLAWD distribution, 
binaries, libraries, and documentation. 

The PHLAWD executable, helper apps, and libraries will be included 
in the user's PATH and LD_LIBRARY_PATH.  
usage: PHLAWD task configfile 

Version %{version}
]]

help(help_message,"\n")

whatis("Name: PHLAWD")
whatis("Version: %{version}")
whatis("Category: CompBioApps")
whatis("Keywords: Biology, Phylogentics, Genomics, Assembly")
whatis("URL: http://code.google.com/p/phlawd")
whatis("Description: PHyLogeny Assembly With Databases")

-- Prerequisites
prereq("jdk64","mafft","muscle","quicktree","phyutility","sqlite")


setenv("TACC_PHLAWD_DIR","%{INSTALL_DIR}")
setenv("TACC_PHLAWD_BIN","%{INSTALL_DIR}/bin")
setenv("TACC_PHLAWD_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_PHLAWD_MAN","%{INSTALL_DIR}/man")
--For phyutility that uses java with a specific jar
setenv("CLASSPATH","%{INSTALL_DIR}/lib:%{INSTALL_DIR}/bin")

prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("MANPATH","%{INSTALL_DIR}/man")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
## version file for PHLAWD
##

set     ModulesVersion      "%version"
EOF


%files -n %{name}-%{comp_fam_ver}
%defattr(0755,root,root)
%{INSTALL_DIR}
%{MODULE_DIR}


%post
%clean
rm -rf $RPM_BUILD_ROOT
