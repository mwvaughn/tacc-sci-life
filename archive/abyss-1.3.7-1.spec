# $Id$

# Build using build_intel11_mvapich2.sh

Summary: Assembly By Short Sequences - a de novo, parallel, paired-end sequence assembler.
Name: abyss
Version: 1.3.7
Release: 1
License: GPLv3
Group: Applications/Life Sciences
Source: http://www.bcgsc.ca/platform/bioinfo/software/abyss/releases/%{version}/abyss-%{version}.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu

%include rpm-dir.inc
%include ../system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define PNAME abyss
%define MODULE_VAR TACC_ABYSS
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}

%package -n %{PACKAGE_NAME}
Group: Applications/Life Sciences
Summary: Assembly By Short Sequences - a de novo, parallel, paired-end sequence assembler.

%description
%description -n %{PACKAGE_NAME} 
ABySS is a de novo, parallel, paired-end sequence assembler that is designed for short reads. The single-processor version is useful for assembling genomes up to 100 Mbases in size. The parallel version is implemented using MPI and is capable of assembling larger genomes.

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# %setup 

%build

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%include ../system-load.inc
%include compiler-load.inc
%include mpi-load.inc

module purge
module load TACC
module load intel/13.0.2.146
module load boost/1.51.0

# Temp install Google Sparsehash
wget "https://sparsehash.googlecode.com/files/sparsehash-2.0.2.tar.gz"

export CPATH="$TACC_SPARSEHASH_INC:$TACC_BOOST_INC"

./configure --prefix=%{INSTALL_DIR} CC=mpicc CXX=mpicxx CPPFLAGS=-wr279,68 --enable-mpich LDFLAGS=--Wl,-rpath,/opt/apps/intel11_1/mvapich2/1.6/lib --enable-maxk=96
make
make -j 2 DESTDIR=$RPM_BUILD_ROOT install

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_BIN for the location of the %{PNAME}
distribution.

Version %{version}
]]
)

whatis("Name: Abyss")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Assembly, Sequencing")
whatis("URL:http://www.bcgsc.ca/platform/bioinfo/software/abyss")
whatis("Description: Assembly By Short Sequences - a de novo, parallel, paired-end sequence assembler.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
append_path("MANPATH"    ,"%{INSTALL_DIR}/share/man"   )

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
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

