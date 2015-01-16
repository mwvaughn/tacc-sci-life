Summary:   NAMD - scalable molecular dynamics
Name:      namd
Version:   2.9
Release:   1
License:   GPL
Vendor:    namd
Group: Applications/Life Sciences
Source:    NAMD_%{version}_Source.tar.gz
Packager:  TACC - jfonner@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

   
%define charm_version 6.4.0

%include rpm-dir.inc
%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc


%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define  MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%package     -n %{name}%{version}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: NAMD - scalable molecular dynamicss. Uses charm %{charm_version}
Group: Applications/Life Sciences

%description
%description -n %{name}%{version}-%{comp_fam_ver}-%{mpi_fam_ver}
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.


%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


%setup -n NAMD_%{version}_Source
tar xf  charm-%{charm_version}.tar

%build

%include compiler-load.inc
%include mpi-load.inc

rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


### Build Charm++ libraries
cd charm-%{charm_version}
echo "BUILD: env MPICXX=mpicxx ./build charm++ mpi-linux-x86_64 --no-build-shared --with-production"
             env MPICXX=mpicxx ./build charm++ mpi-linux-x86_64 --no-build-shared --with-production


### Build NAMD
cd ..
wget http://www.ks.uiuc.edu/Research/namd/libraries/fftw-linux-x86_64.tar.gz
tar xzf fftw-linux-x86_64.tar.gz
mv linux-x86_64 fftw

wget http://www.ks.uiuc.edu/Research/namd/libraries/tcl8.5.9-linux-x86_64.tar.gz
tar xzf tcl8.5.9-linux-x86_64.tar.gz
mv tcl8.5.9-linux-x86_64 tcl


./config Linux-x86_64-icc --charm-arch mpi-linux-x86_64
cd Linux-x86_64-icc
make release
mv NAMD*.tar.gz ../
cd ..
rm -r ./Linux-x86_64-icc

module load cuda/4.0
./config  Linux-x86_64-icc --charm-arch mpi-linux-x86_64 --with-cuda --cuda-prefix $TACC_CUDA_DIR
cd Linux-x86_64-icc
make release
mv NAMD*.tar.gz ../
cd ..
rm -r ./Linux-x86_64-icc

# --strip-components 1
%install
mkdir -p               $RPM_BUILD_ROOT/%{INSTALL_DIR}/cuda_bin
mkdir -p               $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

mv ./NAMD*CUDA*tar.gz  $RPM_BUILD_ROOT/%{INSTALL_DIR}/cuda_bin/
mv ./NAMD*tar.gz       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/


cd                     $RPM_BUILD_ROOT/%{INSTALL_DIR}/cuda_bin/
tar xzf NAMD*.tar.gz --strip-components 1
rm NAMD*.tar.gz

cd                     $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
tar xzf NAMD*.tar.gz --strip-components 1
rm NAMD*.tar.gz

chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}

#############################    MODULES  ######################################

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[

The TACC NAMD module appends the path to the namd2 executable to the PATH 
environment variable. Also $TACC_NAMD_DIR, and $TACC_NAMD_BIN are set to NAMD 
home and bin directories.

The CUDA GPU version of NAMD was compiled with cuda/4.0 is available in the 
$TACC_NAMD_CUDA directory. This directory is not part of the path variable, 
so executing "namd2" (without specifying a path) runs the normal, MPI version 
of NAMD. Executing "$TACC_NAMD_CUDA/namd2" runs the CUDA version of NAMD. When 
using the GPU version, be sure to specify the "gpu" queue and load the cuda/4.0
module. So these lines should be part of your submission script:

#$ -q gpu
module load cuda/4.0

More information on command line flags is on the developer website, here: 
http://www.ks.uiuc.edu/Research/namd/2.9/ug/node88.html

Version %{version}
]]

help(help_message,"\n")

whatis("Name: NAMD")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords:  Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL: http://www.ks.uiuc.edu/Research/namd/")
whatis("Description: Scalable Molecular Dynamics software")



local namd_dir="%{INSTALL_DIR}"

setenv("TACC_NAMD_DIR",namd_dir)   
setenv("TACC_NAMD_BIN",pathJoin(namd_dir,"bin")) 
setenv("TACC_NAMD_CUDA",pathJoin(namd_dir,"cuda_bin")) 
append_path("PATH",pathJoin(namd_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for NAMD %version
##

set     ModulesVersion      "%{version}"
EOF


%files -n %{name}%{version}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
# START  New RPM SPEC design with new compiler and mvapich 01/10 on Longhorn.
