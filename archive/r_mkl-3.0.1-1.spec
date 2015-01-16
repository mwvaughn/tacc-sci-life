#
# R-3.01.spec, v3.01, 2013-06-28 vaughn@tacc.utexas.edu
#
# See http://www.r-project.org/
# Need to use build_intel13.sh for this

Summary:    R is a free software environment for statistical computing and graphics.
Name:       R_mkl
Version:    3.0.1
Release:    1
License:    GPLv2
Vendor:     R Foundation for Statistical Computing
Group:      Applications/Statistics
Source:     http://cran.r-project.org/src/base/R-3/R-3.0.1.tar.gz
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
%include compiler-defines.inc

# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR TACC_R_MKL

%package -n %{name}-%{comp_fam_ver}
Summary:   R is a free software environment for statistical computing and graphics.
Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}-%{comp_fam_ver}
R provides a wide variety of statistical (linear and nonlinear 
modelling, classical statistical tests, time-series analysis, 
classification, clustering, ...) and graphical techniques, and 
is highly extensible. 

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
%setup -n R-3.0.1

##
## BUILD
##

%build

##
## INSTALL
##

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Load correct compiler
%include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC
module load intel

# DO NOT preppend $RPM_BUILD_ROOT in prefix
# ./configure --enable-R-shlib --prefix=%{INSTALL_DIR} --with-x=no --with-tcltk --with-tcl-config=/usr/lib64/tclConfig.sh --with-tk-config=/usr/lib64/tkConfig.sh TCLTK_LIB="-L/usr/lib64 -Wl,-rpath,/usr/lib64 -ltcl -ltk" TCLTK_CPPFLAGS="-I/usr/include" --with-blas=$TACC_GOTOBLAS_LIB/libgoto_lp64.a --with-lapack=$TACC_GOTOBLAS_LIB/libgoto_lp64.a --with-system-zlib=/usr/lib64/libz.a BLAS_LIBS=$TACC_GOTOBLAS_LIB/libgoto_lp64.a LAPACK_LIBS=$TACC_GOTOBLAS_LIB/libgoto_lp64.a

./configure --prefix=%{INSTALL_DIR} \
    CC="icc -std=gnu99" CXX="icpc -std=c++11"  F77=ifort FC=ifort\
    --with-x=no --with-tcltk --with-tcl-config=/usr/lib64/tclConfig.sh \
    --with-tk-config=/usr/lib64/tkConfig.sh \
    TCLTK_LIB="-L/usr/lib64 -Wl,-rpath,/usr/lib64 -ltcl -ltk" TCLTK_CPPFLAGS="-I/usr/include"\
    SHLIB_CXXLD="icpc -shared" \
    CFLAGS="  -mkl -fPIC -g -fp-model strict -O3 -xHost" \
    CXXFLAGS=" -std=c++11 -mkl -fPIC -g -fp-model strict -O3 -xHost" \
    FFLAGS=" -mkl -fPIC  -g -fp-model strict -O3 -xHost" \
    FCFLAGS=" -mkl -fPIC  -g -fp-model strict -O3 -xHost" \
    SHLIB_CXXLDFLAGS=" -shared -mkl -fPIC  -g -fp-model strict -O3 -xHost -L$TACC_MKL_LIB" \
    LDFLAGS="-L$TACC_MKL_LIB" \
    MAIN_CFLAGS="-mkl -fPIC" \
    MAIN_FFLAGS="-fPIC -mkl" \
    --with-lapack --with-blas --enable-shared --enable-R-shlib --enable-BLAS-shlib --with-pic --with-x

make
make DESTDIR=$RPM_BUILD_ROOT install

# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0####################################################################
##
## R
##
proc ModulesHelp { } {
	puts stderr "\tThe module %{name} defines the following environmental variables:"
        puts stderr "\t%TACC_R_DIR, %TACC_R_BIN, %TACC_R_LIB for the location of the %{name}"
        puts stderr "\tdistribution, its binaries, and its libraries. It also adds the "
        puts stderr "\tdirectory locations to the %PATH and the %LD_LIBRARY_PATH.\n"
	puts stderr "\tVersion %{version}\n"
}

module-whatis "R"
module-whatis "Version: %{version}"
module-whatis "Category: applications, statistics, graphics"
module-whatis "Keywords: Applications, Statistics, Graphics, Scripting Language"
module-whatis "Description: statistics package"
module-whatis "URL: http://www.r-project.org/"

# Tcl script only
set version %{version}

# Export environmental variables
setenv TACC_R_DIR %{INSTALL_DIR}
setenv TACC_R_BIN %{INSTALL_DIR}/bin
setenv TACC_R_LIB %{INSTALL_DIR}/lib64/

# Prepend the scalasca directories to the adequate PATH variables
prepend-path PATH %{INSTALL_DIR}/bin
prepend-path LD_LIBRARY_PATH %{INSTALL_DIR}/lib64

# This is only necessary if there will be submodules built on 
# this package. Not the case with R (for the time being).
# prepend-path MODULEPATH %{MODULE_DIR}
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for R version %{version}
##
set ModulesVersion "%version"
EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}

# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the source files from /tmp/BUILD
rm -rf /tmp/BUILD/%{name}-%{version}

# Remove the installation files now that the RPM has been generated
rm -rf /var/tmp/%{name}-%{version}-buildroot

