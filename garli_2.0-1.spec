#
# Spec file for GARLI
#

Summary: GARLI (Genetic Algorithm for Rapid Likelihood Inference) performs phylogenetic searches on aligned nucleotide datasets using the maximum likelihood criterion.
Name: garli
Version: 2.0
Release: 1
License: GPL
URL: https://www.nescent.org/wg_garli/Main_Page
Group: Applications/Life Sciences
Source: garli-2.0.tar.gz
# NCL is bundled inside the garli tarball
#Source1: ncl-2.1.15.tar.gz
Packager: gendlerk@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc
%include ../system-defines.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define PNAME garli
%define MODULE_VAR TACC_GARLI

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define  MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: GARLI is a program that performs phylogenetic inference using the maximum-likelihood criterion.
Group: Applications/Life Sciences


%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
GARLI (Genetic Algorithm for Rapid Likelihood Inference) performs phylogenetic searches on aligned nucleotide datasets using the maximum likelihood criterion. The assumed model of nucleotide substitution is the General Time Reversible (GTR) model, with gamma distributed rate heterogeneity and an estimated proportion of invariable sites. The implementation of this model is exactly equivalent to that is PAUP*, making the log likelihood (lnL) scores obtained directly comparable. All model parameters may be estimated, including the equilibrium base frequencies (which are not equal to the empirical base frequencies). The gamma model of rate heterogeneity assumes four rate categories (the default in PAUP*). 

# The prep stage.  To execute just the prep stage do 'rpmbuild -bp'
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# The first call to setup untars the first source.  
%setup

# The second call untars the second source, in a subdirectory
# of the first. 

# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory. 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there !
# The following line commented out since ncl is bundled inside the garli tarball -JMF
#%setup -T -D -a 1

# We should now have a ../BUILD/garli-2.0 and, within that, a
# ../BUILD/garli-2.0/ncl-2.1.15 directory.

# The build step.  To just test the build step do 'rpmbuild -bc'
%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# probably should use intel and mvapich2
%include compiler-load.inc
%include mpi-load.inc


# Create temporary directory for the install.  We need this to
# trick garli into thinking ncl-2.1.15 is installed in its final location!
mkdir -p     %{INSTALL_DIR}
tacctmpfs -m %{INSTALL_DIR}
# First build ncl-2.1.15.  
# We will build ncl-2.1.15 in its own directory off of the garli install.
#rm -rf %{INSTALL_DIR}/ncl-2.1.15
mkdir %{INSTALL_DIR}/ncl-2.1.15

tar xzf ncl-2.1.15.tar.gz
cd ncl-2.1.15
env CPPFLAGS=-DNCL_CONST_FUNCS ./configure --prefix=%{INSTALL_DIR}/ncl-2.1.15 --disable-shared
make
make install


# Now, build garli
cd ..

# To make configuring easier, create an environment variable which points
# to where we just installed ncl.
export MY_NCL_DIR=%{INSTALL_DIR}/ncl-2.1.15

# The ncl-2.1.15 program must be in your PATH to pass configure!
export PATH=${MY_NCL_DIR}/bin:$PATH


# The -DMPICH_IGNORE_CXX_SEEK flag is only needed for mvapich2
# builds, it should have no effect on mvapich1, but we have not 
# tested that yet...
./configure --prefix=%{INSTALL_DIR} \
  CC=mpicc \
  CXX=mpicxx \
  F77=mpif77 \
  --with-ncl="${MY_NCL_DIR}" \
  --enable-mpi \


make 
make install

# Temporarily exit
# exit 1

# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}
# umount %{INSTALL_DIR}/
tacctmpfs -u %{INSTALL_DIR}

# Remove any old module files and create anew
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
# need to update this to lua
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#################################################################
#
# This module file sets up the environment variables and path for meep.
#
#############################################################################

proc ModulesHelp { } {
puts stderr "The %{name} module file defines the following environment variables:\n"
puts stderr "TACC_GARLI_DIR, TACC_GARLI_LIB, TACC_GARLI_INC, and TACC_GARLI_BIN."
puts stderr ""
puts stderr "The GARLI executable is \$TACC_GARLI_BIN/garli"
puts stderr ""
puts stderr "Version %{version}"
}

module-whatis "Name: GARLI"
module-whatis "Version: %{version}"
module-whatis "Category: application, biology"
module-whatis "Keyword: Biology, Application, Tree, Phylogenetics"
module-whatis "URL:  https://www.nescent.org/wg_garli/Main_Page"
module-whatis "Description: Tool for performing phylogenetic inference using the maximum-likelihood criterion. "

setenv TACC_GARLI_DIR %{INSTALL_DIR}
setenv TACC_GARLI_INC %{INSTALL_DIR}/include
setenv TACC_GARLI_LIB %{INSTALL_DIR}/lib
setenv TACC_GARLI_BIN %{INSTALL_DIR}/bin

# Also add ncl env vars.
setenv TACC_NCL_DIR %{INSTALL_DIR}/ncl-2.1.15
setenv TACC_NCL_INC %{INSTALL_DIR}/ncl-2.1.15/include
setenv TACC_NCL_LIB %{INSTALL_DIR}/ncl-2.1.15/lib
setenv TACC_NCL_BIN %{INSTALL_DIR}/ncl-2.1.15/bin


prepend-path    PATH                %{INSTALL_DIR}/bin

# And ncl binary files location.
prepend-path    PATH                %{INSTALL_DIR}/ncl-2.1.15/bin

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0###################################################
##
## version file for %{name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
