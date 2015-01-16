#
# SPEC file for namd.2.7b2
#

Summary: NAMD

Name:      namd
Version:   2.7b2
Release:   3
License: GPL
Vendor:    namd
Group:     Applications/Chemistry
Source:    NAMD_2.7b2_Source.tar.gz
Packager:  TACC - hliu@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

   
%define version_unit 27b2
 
%include rpm-dir.inc
%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc


%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define  MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%description
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

%package     -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: The namd distribution for login and compute nodes. Uses charm 6.1.3
Group:   Applications/Chemistry
%description -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Contains all components


%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


%setup -n NAMD_%{version}_Source
tar xvf  charm-6.1.3.tar

cd arch
cp  $RPM_SOURCE_DIR/namd-patches/intel11_1-mvapich2_1_4-2.7b2/Linux-x86_64.tcl .
cp  $RPM_SOURCE_DIR/namd-patches/intel11_1-mvapich2_1_4-2.7b2/Linux-x86_64.fftw .
#cp  $RPM_SOURCE_DIR/namd-patches/intel11_1-mvapich2_1_4-2.7b2/Linux-x86_64.cuda .

cd ../src

%build

%include compiler-load.inc
%include mpi-load.inc

rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module load fftw2
#module load cuda

### Build Charm++ libraries
cd charm-6.1.3
echo "BUILD: ./build charm++ mpi-linux-x86_64 mpicxx --no-build-shared -O -DCMK_OPTIMIZE=1"
             ./build charm++ mpi-linux-x86_64 mpicxx --no-build-shared -O -DCMK_OPTIMIZE=1


### Build NAMD

cd ..

./config tcl fftw Linux-x86_64-MPI-icc
cd                Linux-x86_64-MPI-icc

make

%install
mkdir -p                                                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
ls -l Linux-x86_64-MPI-icc 
cp    Linux-x86_64-MPI-icc/{namd2,psfgen,flipbinpdb,flipdcd} $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}

#############################    MODULES  ######################################

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[

The TACC NAMD module appends the path to the namd2 executable
to the PATH environment variable.  Also TACC_NAMD_DIR, and 
TACC_NAMD_BIN are set to NAMD home and bin directories.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: NAMD")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL: http://www.ks.uiuc.edu/Research/namd/")
whatis("Description: Scalable Molecular Dynamics software")



local namd_dir="%{INSTALL_DIR}"

setenv("TACC_NAMD_DIR",namd_dir)   
setenv("TACC_NAMD_BIN",pathJoin(namd_dir,"bin")) 
append_path("PATH",pathJoin(namd_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for NAMD %version
##

set     ModulesVersion      "%{version}"
EOF


%files -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
# START  New RPM SPEC design with new compiler and mvapich 01/10 on Longhorn.
