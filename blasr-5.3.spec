%define		PNAME	blasr
Version:	5.3
Release:	1
License:	BSD
URL:		https://github.com/PacificBiosciences/blasr
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	A set of tools for fast aligning long reads for consensus and assembly

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR      %{MODULE_VAR_PREFIX}BLASR

## PACKAGE DESCRIPTION
%description
A PacificBiosciences tool for aligning very long sequencing reads.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
#%setup -n %{PNAME}-%{version}

## BUILD
%build


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
BI=$RPM_BUILD_ROOT/%{INSTALL_DIR}
BR=${RPM_BUILD_ROOT}
ID=${INSTALL_DIR}

PATH=${BI}/bin:${PATH}
#LD_LIBRARY_PATH=${BI}/lib:${LD_LIBRARY_PATH}
#INCLUDE=${BI}/include:${INCLUDE}

TOP=$PWD
[ -e test_install ] && rm -rf test_install
mkdir test_install
BI=$TOP/test_install

module purge
module load TACC
case %{PLATFORM} in
wrangler)
	#module load python/2.7.9 hdf5 cmake samtools/1.3 boost/1.55.0
	module load python/2.7.9 hdf5 cmake boost/1.55.0
	module use $WORK/public/apps/modulefiles
	module load ccache googletest
	export CC=icc
	export CXX=icpc
	export CFLAGS="-fPIC -O3 -xHOST"
	export CXXFLAGS="-fPIC -O3 -xHOST -D_GNU_SOURCE"
	#export LDFLAGS="-L${BI}/lib"
#	export CC=gcc
#	export CXX=g++
#	export CFLAGS="-fPIC -I${BI}/include"
#	export CXXFLAGS="-fPIC -I${BI}/include -O3 -D_GNU_SOURCE"
#	export LDFLAGS="-L${BI}/lib"
	export BOOST_ROOT=$TACC_BOOST_DIR
	;;
ls5)
	bver="boost/1.59"
	module load python/2.7.12 hdf5 cmake samtools/1.3 $bver
	module use $WORK/ls5/public/apps/modulefiles
	module load ccache
	export CC=icc
	export CXX=icpc
	export CFLAGS="-fPIC -O3 -xAVX -axCORE-AVX2"
	export CXXFLAGS="-fPIC -O3 -xAVX -axCORE-AVX2 -D_GNU_SOURCE"
	export BOOST_ROOT=$TACC_BOOST_DIR
	;;
*)
	module load python/2.7.12 hdf5 cmake samtools/1.3 boost/1.61.0
	module use $WORK/public/apps/modulefiles
	module load ccache googletest
	;;
esac

# Load personal modules for deps

function pbgit {
	GIT=/work/03076/gzynda/rpmbuild/SOURCES/${1}-${2}.tar.gz
	[ -d $1 ] && rm -rf $1
	if [ -e $GIT ]
	then
		tar -xzf $GIT
	else
		git clone https://github.com/PacificBiosciences/${1}.git && cd $1
		[ -n "$2" ] && git checkout $2
		git submodule update --init --recursive
		cd .. && tar -czf $GIT $1
	fi
	cd $1
}

################################################
# htslib
################################################
BIN=/work/03076/gzynda/rpmbuild/SOURCES/htslib-bin.tar.gz
if [ -e $BIN ]
then
	tar -xzf $BIN -C ${BI}
else
	# GIT
	pbgit htslib ea846607f3ca7f49b3fb43df76f572d3f47cc6bb
	# LOAD
	# BUILD
	make CC=$CC CFLAGS="${CFLAGS}" ZLIB_ROOT=/usr/lib64 -j 24 VERBOSE=1
	mkdir -p tmp/local/pb_htslib/{include,lib}
	tar -cvf - */*\.h | tar -xvf - -C $PWD/tmp/local/pb_htslib/include
	tar -cf - *\.a | tar -xf - -C $PWD/tmp/local/pb_htslib/lib
	tar -cvzf $BIN -C $PWD/tmp/ local
	tar -xvzf $BIN -C ${BI}
fi
export HTS_INC=${BI}/local/pb_htslib/include
export HTS_LIB=${BI}/local/pb_htslib/lib
cd $TOP

################################################
# pbbam
################################################
BIN=/work/03076/gzynda/rpmbuild/SOURCES/pbbam-bin.tar.gz
if [ -e $BIN ]
then
	tar -xzf $BIN -C ${BI}
else
	# GIT
	pbgit pbbam 928605a86ac024aced821fe4a4bce0b43d5ee680
	mkdir build && cd build
	# LOAD
	# BUILD
	#CC=icc CXX=icpc CFLAGS="$CF" CXXFLAGS="$CF" LDFLAGS="$LF" \
           # -DCMAKE_SKIP_BUILD_RPATH=FALSE \
	cmake \
            -DPacBioBAM_build_shared=ON \
            -DPacBioBAM_build_docs=OFF \
            -DPacBioBAM_build_tests=OFF \
            -DZLIB_INCLUDE_DIRS=/usr/include \
            -DZLIB_LIBRARIES=/usr/lib64/libz.so \
            -DHTSLIB_INCLUDE_DIRS=$HTS_INC \
            -DHTSLIB_LIBRARIES=$HTS_LIB/libhts.a \
            -DBoost_INCLUDE_DIRS=${TACC_BOOST_INC} \
            -DCMAKE_SKIP_RPATH=TRUE \
            ..
            #-DCMAKE_BUILD_TYPE=RelWithDebInfo \
            #-DCMAKE_SKIP_BUILD_RPATH=TRUE \
	make -j 24 VERBOSE=1
	ln -s ../include .
	tar -cvhzf $BIN bin lib include
	tar -xvzf $BIN -C ${BI}
fi
cd $TOP

################################################
# blasr_libcpp
################################################
BIN=/work/03076/gzynda/rpmbuild/SOURCES/blasr_libcpp-bin.tar.gz
if [ ! -e $BIN ]
then
	pbgit blasr_libcpp f43ccacc4d360ae28407008da03293a14b84a78c
	python configure.py PREFIX=${BI} \
		HDF5_INC=$TACC_HDF5_INC \
		HDF5_LIB=$TACC_HDF5_LIB \
		ZLIB_LIB=/usr/lib64 \
		PBBAM_INC=${BI}/include \
		PBBAM_LIB=${BI}/lib \
		BOOST_INC=$TACC_BOOST_INC \
		HTSLIB_INC=$HTS_INC \
		HTSLIB_LIB=$HTS_LIB
	
	make -j24 libpbdata LDLIBS="-Wl,-rpath,$TACC_HDF5_LIB -lpbbam" VERBOSE=1
	make -j24 libpbihdf LDLIBS="-Wl,-rpath,$TACC_HDF5_LIB" VERBOSE=1
	make -j24 libblasr LDLIBS="-Wl,-rpath,$TACC_HDF5_LIB" VERBOSE=1

	mkdir -p tmp/{lib,include}
	cp alignment/libblasr.{a,so} tmp/lib/
	cp hdf/libpbihdf.{a,so} tmp/lib/
	cp pbdata/libpbdata.{a,so} tmp/lib/
	find alignment hdf pbdata -name \*.h\* | tar -cf - -T - | tar -xf - -C tmp/include
	tar -czf $BIN -C tmp lib include
fi
tar -xzf $BIN -C ${BI}
cd ..

################################################
# blasr
################################################
# GIT
pbgit blasr 8d086d747e51a409f25481524e92e99750b14d59
# LOAD
BLASR=${TOP}/blasr
# BUILD

################################################
# blasr config
################################################

# cmake bax2bam
mkdir -p $BLASR/utils/bax2bam/build
cd $BLASR/utils/bax2bam/build
#CC=icc CXX=icpc CFLAGS="-O3 -xHOST" CXXFLAGS="-O3 -xHOST" 
cmake \
	-DBoost_INCLUDE_DIRS=$TACC_BOOST_INC \
	-DHDF5_RootDir=$TACC_HDF5_DIR \
	-DPacBioBAM_INCLUDE_DIRS=${BI}/include \
	-DPacBioBAM_LIBRARIES=${BI}/lib/libpbbam.so \
	-DHTSLIB_INCLUDE_DIRS=$HTS_INC \
	-DHTSLIB_LIBRARIES=$HTS_LIB/libhts.a \
	-DBax2BAM_build_tests=OFF \
	-DZLIB_INCLUDE_DIRS=/usr/include \
	-DZLIB_LIBRARIES=/usr/lib64/libz.so \
	-DBax2Bam_EXE_LINKER_FLAGS="-L$TACC_HDF5_LIB -Wl,-rpath,$TACC_HDF5_LIB -lsz" \
	-DBLASR_INCLUDE_DIRS=${BI}/include/alignment \
	-DPBIHDF_INCLUDE_DIRS=${BI}/include/hdf \
	-DPBDATA_INCLUDE_DIRS=${BI}/include/pbdata \
	-DBLASR_LIBRARIES=${BI}/lib/libblasr.so \
	-DPBIHDF_LIBRARIES=${BI}/lib/libpbihdf.so \
	-DPBDATA_LIBRARIES=${BI}/lib/libpbdata.so \
	-DCMAKE_SKIP_BUILD_RPATH=TRUE \
	-DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath,$TACC_HDF5_LIB" \
	..

# cmake bam2bax
mkdir -p $BLASR/utils/bam2bax/build
cd $BLASR/utils/bam2bax/build
#CC=icc CXX=icpc CFLAGS="-O3 -xHOST" CXXFLAGS="-O3 -xHOST" 
cmake \
	-DBoost_INCLUDE_DIRS=$TACC_BOOST_INC \
	-DHDF5_RootDir=$TACC_HDF5_DIR \
	-DPacBioBAM_INCLUDE_DIRS=${BI}/include \
	-DPacBioBAM_LIBRARIES=${BI}/lib/libpbbam.so \
	-DHTSLIB_INCLUDE_DIRS=$HTS_INC \
	-DHTSLIB_LIBRARIES=$HTS_LIB/libhts.a \
	-DBam2Bax_build_tests=OFF \
	-DZLIB_INCLUDE_DIRS=/usr/include \
	-DZLIB_LIBRARIES=/usr/lib64/libz.so \
	-DBax2Bam_EXE_LINKER_FLAGS="-L$TACC_HDF5_LIB -Wl,-rpath,$TACC_HDF5_LIB -lsz" \
	-DBLASR_INCLUDE_DIRS=${BI}/include/alignment \
	-DPBIHDF_INCLUDE_DIRS=${BI}/include/hdf \
	-DPBDATA_INCLUDE_DIRS=${BI}/include/pbdata \
	-DBLASR_LIBRARIES=${BI}/lib/libblasr.so \
	-DPBIHDF_LIBRARIES=${BI}/lib/libpbihdf.so \
	-DPBDATA_LIBRARIES=${BI}/lib/libpbdata.so \
        -DCMAKE_SKIP_BUILD_RPATH=TRUE \
	-DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath,$TACC_HDF5_LIB" \
	..

# blasr config
cd $BLASR
python configure.py --shared \
	PREFIX=$BI \
	HDF5_INC=$TACC_HDF5_INC \
	HDF5_LIB=$TACC_HDF5_LIB \
	HDF5_LIBFLAGS="-L$TACC_HDF5_LIB -Wl,-rpath,$TACC_HDF5_LIB" \
	ZLIB_LIB=/usr/lib64 \
	BOOST_INC=$TACC_BOOST_INC \
	LIBPBDATA_INC=${BI}/include/pbdata \
	LIBPBIHDF_INC=${BI}/include/hdf \
	LIBBLASR_INC=${BI}/include/alignment \
	LIBPBDATA_LIB=${BI}/lib \
	LIBPBIHDF_LIB=${BI}/lib \
	LIBBLASR_LIB=${BI}/lib \
	PBBAM_INC=${BI}/include \
	PBBAM_LIB=${BI}/lib \
	HTSLIB_INC=$HTS_INC \
	HTSLIB_LIB=$HTS_LIB

################################################
# blasr build
################################################

cd $BLASR
export LDFLAGS="-Wl,-rpath,$TACC_HDF5_LIB"
make -j 24 blasr HDF5_LIBFLAGS="-Wl,-rpath,$TACC_HDF5_LIB -lhdf5_cpp -lhdf5 -lsz" VERBOSE=1
cd $BLASR/utils
make -j 24 HDF5_LIBFLAGS="-Wl,-rpath,$TACC_HDF5_LIB -lhdf5_cpp -lhdf5 -lsz" VERBOSE=1
cd $BLASR/utils/bax2bam/build && make -j 24 VERBOSE=1
cd $BLASR/utils/bam2bax/build && make -j 24 VERBOSE=1

cd $BLASR && cp blasr $BI/bin/
cd $BLASR/utils && cp loadPulses pls2fasta sawriter samFilter samtoh5 samtom4 sdpMatcher toAfg $BI/bin/
cd $BLASR/utils/bax2bam && cp bin/* $BI/bin/
cd $BLASR/utils/bam2bax && cp bin/* $BI/bin/

# Delete bin tars
rm /work/03076/gzynda/rpmbuild/SOURCES/*-bin.tar.gz

## Install Steps End
#--------------------------------------

#--------------------------------------

cp -r $TOP/test_install/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN
 - %{MODULE_VAR}_LIB

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, PacBio")
whatis("Description: blasr - A set of tools for fast aligning long reads")
whatis("URL: %{url}")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
setenv("%{MODULE_VAR}_INC",	pathJoin("%{INSTALL_DIR}", "include"))
EOF
## Modulefile End
#--------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
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
