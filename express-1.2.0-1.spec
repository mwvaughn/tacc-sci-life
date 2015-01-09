Summary:    express - Streaming quantification for high-throughput sequencing 
Name:       express
Version:    1.2.0
Release:    1
License:    Artistic License 2.0
Vendor:     http://bio.math.berkeley.edu/eXpress/
Group:      ComputationalBiology/genomics
Source0:    %{name}-%{version}-src.tgz
Source1:    bamtools-1.0.2.tar.gz
Packager:   TACC - jfonner@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot
requires:   boost149-gcc4_4 = 1.49.0

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME express

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group:   Applications/Biology

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
eXpress is a streaming tool for quantifying the abundances of a set of target sequences from sampled subsequences. Example applications include transcript-level RNA-Seq quantification, allele-specific/haplotype expression analysis (from RNA-Seq), transcription factor binding quantification in ChIP-Seq, and analysis of metagenomic data.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_EXPRESS

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------

%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/bwa-0.5.9
%setup -n %{name}-%{version}-src

# The next command unpacks Source1
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source). 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -n %{name}-%{version}-src -T -D -a 1

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi



# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
#%include mpi-load.inc
#%include mpi-env-vars.inc
# Load additional modules here (as needed)
module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc
module load cmake
module load boost

#-----------------------------
# Build parallel version
#-----------------------------

export MY_EXPRESS_DIR=`pwd`

cd $MY_EXPRESS_DIR
mv ./bamtools*/ ./bamtools/
cd ./bamtools
export MY_BAMTOOLS_DIR=`pwd`

cd $MY_BAMTOOLS_DIR
mkdir build
cd build
cmake ..
make

cd $MY_EXPRESS_DIR/src
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{INSTALL_DIR} ..

cp ./CMakeFiles/express.dir/link.txt ./CMakeFiles/express.dir/link.txt.original
cat ./CMakeFiles/express.dir/link.txt.original|sed -r "s/\s+/\n/g"|awk -v TACC_BOOST_INC=$TACC_BOOST_INC -v TACC_BOOST_LIB=$TACC_BOOST_LIB -v MY_BAMTOOLS_DIR=$MY_BAMTOOLS_DIR -v GCC_LIB=$GCC_LIB 'NR==1{print $0;printf "-I%s\n",TACC_BOOST_INC};NR>1{print};/rdynamic/{exit};END{printf "-Wl,-rpath,%s/lib,-rpath,%s,-rpath,%s -L%s/lib -lbamtools %s/lib/libbamtools.a -L%s -lboost_filesystem -lboost_thread -lboost_system -lboost_program_options -lpthread\n",MY_BAMTOOLS_DIR,TACC_BOOST_LIB,GCC_LIB,MY_BAMTOOLS_DIR,MY_BAMTOOLS_DIR,TACC_BOOST_LIB;}' | tr '\n' ' ' | xargs echo > ./CMakeFiles/express.dir/link.txt

#echo "`which c++` -I$TACC_BOOST_INC CMakeFiles/express.dir/biascorrection.o CMakeFiles/express.dir/bundles.o CMakeFiles/express.dir/fld.o CMakeFiles/express.dir/fragments.o CMakeFiles/express.dir/main.o CMakeFiles/express.dir/mapparser.o CMakeFiles/express.dir/markovmodel.o CMakeFiles/express.dir/mismatchmodel.o CMakeFiles/express.dir/robertsfilter.o CMakeFiles/express.dir/sequence.o CMakeFiles/express.dir/targets.o CMakeFiles/express.dir/threadsafety.o -o express -rdynamic -Wl,-rpath,$MY_BAMTOOLS_DIR/lib,-rpath,$TACC_BOOST_LIB,-rpath,/opt/apps/gcc/4.4.5/lib64/ -L$MY_BAMTOOLS_DIR/lib -lbamtools -L$TACC_BOOST_LIB -lboost_filesystem -lboost_thread -lboost_system -lboost_program_options -lpthread" > $MY_EXPRESS_DIR/src/build/CMakeFiles/express.dir/link.txt

cat ./CMakeFiles/express.dir/link.txt

make CXX_FLAGS="-I$TACC_BOOST_INC -I$MY_BAMTOOLS_DIR/include"
make DESTDIR=$RPM_BUILD_ROOT install

# move other files over
cd $MY_EXPRESS_DIR
cp -r sample_data LICENSE README express-doc.pdf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} built with gcc.
This module makes available the %{PNAME} executable. Documentation for %{PNAME} is in $TACC_EXPRESS_DIR/express-doc.pdf and available online at the publisher\'s website: http://bio.math.berkeley.edu/eXpress/
The %{PNAME} executable can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: life sciences, genomics")
whatis("Keywords: LSC, 2012Q2, Biology, Genomics")
whatis("Description: express - Streaming quantification for high-throughput sequencing")
whatis("URL: http://bio.math.berkeley.edu/eXpress/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
prepend_path("PATH"       ,"%{INSTALL_DIR}/bin")

EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF



#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

