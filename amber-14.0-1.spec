#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME amber
Version:   14.0
Release:   1
License:   UCSF
Vendor:    Amber
Group:     Applications/Life Sciences 
Source0:   AmberTools15.tar.bz2
Source1:   Amber14.tar.bz2
Packager:  TACC - jfonner@tacc.utexas.edu
Summary:   Amber Toolkit and parallel modules.

%define version_unit 14

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR %{MODULE_VAR_PREFIX}AMBER

#                   Rename rpm to "-n" argument at TACC
# %package -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
# Summary: The Amber tools and parallel modules 
# Group:  Applications/Life Sciences

# %description -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
%description
Amber molecular dynamics serial, parallel, and cuda modules 
 
## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup  -n %{PNAME}%{version_unit} 

# The next command unpacks Source1
# -b <n> means unpack the nth source *before* changing directories.
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source).
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -T -D -b 1 -n %{PNAME}%{version_unit}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start
%include ./include/compiler-load.inc
%include ./include/mpi-load.inc

# %if "%{PLATFORM}" != "stampede"
#     module load mkl
# %endif

module load cuda
# module load hdf5 netcdf/3.6.3
# module load python 
# add the next line when if mpi4py is a separate module
# module load mpi4py

echo COMPILER LOAD: %{comp_module}
echo MPI      LOAD: %{mpi_module}

       AMBERHOME=`pwd`
#                 MKL_HOME=$TACC_MKL_DIR
                          CUDA_HOME=$TACC_CUDA_DIR
export AMBERHOME CUDA_HOME 
				# MKL_HOME 

# LDFLAGS="/usr/lib64/libXext.so.6 -L/usr/lib64" ./configure intel
# Amber now tries to download and install new bugfixes during the configure step if you tell it "y"
# make clean

./update_amber --update
./update_amber --update
./update_amber --update

./configure intel 
make install

make clean
./configure -mpi intel 
cd src
make install
cd ..

make clean
./configure -cuda intel 
			      # --with-netcdf $TACC_NETCDF_DIR intel
make LDFLAGS="-Wl,-rpath,$TACC_CUDA_LIB" install

make clean
./configure -cuda -mpi intel 
make LDFLAGS="-Wl,-rpath,$TACC_CUDA_LIB" install

cp    -rp AmberTools bin dat doc benchmarks   \
          GNU_LGPL_v2 include \
          lib README share             \
                            $RPM_BUILD_ROOT/%{INSTALL_DIR}
# rm -rf                      $RPM_BUILD_ROOT/%{INSTALL_DIR}/AmberTools/src
# chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT/%{INSTALL_DIR}


#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}


cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
This revision of Amber was built on %(date +'%B %d, %Y') and includes all bugfixes
up to that point. A list of bugfixes is on the Amber site here:
http://ambermd.org/bugfixes.html

The TACC Amber installation includes the parallel modules with the .MPI suffix:

MMPBSA.py.MPI  pbsa.MPI  pmemd.MPI  ptraj.MPI  sander.LES.MPI  sander.MPI

The pmemd binaries for use with GPUs are named:

pmemd.cuda.MPI  pmemd.cuda

They were built with "single-precision, double-precision" for the best trade-off
between speed and accuracy.  Visit http://ambermd.org/gpus/ for more 
information. Also note that when using the CUDA version of pmemd, you can only 
use 1 thread per graphics card and must use the "gpu" queue.  For example, if 
using 1 GPU card on two nodes, your job submission script should include the 
following lines (along with all the other usual lines):

#SBATCH -n 2 -N 2
#SBATCH -p gpu
ibrun pmemd.cuda.MPI -O -i mdin -o mdout -p prmtop \
-c inpcrd -r restrt -x mdcrd </dev/null

Your ibrun line will change depending your filenames, etc. Cuda libraries are
hard linked, so loading the cuda module is not required.  Again, visit
http://ambermd.org/gpus/ for more information as well as the Stampede guide at 
http://www.tacc.utexas.edu/user-services/user-guides/stampede-user-guide

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

whatis("Name: Amber")
whatis("Version: 12.0")
whatis("Version-notes: Compiler:%{comp_fam_ver}, MPI:%{mpi_fam_ver}")
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
local amber_python= "%{INSTALL_DIR}/lib/python2.6/site-packages"
local amber_man   = "%{INSTALL_DIR}/share/man"

setenv("TACC_AMBER_DIR"   , amber_dir  )
setenv("TACC_AMBER_TOOLS" , amber_tools)
setenv("TACC_AMBER_BIN"   , amber_bin  )
setenv("TACC_AMBER_DAT"   , amber_dat  )
setenv("TACC_AMBER_DOC"   , amber_doc  )
setenv("TACC_AMBER_INC"   , amber_inc  )
setenv("TACC_AMBER_LIB"   , amber_lib  )
setenv("TACC_AMBER_MAN"   , amber_man  )
setenv("AMBERHOME"        , amber_dir  )

append_path("PATH"        ,amber_bin   )
append_path("LD_LIBRARY_PATH",amber_lib)
append_path("PYTHONPATH"  ,amber_python)
append_path("MANPATH"     ,amber_man   )
EOF



cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## Version file for AMBER %version
## Compiler: %{comp_fam_ver} and  MPI: %{mpi_fam_ver}
##

set     ModulesVersion      "%{version}"
EOF

if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
    $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#############################    MODULES  ######################################


%files 
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post 

%clean

#rm -rf $RPM_BUILD_ROOT
