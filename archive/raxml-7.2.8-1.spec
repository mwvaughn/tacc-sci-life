#
# Spec file for RAxML
#
Summary:   RAxML a maximum likelihood code to infer phylogenetic trees
Name:      raxml
Version:   7.2.8
Release:   1
License:   GPL
Group: Applications/Life Sciences
Source:    RAxML-7.2.8.tar.gz
Packager:  TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary:   RAxML a maximum likelihood code to infer phylogenetic trees
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
RAxML (Randomized Axelerated Maximum Likelihood) is a program for sequential and parallel Maximum
Likelihood [1] based inference of large phylogenetic trees.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n RAxML-%{version}


%build

%include compiler-load.inc
%include mpi-load.inc

export MPICC=`which mpicc   || /bin/true`
export MPIF77=`which mpif77 || /bin/true`

#Build pthreads
make -f Makefile.SSE3.PTHREADS clean
make -f Makefile.SSE3.PTHREADS 

#Build hybrid
make -f Makefile.SSE3.HYBRID clean
make -f Makefile.SSE3.HYBRID 

#Build MPI
make -f Makefile.SSE3.MPI clean
make -f Makefile.SSE3.MPI 


%install

rm    -rf          $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p           $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir              $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -p raxmlHPC*    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*


## Module for raxml
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The RAxML modulefile defines the following environment variables,
TACC_RAXML_DIR and TACC_RAXML_BIN,
for the location of the RAxML directory and binaries.

The modulefile also appends TACC_RAXML_BIN directory to PATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: RAxML")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Application, Phylogenetics")
whatis("URL:  http://wwwkramer.in.tum.de/exelixis/software.html")
whatis("Description: Maximum Likelihood Tree Inference Tool")

local raxml_dir="%{INSTALL_DIR}"

setenv("TACC_RAXML_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_RAXML_BIN"      ,"%{INSTALL_DIR}/bin")

prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for raxml
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(755,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT
