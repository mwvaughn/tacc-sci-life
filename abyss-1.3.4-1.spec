# $Id$

# Build using build_intel11_mvapich2.sh

Summary: Assembly By Short Sequences - a de novo, parallel, paired-end sequence assembler.
Name: abyss
Version: 1.3.4
Release: 1
License: GPL
Group: Applications/Life Sciences
Source0:  abyss-%{version}.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot


%define debug_package %{nil}
%include rpm-dir.inc

%include compiler-defines.inc
%include mpi-defines.inc

%define PNAME abyss
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_ABYSS
%package -n %{PNAME}-%{comp_fam_ver}-%{mpi_fam_ver}
Group: Applications/Life Sciences
Summary: Assembly By Short Sequences - a de novo, parallel, paired-end sequence assembler.

%description
%description -n %{PNAME}-%{comp_fam_ver}-%{mpi_fam_ver}
ABySS is a de novo, parallel, paired-end sequence assembler that is designed for short reads. The single-processor version is useful for assembling genomes up to 100 Mbases in size. The parallel version is implemented using MPI and is capable of assembling larger genomes.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version}

%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
%include compiler-load.inc
# Load correct mpi stack
%include mpi-load.inc
%include mpi-env-vars.inc
# Load additional modules here (as needed)
module unload $TACC_FAMILY_COMPILER

module purge
module load TACC
module load intel
module load sparsehash
module load boost

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

