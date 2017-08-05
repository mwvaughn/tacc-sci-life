#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define   PNAME kallisto
Version:  0.42.4
Release:  1
License:  The Regents of the University of California  
Group:    Applications/Life Sciences
Source:   https://github.com/pachterlab/kallisto/archive/v0.42.4.tar.gz
Packager: TACC - wallen@tacc.utexas.edu
Summary:  A program for quantifying abundances of transcripts from RNA-Seq data 

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
#%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR %{MODULE_VAR_PREFIX}KALLISTO

## PACKAGE DESCRIPTION
%description
From the developers: kallisto is a program for quantifying abundances of transcripts from RNA-Seq data, or more generally of target sequences using high-throughput sequencing reads. It is based on the novel idea of pseudoalignment for rapidly determining the compatibility of reads with targets, without the need for alignment. On benchmarks with standard RNA-Seq data, kallisto can quantify 30 million human reads in less than 3 minutes on a Mac desktop computer using only the read sequences and a transcriptome index that itself takes less than 10 minutes to build. Pseudoalignment of reads preserves the key information needed for quantification, and kallisto is therefore not only fast, but also as accurate as existing quantification tools. In fact, because the pseudoalignment procedure is robust to errors in the reads, in many benchmarks kallisto significantly outperforms existing tools.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%setup -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL 
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#--------------------------------------
## Install Steps Start
module purge
module load TACC

%if "%{PLATFORM}" == "stampede"
    module swap $TACC_FAMILY_COMPILER gcc/4.9.1
    module load hdf5/1.8.16 zlib/1.2.8 cmake/3.1.0
    export EXTRA_CMAKE_FLAGS=" -DZLIB_INCLUDE_DIR=$TACC_ZLIB_INC -DZLIB_LIBRARY=$TACC_ZLIB_LIB/libz.so "
%endif

%if "%{PLATFORM}" == "ls5"
    module swap $TACC_FAMILY_COMPILER gcc/4.9.3
    module load hdf5/1.8.16 cmake/3.4.1
    export CFLAGS="-O3 -march=sandybridge -mtune=haswell"
    export LDFLAGS="-march=sandybridge -mtune=haswell"
%endif

# Install with cmake
cd $RPM_BUILD_DIR
rm -rf %{PNAME}-%{version}-cmake/
mv %{PNAME}-%{version} %{PNAME}-%{version}-cmake
mkdir %{PNAME}-%{version}
mkdir -p %{PNAME}-%{version}-cmake/build/
cd %{PNAME}-%{version}-cmake/build/

cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_DIR/%{PNAME}-%{version} \
      -DCMAKE_C_COMPILER=`which gcc` \
      -DCMAKE_CXX_COMPILER=`which g++` \
      -DHDF5_DIR=$TACC_HDF5_DIR \
      $EXTRA_CMAKE_FLAGS \
      ../

make -j 4
make install

# Copy the relevant files
cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/bin/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}-cmake/test/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[

This module loads %{PNAME} version %{version} built with %{comp_fam} and cmake/3.1.0.
Documentation for %{PNAME} is available online at: http://dock.compbio.ucsf.edu/

The executable can be found in %{MODULE_VAR}_BIN
The test files can be found in %{MODULE_VAR}_TEST

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, Transcript Quantification, Pseudoalignment, RNA-Seq")
whatis("Description: kallisto is a program for quantifying abundances of transcripts from RNA-Seq data.")
whatis("URL: http://pachterlab.github.io/kallisto/")

prepend_path("PATH",               "%{INSTALL_DIR}/bin")
setenv(      "%{MODULE_VAR}_DIR",  "%{INSTALL_DIR}/")
setenv(      "%{MODULE_VAR}_BIN",  "%{INSTALL_DIR}/bin/")
setenv(      "%{MODULE_VAR}_TEST", "%{INSTALL_DIR}/test/")

EOF

%if "%{PLATFORM}" == "stampede"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("gcc/4.9.1", "hdf5/1.8.16", "zlib/1.2.8")
EOF
%endif

%if "%{PLATFORM}" == "ls5"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
prereq("gcc/4.9.3", "hdf5/1.8.16")
EOF
%endif

## Modulefile End
#--------------------------------------

# Lua sytax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#--------------------------------------
## VERSION FILE
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
## VERSION FILE END
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}

## POST 
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

# In SPECS dir:
# ./build_rpm.sh --gcc=49 kallisto-0.42.4-1.spec
#
# In apps dir: 
# export RPM_DBPATH=$PWD/db/
# rpm --dbpath $PWD/db --relocate /opt/apps=$PWD -Uvh --force --nodeps /path/to/rpm/file/rpm_file.rpm
# sed -i 's?opt/apps?work/03439/wallen/stampede/apps?g' /path/to/modulefiles/package/version.lua

