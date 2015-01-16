#
# Spec file for LAMMPS
#
Summary:   LAMMPS is a Molecular Dynamics package.
Name:      lammps
Version:   5May12
Release:   1
License:   GPL
Vendor:    Sandia
Group: Applications/Chemistry
Source:    lammps-5May12.tar.gz
Packager:  TACC - milfeld@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary:   LAMMPS Molecular Dynamics package.
Group: Applications/Chemistry

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
LAMMPS is a classical molecular dynamics code with the following functionality: It can be run on a single processor or in parallel.  It is written in highly portable C++.  It is easy to extend with new features and functionality.  It has a syntax for defining and using variables and formulas, as well as a syntax for looping over runs and breaking out of loops.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n lammps-%{version}


%build

%include compiler-load.inc
%include mpi-load.inc

#export MPICC=`which mpicc   || /bin/true`
#export MPIF77=`which mpif77 || /bin/true`

module load mkl/10.3
module load fftw2

export MKLROOT=$TACC_MKL_DIR
# kim     IMPORTANT final "/" required on KIM_DIR
export KIM_DIR=`pwd`/lib/kim/
export KIM_INTEL=yes
MY_PWD=`pwd`

#### JPEG TAR

cd lib
   tar -xzvf ../jpegsrc.v8d.tar.gz
   mv jpeg*  jpeg
cd $MY_PWD

cd src
   tar -xvf   ../USER-JPEG.tar
cd $MY_PWD

#### KIM TAR

cd lib
tar -xzvf ../openkim-api-latest.tgz

#                Move contents of kim to distribution directory.
mv kim/README kim/README.lammps
mv kim/*     openkim-api-v1.0.1

#                Delete kim and move distribution kim to new kim
rmdir kim
mv openkim-api-v1.0.1 kim

cd $MY_PWD

### MAKEFILES
cd TACC_MAKES
   for dir in atc  awpmd             jpeg  kim          meam  poems  reax; do
  
     for file in `ls ${dir}*`; do
       base_name=`echo $file | sed "s/${dir}_//"`
       echo  "cp $file  ../lib/$dir/$base_name"
              cp  $file ../lib/$dir/$base_name
     done
  
   done

       echo  "cp  lammps_Makefile.tacc ../src/MAKE/Makefile.tacc"
              cp  lammps_Makefile.tacc ../src/MAKE/Makefile.tacc

       echo  "cp  xmovie_Makefile ../tools/xmovie/Makefile"
              cp  xmovie_Makefile ../tools/xmovie/Makefile
  
cd $MY_PWD

#### LIBS

for dir in atc  awpmd             jpeg  kim          meam  poems  reax; do
    echo "Will be building $dir"
done

cd lib/atc
   echo "Working on atc"
   eval make -f Makefile.icc 
cd $MY_PWD

cd lib/awpmd
   echo "Working on awpmd"
   eval make -f Makefile.openmpi
cd $MY_PWD

cd lib/jpeg
   echo "Working on jpeg"

  ./configure CC=icc CFLAGS='-g -O2' --disable-shared --prefix=`pwd` 
  eval make
  eval make install

cd $MY_PWD

cd lib/kim
   echo "Working on kim"
   eval make examples
cd $MY_PWD

cd lib/meam
   echo "Working on meam"
   eval make -f Makefile.ifort
cd $MY_PWD

cd lib/poems
   echo "Working on poems"
   eval make -f Makefile.icc
cd $MY_PWD

cd lib/reax
   echo "Working on reax"
   eval make -f Makefile.ifort
cd $MY_PWD


#### Make the PACKAGE LIST
cd src
make yes-all
make no-GPU
make no-USER-GPU
make no-USER-CUDA
make no-USER-OMP
make yes-USER-JPEG
make package-status
cd $MY_PWD

#### LAMMPS  (finally!)

cd src
   eval make tacc 
cd $MY_PWD


#### TOOLS

TOPPWD=`pwd`
cd tools
MYPWD=`pwd`

make
   rm -rf *.o

cd createatoms
   ifort createAtoms.f -ocreateAtoms
cd $MYPWD

cd eam_database
    ifort create.f
cd $MYPWD

cd eam_generate
   for i in Al_Zhou  Cu_Mishin1  Cu_Zhou   W_Zhou; do
      echo Working on $i
      icpc ${i}.c -o ${i}.exe
   done
cd $MYPWD

cd $MYPWD

cd lmp2arc/src
   make
   rm -rf *.o
cd $MYPWD

cd lmp2cfg
   ifort lmp2cfg.f -olmp2cfg
cd $MYPWD

cd msi2lmp/src
   make
   rm -rf *.o
cd $MYPWD

cd reax
   ifort bondConnectCheck.f90 -obondConnectCheck
   icc mol_fra.c -omol_fra
cd $MYPWD

cd xmovie
   make
   rm -rf *.o
cd $MYPWD

cd $TOPPWD

%install


rm    -rf          $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p           $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir              $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp src/lmp_tacc    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

cp -pR bench       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bench
cp -pR couple      $RPM_BUILD_ROOT/%{INSTALL_DIR}/couple
cp -pR doc         $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
cp -pR examples    $RPM_BUILD_ROOT/%{INSTALL_DIR}/examples
cp -pR lib         $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
cp -pR potentials  $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials
cp -pR python      $RPM_BUILD_ROOT/%{INSTALL_DIR}/python
cp -pR tools       $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools

chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*


## Module for lamps
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The LAMMPS modulefile defines the following environment variables:
TACC_LAMMPS_DIR/BIN/BENCH/COUPLE/DOC/EXAM/LIB/POT/PYTH/TOOLS
for the location of the LAMMPS home, binaries,
benchmarks, coupling intefaces, documentation, examples,
libraries, potentials, python scripts, and tools, respectively.

The modulefile also appends TACC_LAMMPS_BIN & TACC_LAMMPS_TOOLS to PATH.

To run LAMMPS, please include the following lines in your job script:

       module load lammps
       ibrun lmp_tacc <options>  < in.myinput

using the appropriate input file name.
See the manual for details: $TACC_LAMMPS_DOC/doc/Manual.pdf.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: LAMMPS")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL:  http://lammps.sandia.gov/index.html")
whatis("Description: Molecular Dynamics Chemistry Package")

local lmp_dir="%{INSTALL_DIR}"

setenv("TACC_LAMMPS_DIR"       ,lmp_dir)
setenv("TACC_LAMMPS_BIN"       ,pathJoin(lmp_dir,"bin"))

setenv("TACC_LAMMPS_BENCH"     ,pathJoin(lmp_dir,"bench"))
setenv("TACC_LAMMPS_COUPLE"    ,pathJoin(lmp_dir,"couple"))
setenv("TACC_LAMMPS_DOC"       ,pathJoin(lmp_dir,"doc"))
setenv("TACC_LAMMPS_EXAM"      ,pathJoin(lmp_dir,"examples"))
setenv("TACC_LAMMPS_LIB"       ,pathJoin(lmp_dir,"lib"))
setenv("TACC_LAMMPS_POT"       ,pathJoin(lmp_dir,"potentials"))
setenv("TACC_LAMMPS_PYTH"      ,pathJoin(lmp_dir,"python"))
setenv("TACC_LAMMPS_TOOLS"     ,pathJoin(lmp_dir,"tools"))

append_path("PATH",pathJoin(lmp_dir,"bin"))
append_path("PATH",pathJoin(lmp_dir,"tools"))


EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for lammps
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(755,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
#rm -rf $RPM_BUILD_ROOT
