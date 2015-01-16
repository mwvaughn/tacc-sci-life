#
# Spec file for RAxML
#
Summary:   RAxML-Light a lightweight MPI maximum likelihood code to infer phylogenetic trees
Name:      raxml-light
Version:   1.0.6
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
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary:   RAxML-Light a lightweight maximum likelihood code to infer phylogenetic trees
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
RAxML-Light (Randomized Axelerated Maximum Likelihood) is a lightweight program for sequential and parallel Maximum
Likelihood based inference of large phylogenetic trees.  It has less functionality than RAxML, but may be run in 
parallel using MPI.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#Setup RAxML-Light 
%setup -n %{name}-%{version}


%build

%include compiler-load.inc
%include mpi-load.inc

export MPICC=`which mpicc   || /bin/true`
export MPIF77=`which mpif77 || /bin/true`

#Build pthreads
make -f Makefile.SSE3.PTHREADS clean
make -f Makefile.SSE3.PTHREADS 


#Build MPI
make -f Makefile.SSE3.MPI clean
make -f Makefile.SSE3.MPI 

%install

rm    -rf          $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p           $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir              $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
mkdir              $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
cp -p raxmlLight*  $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -p *.pdf        $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc

chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*


## Module for raxml
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The RAxML-Light modulefile defines the following environment variables,
TACC_RAXML_LIGHT_DIR, TACC_RAXML_LIGHT_BIN, and TACC_RAXML_LIGHT_DOC
for the location of the RAxML-LIGHT directory, binaries, and documentation.

The modulefile also appends TACC_RAXML_LIGHT_BIN directory to PATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: RAxML-Light")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Application, Phylogenetics")
whatis("URL:  http://wwwkramer.in.tum.de/exelixis/software.html")
whatis("Description: Light Weight Maximum Likelihood Tree Inference Tool")

setenv("TACC_RAXML_LIGHT_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_RAXML_LIGHT_BIN"      ,"%{INSTALL_DIR}/bin")
setenv("TACC_RAXML_LIGHT_DOC"      ,"%{INSTALL_DIR}/doc")

prepend_path("PATH","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for raxml-light
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
