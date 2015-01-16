#
# SPEC file for namd.2.9
#

Summary: NAMD

Name:      namd
Version:   2.9
Release:   1
License: GPL
Vendor:    namd
Group:     Applications/Chemistry
Source:    NAMD_2.9_Source.tar.gz
Packager:  TACC - xzhu216@tacc.utexas.edu


%define debug_package %{nil}
%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define versionnum 2.9
%define cudaver 4.2
%define cudavernum 42
 
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}-cuda%{cudavernum}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR TACC_NAMD

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}-cuda%{cudavernum}
Summary: The namd distribution for login and compute nodes. Uses charm 6.4.0
Group: Applications/Chemistry

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}-cuda%{cudavernum}
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


%setup -n NAMD_%{versionnum}_Source


%build

%include compiler-load.inc
%include mpi-load.inc
module load cuda/4.2
ls -l $TACC_CUDA_DIR

### Build Charm++ libraries
tar xvf  charm-6.4.0.tar
cd charm-6.4.0
echo "BUILD: env MPICXX=mpicxx ./build charm++ mpi-linux-x86_64 --no-build-shared --with-production"
             env MPICXX=mpicxx ./build charm++ mpi-linux-x86_64 --no-build-shared --with-production

cd ..
wget http://www.ks.uiuc.edu/Research/namd/libraries/fftw-linux-x86_64.tar.gz
tar xzf fftw-linux-x86_64.tar.gz
mv linux-x86_64 fftw

wget http://www.ks.uiuc.edu/Research/namd/libraries/tcl8.5.9-linux-x86_64.tar.gz
wget http://www.ks.uiuc.edu/Research/namd/libraries/tcl8.5.9-linux-x86_64-threaded.tar.gz
tar xzf tcl8.5.9-linux-x86_64.tar.gz
tar xzf tcl8.5.9-linux-x86_64-threaded.tar.gz
mv tcl8.5.9-linux-x86_64 tcl
mv tcl8.5.9-linux-x86_64-threaded tcl-threaded

### Build NAMD

### hack config and cuda files   
###sed -i 's@lib64/libcudart.so.\[1-9\]@lib64/libcudart.so@' config 

./config Linux-x86_64-icc --charm-arch mpi-linux-x86_64 --with-cuda --cuda-prefix $TACC_CUDA_DIR 
cd Linux-x86_64-icc

make -j 2

cd ..

%install
mkdir -p                                                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp  -p  Linux-x86_64-icc/{namd2,psfgen,flipbinpdb,flipdcd} $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}

#############################    MODULES  ######################################

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}-cuda%{cudavernum}.lua << 'EOF'
local help_message = [[

The TACC NAMD module appends the path to the namd2 executable
to the PATH environment variable.  Also TACC_NAMD_DIR, and
TACC_NAMD_BIN are set to NAMD home and bin directories.

This is a CUDA enabled compilation of NAMD.2.9. A simple way to 
launch the CUDA enabled namd job is
ibrun namd2 +idlepoll inputFile > outputFile.

cuda has to be loaded by
module load cuda/4.2
before using this cuda enabled namd.

For details about cuda acceleration, refer NAMD documentation.

Version %{version}-cuda%{cudavernum}
]]

help(help_message,"\n")

whatis("Name: NAMD")
whatis("Version: %{version}-cuda%{cudavernum}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL: http://www.ks.uiuc.edu/Research/namd/")
whatis("Description: Scalable Molecular Dynamics software")


local namd_dir="%{INSTALL_DIR}"

setenv("TACC_NAMD_DIR",namd_dir)
setenv("TACC_NAMD_BIN",pathJoin(namd_dir,"bin"))
append_path("PATH",pathJoin(namd_dir,"bin"))

prereq ("cuda/4.2")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version}-cuda%{cudavernum} << 'EOF'
#%Module1.0#################################################
##
## version file for NAMD %version-cuda%{cudavernum}
##

set     ModulesVersion      "%{version}-cuda%{cudavernum}"
EOF


%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}-cuda%{cudavernum}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT

# START  New RPM SPEC design with new compiler and mvapich 01/10 on Longhorn.
#
