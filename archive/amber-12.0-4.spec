#
# $Id: $
#
#
Summary: Amber Toolkit and parallel modules.

###
Name:      amber 
Version:   12.0
Release:   4
License:   UCSF
Vendor:    Amber
Group: Applications/Life Sciences 
Source0:   AmberTools12.tar.bz2
Source1:   Amber12.tar.bz2
Packager:  TACC - jfonner@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%define version_unit 12

%include rpm-dir.inc
%description
Amber Toolkit and parallel modules

%define PNAME amber
%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define  MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}

#                   Rename rpm to "-n" argument at TACC
%package -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: The Amber tools and parallel modules 
Group:  Applications/Chemistry

%description -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Amber serial, parallel, and cuda modules 
 
%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

# %setup  -n %{PNAME}%{version_unit} 

%build

set +x
%include compiler-load.inc
%include mpi-load.inc
module load mkl
module load cuda
module load cuda_SDK
module load hdf5 netcdf
set -x

echo COMPILER LOAD: %{comp_fam_ver_load}
echo MPI      LOAD: %{mpi_fam_ver_load}

mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
cd                   %{INSTALL_DIR}

tar xjf %{_topdir}/SOURCES/AmberTools12.tar.bz2 --strip-components 1
tar xjf %{_topdir}/SOURCES/Amber12.tar.bz2 --strip-components 1


       AMBERHOME=`pwd`
                 MKL_HOME=$TACC_MKL_DIR
                          CUDA_HOME=$TACC_CUDA_DIR
export AMBERHOME MKL_HOME CUDA_HOME

# LDFLAGS="/usr/lib64/libXext.so.6 -L/usr/lib64" ./configure intel
# Amber now tries to download and install new bugfixes during the configure step if you tell it "y"
# make clean
yes | ./configure --with-netcdf $TACC_NETCDF_DIR intel
make install

make clean
yes | ./configure -mpi --with-netcdf $TACC_NETCDF_DIR intel
make install

make clean
yes | ./configure -cuda --with-netcdf $TACC_NETCDF_DIR intel
make LDFLAGS="-Wl,-rpath,$TACC_CUDA_LIB" install

make clean
yes | ./configure -cuda -mpi --with-netcdf $TACC_NETCDF_DIR intel
make LDFLAGS="-Wl,-rpath,$TACC_CUDA_LIB" install


%install

 cd                   %{INSTALL_DIR}
 cp   -rp AmberTools bin dat doc benchmarks   \
          GNU_LGPL_v2 include \
          lib README share             \
                            $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -r                       $RPM_BUILD_ROOT/%{INSTALL_DIR}/AmberTools/src
chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd                          $RPM_BUILD_ROOT
umount                                      %{INSTALL_DIR}

#############################    MODULES  ######################################

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The TACC Amber installation includes the parallel modules with the .MPI suffix:

MMPBSA.MPI  pbsa.MPI  pmemd.MPI  ptraj.MPI  sander.LES.MPI  sander.MPI

The pmemd binaries for use with GPUs are named:

pmemd.cuda.MPI  pmemd.cuda

They were built with "single-precision, double-precision" for the best trade-off
between speed and accuracy.  Visit http://ambermd.org/gpus/ for more 
information. Also note that when using the CUDA version of pmemd, you can only 
use 1 thread per graphics card and must use the "gpu" queue.  For example, if 
using 2 GPU cards on one node, your job submission script should include the 
following lines (along with all the other usual lines):

#$ -pe 2way 12
#$ -q gpu
ibrun pmemd.cuda.MPI -O -i mdin -o mdout -p prmtop \
-c inpcrd -r restrt -x mdcrd </dev/null

Your ibrun line will change depending your filenames, etc. Cuda libraries are
hard linked, so loading the cuda module is not required.  Again, visit
http://ambermd.org/gpus/ for more information as well as the Lonestar guide at 
http://www.tacc.utexas.edu/user-services/user-guides/lonestar-user-guide

Amber tools examples and benchmarks are included in the AmberTools directory.
Examples, data, docs, includes, info, libs are included in directories with
corresponding names. 

The Amber modulefile defines the following environment variables:
TACC_AMBER_DIR, TACC_AMBER_TOOLS, TACC_AMBER_BIN, TACC_AMBER_DAT,
TACC_AMBER_DOC, TACC_AMBER_INC, TACC_AMBER_LIB, and TACC_AMBER_MAN 
for the corresponding Amber directories.

Also, AMBERHOME is set to the Amber Home Directory (TACC_AMBER_DIR),
and $AMBERHOME/bin is included in the PATH variable.

Version %{version}
]]
)

whatis("Name: AMBER")
whatis("Version: 11.0")
whatis("Version-notes: Compiler:%{comp_fam_ver}, MPI:%{mpi_fam_ver}, MKL:10.2, FFTW:3.2.2")
whatis("Category: Application, Chemistry")
whatis("Keywords:  Chemistry, Biology, Molecular Dynamics, Cuda, Application")
whatis("URL: http://amber.scripps.edu/")
whatis("Description: Molecular Modeling Package")


--
-- Create environment variables.
--
local amber_dir   = "%{INSTALL_DIR}"
local amber_tools = "%{INSTALL_DIR}/AmberTools"
local amber_bin   = "%{INSTALL_DIR}/bin"
local amber_dat   = "%{INSTALL_DIR}/dat"
local amber_doc   = "%{INSTALL_DIR}/doc"
local amber_inc   = "%{INSTALL_DIR}/include"
local amber_lib   = "%{INSTALL_DIR}/lib"
local amber_man   = "%{INSTALL_DIR}/share/man"

setenv("TACC_AMBER_DIR"  , amber_dir  )
setenv("TACC_AMBER_TOOLS", amber_tools)
setenv("TACC_AMBER_BIN"  , amber_bin  )
setenv("TACC_AMBER_DAT"  , amber_dat  )
setenv("TACC_AMBER_DOC"  , amber_doc  )
setenv("TACC_AMBER_INC"  , amber_inc  )
setenv("TACC_AMBER_LIB"  , amber_lib  )
setenv("TACC_AMBER_MAN"  , amber_man  )
setenv("AMBERHOME"       , amber_dir  )

append_path("PATH"       ,amber_bin   )
append_path("MANPATH"    ,amber_man   )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## Version file for AMBER %version
## Compiler: %{comp_fam_ver} and  MPI: %{mpi_fam_ver}
##

set     ModulesVersion      "%{version}"
EOF

#############################    MODULES  ######################################


%files -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}

%clean

#rm -rf $RPM_BUILD_ROOT
