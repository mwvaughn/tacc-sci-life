# $Id$

Summary: mpiBlast: Parallel implementation of NCBI BLAST.
Name: mpiblast
Version: 1.6.0
Release: 2
License: GPL
Group: Applications/Life Sciences 
Source0:  mpiBLAST-%{version}.tgz
Packager: vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot


%define debug_package %{nil}
%include rpm-dir.inc

%include compiler-defines.inc
%include mpi-defines.inc

%define PNAME mpiblast
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_MPIBLAST

%package -n %{PNAME}-%{comp_fam_ver}-%{mpi_fam_ver}
Group: ComputationalBiology/genomics
Summary: mpiBlast: Parallel implementation of NCBI BLAST.

%description
%description -n %{PNAME}-%{comp_fam_ver}-%{mpi_fam_ver}
mpiBlast: Parallel implementation of NCBI BLAST.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version}

%build

%include compiler-load.inc
%include mpi-load.inc


./configure --with-mpi=$MPICH_HOME CC=mpicc CXX=mpicxx
make ncbi
make

%install

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

mkdir -p %{INSTALL_DIR}/bin
mkdir -p %{INSTALL_DIR}/ncbi/data
cd src/
mv mpiblast mpiblast_cleanup mpiformatdb %{INSTALL_DIR}/bin
cd ../ncbi/data
mv * %{INSTALL_DIR}/ncbi/data

cp -rp %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

umount %{INSTALL_DIR}


#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_BIN for the location of the %{PNAME} distribution.

Version %{version}
]]
)

whatis("Name: mpiBlast")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics")
whatis("URL: http://www.mpiblast.org/")
whatis("Description: mpiBLAST is a freely available, open-source, parallel implementation of NCBI BLAST.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DATA", "%{INSTALL_DIR}/ncbi/data")


EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

