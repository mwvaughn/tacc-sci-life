#
# R-3.0.2.spec 2013-11-05 13:59:00 vaughn@tacc.utexas.edu
#
# See http://www.r-project.org/

Summary:    R is a free software environment for statistical computing and graphics.
Name:       Rstats
Version:    3.0.2    
Release:    1 
License:    GPLv2
Vendor:     R Foundation for Statistical Computing
Group:      Applications/Statistics
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - vaughn@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include ../system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define PNAME Rstats
%define MODULE_VAR TACC_R
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}

%package -n %{PACKAGE_NAME}
Summary: The R statistical computing environment 
Group:  Applications/Statistics

%description
%description -n %{PACKAGE_NAME} 
R provides a wide variety of statistical (linear and nonlinear 
modelling, classical statistical tests, time-series analysis, 
classification, clustering, ...) and graphical techniques, and 
is highly extensible. 

%prep
rm -rf $RPM_BUILD_ROOT

# %setup 

%build

%install
%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include compiler-load.inc
%include mpi-load.inc

module purge
module load TACC
module load intel
module load mkl
module swap mvapich2 mvapich2/1.8
module load hdf5
module load netcdf
module load boost

echo COMPILER LOAD: %{comp_fam_ver_load}
echo MPI      LOAD: %{mpi_fam_ver_load}

mkdir -p        %{INSTALL_DIR}
tacctmpfs -m 	%{INSTALL_DIR}
cd              %{INSTALL_DIR}
 
R_HOME=`pwd`
MKL_HOME=$TACC_MKL_DIR
CUDA_HOME=$TACC_CUDA_DIR
export R_HOME MKL_HOME CUDA_HOME

# Set up src directory
export SRC_DIR=${R_HOME}/src
mkdir -p ${SRC_DIR}
cd ${SRC_DIR}

wget 'http://mirrors.nics.utk.edu/cran/src/base/R-3/R-3.0.2.tar.gz'
tar zxf R-3.0.2.tar.gz
cd R-3.0.2

./configure --prefix=%{INSTALL_DIR} \
  --enable-R-shlib --enable-shared \
  --with-blas --with-lapack --with-pic \
  --without-readline \
  CC=mpicc CXX=mpicxx F77=ifort FC=ifort \
  LD=xild AR=xiar \
  SHLIB_CFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -pthread "\
  MAIN_FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -pthread "\
  SHLIB_FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread "\
  MAIN_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -pthread "\
  SHLIB_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread "\
  DYLIB_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread "\
  SHLIB_CXXLDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread "\
  SHLIB_FCLDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread "\
  BLAS_LIBS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} -lmkl_intel_lp64 -lmkl_core -lmkl_intel_thread -lpthread -lm"\
  LAPACK_LIBS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} -lmkl_intel_lp64 -lmkl_core -lmkl_intel_thread -lpthread -lm"\
  CFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} "\
  LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} "\
  CPPFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} "\
  FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} "\
  CXXFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} "\
  FCFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost -pthread -L${TACC_MKL_LIB} "

make
make install

export PATH=%{INSTALL_DIR}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR}/lib64:%{INSTALL_DIR}/lib:$LD_LIBRARY_PATH

#############################################################
# Hand-install a set of modules that require specific compiler
# behavior and flags
#############################################################

#############################################################
# RMPI
#############################################################
# Note the include and libpath are for mvapich2/2.0a on stampede
# the same package will be installed on ls4
cd ${SRC_DIR}
wget 'http://www.stats.uwo.ca/faculty/yu/Rmpi/download/linux/Rmpi_0.6-3.tar.gz'

R CMD INSTALL Rmpi_0.6-3.tar.gz --configure-args="--with-Rmpi-include=/opt/apps/intel11_1/mvapich2/1.8/include --with-Rmpi-libpath=/opt/apps/intel11_1/mvapich2/1.8/lib --with-Rmpi-type=MPICH2"

#############################################################
# pdbMPI pbdSLAP pbdBASE pbdDMAT pbdDEMO pbdNCDF4 pmclust
#############################################################
cd ${SRC_DIR}
wget 'http://cran.r-project.org/src/contrib/rlecuyer_0.3-3.tar.gz'
sleep 5
wget 'http://cran.r-project.org/src/contrib/pbdMPI_0.2-1.tar.gz'
sleep 5

R CMD INSTALL rlecuyer_0.3-3.tar.gz
R CMD INSTALL pbdMPI_0.2-1.tar.gz --configure-args=" --with-mpi-include=/opt/apps/intel11_1/mvapich2/1.8/include --with-mpi-libpath=/opt/apps/intel11_1/mvapich2/1.8/lib --with-mpi-type=MPICH2"

echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
install.packages("ggplot2");
install.packages("snow");
install.packages("pbdSLAP");
install.packages("pbdBASE");
install.packages("pbdDMAT");
install.packages("pbdDEMO");
install.packages("pbdNCDF4");
install.packages("pmclust");
install.packages("snowfall");
install.packages("iterators");
install.packages("foreach");
install.packages("multicore");
install.packages("doMC");
install.packages("doSNOW");
install.packages("doMPI");
install.packages("doParallel");
install.packages("BH");
install.packages("bigmemory.sri");
install.packages("bigmemory");
install.packages("biganalytics");
install.packages("bigtabulate");
install.packages("synchronicity");
install.packages("Rdsm");
install.packages("SparseM");
install.packages("slam");
install.packages("cluster");
install.packages("randomForest");
install.packages("bit");
install.packages("ff");
install.packages("mchof"); ' > optional.R
Rscript optional.R

###########################################################
# Bioconductor
###########################################################
# create the script for bioconductor
echo 'source("http://bioconductor.org/biocLite.R");
biocLite();
biocLite(c("ggplot2","ShortRead","RankProd","multtest","IRanges","edgeR","Biostrings","GenomicFeatures","bioDist","GenomicRanges"));' > bio.R
Rscript bio.R

#----------------------------------------------------------
# Copy into rpm directory
#----------------------------------------------------------
cd %{INSTALL_DIR}
rm -rf src
cp -rp . $RPM_BUILD_ROOT/%{INSTALL_DIR}
chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd $RPM_BUILD_ROOT

#----------------------------------------------------------
# UNMOUNT THE TEMP FILESYSTEM
#----------------------------------------------------------
tacctmpfs -u %{INSTALL_DIR}

#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
This is the R statistics (Rstats) package built on %(date +'%B %d, %Y').

It includes the following accessory packages:
Rmpi, snow, snowfall
pdbMPI, pbdSLAP, pbdBASE, pbdDMAT, pbdDEMO, pbdNCDF4, pmclust
multicore
doMC, doSNOW, doMPI, doParallel
BH, bigmemory, biganalytics, bigtabulate, synchronicity
Rdsm, fork, SparseM, slam, cluster, randomForest, bit, ff, mchof
BioConductor (base installation)

The R modulefile defines the environment variables TACC_R_DIR, TACC_R_BIN,
TACC_R_LIB and extends the PATH and LD_LIBRARY_PATH paths as appropriate.

Version %{version}
]]
)

whatis("Name: R")
whatis("Version: %{version}")
whatis("Version-notes: Compiler:%{comp_fam_ver}, MPI:%{mpi_fam_ver}")
whatis("Category: Applications, Statistics, Graphics")
whatis("Keywords: Applications, Statistics, Graphics, Scripting Language")
whatis("URL: http://www.r-project.org/")
whatis("Description: statistics package")

--
-- Create environment variables.
--
local r_dir   = "%{INSTALL_DIR}"
local r_bin   = "%{INSTALL_DIR}/bin"
local r_inc   = "%{INSTALL_DIR}/include"
local r_lib   = "%{INSTALL_DIR}/lib64"
local r_man   = "%{INSTALL_DIR}/share/man"

setenv("TACC_R_DIR", r_dir)
setenv("TACC_R_BIN", r_bin)
setenv("TACC_R_INC", r_inc)
setenv("TACC_R_LIB", r_lib)
setenv("TACC_R_MAN", r_man)
setenv("MV2_SUPPORT_DPM", 1)

append_path("PATH", r_bin)
append_path("MANPATH", r_man)
append_path("LD_LIBRARY_PATH", r_lib)
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for R version %{version}
##
set ModulesVersion "%version"
EOF

#----------------------------------------------------------
# Lua syntax check 
#----------------------------------------------------------
if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
    $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{PACKAGE_NAME} 
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post -n %{PACKAGE_NAME} 

%clean

