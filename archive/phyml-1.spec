#
# Spec file for PhyML
#
Summary: PhyML 20120412
Name: phyml
Version: 20120412
Release: 1
License: GPL
Vendor: http://code.google.com/p/phyml/downloads/list 
Group: Applications/Life Sciences
Source: phyml-20120412.tar.gz
Packager: gendlerk@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary: PhyML - a tool to estimate maximum likelihood phylogenies from alignments of nucleotide or amino acid sequences
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}
PhyML is a software package tasked to estimate maximum likelihood phylogenies from alignments of nucleotide or amino acide sequences. 

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n phyml-%{version}

%build
%include compiler-load.inc

## Notes on phyml configure options
## --enable-mpi            compile PhyML MPI library

### Make w/o mpi support
./configure
make clean
make DESTDIR=$RPM_BUILD_ROOT


## Make w/ mpi support
#export MPICC=mpicc
#./configure --enable-mpi \
#            --prefix=%{INSTALL_DIR}
#make clean
#make

%install

rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/*
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

cd src
cp phyml $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.

## Module for phyml
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_message=[[
The PHYML modulefile defines the following environment variables:
TACC_PHYML_DIR, TACC_PHYML_LIB, for the location of the PHYML %{version} distribution and libraries files respectively.


Version %{version}
]]

help(help_message,"\n")

whatis("Name: PhyML")
whatis("Version: %{version}")
whatis("Category: applications, biology, phylogenetics")
whatis("Keywords: Biology, Phylogenetics, ")
whatis("URL: http://code.google.com/p/phyml/")
whatis("Description: Estimate maximum likelihood phylogenies from alignments of nucleotide or amino acid sequences")

local phyml_dir=" %{INSTALL_DIR}"

setenv("TACC_PHYML_DIR",phyml_dir)
setenv("TACC_PHYML_LIB",pathJoin(phyml_dir,"lib"))

--
-- Append paths
--
append_path("LD_LIBRARY_PATH",pathJoin(phyml_dir,"lib"))
append_path("PATH",pathJoin(phyml_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for PhyML
##

set     ModulesVersion      "%version"
EOF


%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}


%post
%clean
rm -rf $RPM_BUILD_ROOT
