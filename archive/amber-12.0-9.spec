Summary: Amber Toolkit and parallel modules.
Name:      amber 
Version:   12.0
Release:   9
License:   UCSF
Vendor:    Amber
Group: Applications/Life Sciences 
Source0:   AmberTools13.tar.bz2
Source1:   Amber12.tar.bz2
Packager:  TACC - jfonner@tacc.utexas.edu
Requires: netcdf-3.6-intel13

%define version_unit 12

%include rpm-dir.inc
# Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include ../system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define      PNAME amber
%define MODULE_VAR TACC_AMBER
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define  MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}

#                   Rename rpm to "-n" argument at TACC
%package -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: The Amber tools and parallel modules 
Group:  Applications/Life Sciences

%description
%description -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Amber serial, parallel, and cuda modules 
 
%prep
rm   -rf $RPM_BUILD_ROOT

# %setup  -n %{PNAME}%{version_unit} 

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include compiler-load.inc
%include mpi-load.inc

%if "%{PLATFORM}" != "stampede"
    module load mkl
%endif

module load cuda
module load hdf5 netcdf/3.6.3
module load python mpi4py

echo COMPILER LOAD: %{comp_fam_ver_load}
echo MPI      LOAD: %{mpi_fam_ver_load}

mkdir -p        %{INSTALL_DIR}
tacctmpfs -m 	%{INSTALL_DIR}
cd              %{INSTALL_DIR}
pwd

tar xjf %{_topdir}/SOURCES/AmberTools13.tar.bz2 --strip-components 1
tar xjf %{_topdir}/SOURCES/Amber12.tar.bz2 --strip-components 1


       AMBERHOME=`pwd`
                 MKL_HOME=$TACC_MKL_DIR
                          CUDA_HOME=$TACC_CUDA_DIR
export AMBERHOME MKL_HOME CUDA_HOME

# LDFLAGS="/usr/lib64/libXext.so.6 -L/usr/lib64" ./configure intel
# Amber now tries to download and install new bugfixes during the configure step if you tell it "y"
# make clean

# it takes two or more rounds of configure to get the updates... Im' just testing this
./update_amber --update
./update_amber --update
./update_amber --update
./update_amber --update

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




 cd                   %{INSTALL_DIR}
 cp   -rp AmberTools bin dat doc benchmarks   \
          GNU_LGPL_v2 include \
          lib README share             \
                            $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -r                       $RPM_BUILD_ROOT/%{INSTALL_DIR}/AmberTools/src
chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd                          $RPM_BUILD_ROOT
tacctmpfs -u                                %{INSTALL_DIR}

###########################    MODULE FILE  ####################################

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

%if "%{PLATFORM}" == "stampede"

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

%endif

%if "%{PLATFORM}" == "lonestar"

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
This revision of Amber was built on %(date +'%B %d, %Y') and includes all bugfixes
up to that point. A list of bugfixes is on the Amber site here:
http://ambermd.org/bugfixes.html

The TACC Amber installation includes the parallel modules with the .MPI suffix:

MMPBSA.py.MPI  pbsa.MPI  pmemd.MPI  pmemd.amoeba.MPI  ptraj.MPI  sander.LES.MPI  sander.MPI

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

Version %{version}. 
]]
)

whatis("Name: AMBER")
whatis("Version: %{version}")
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


%endif

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


%files -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}

%clean

#rm -rf $RPM_BUILD_ROOT
