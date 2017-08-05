#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME fastx_toolkit
Version:  0.0.14
Release:  1
License:  GPL
Vendor:   Hannon Lab
Group:    Applications/Life Sciences
Source0:  fastx_toolkit-%{version}.tar.bz2
Source1:  libgtextutils-0.7.tar.gz
Packager: TACC - jcarson@tacc.utexas.edu vaughn@tacc.utexas.edu jfonner@tacc.utexas.edu
Summary:  FASTX Toolkit is a collection of command line tools for Short-Reads FASTA/FASTQ files preprocessing.

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR %{MODULE_VAR_PREFIX}FASTX

%description
The FASTX-Toolkit is a collection of command line tools for Short-Reads FASTA/FASTQ files preprocessing.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm  -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm  -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup  -n %{PNAME}-%{version}

# The next command unpacks Source1
# -b <n> means unpack the nth source *before* changing directories.
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source).
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -T -D -a 1 -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module swap $TACC_FAMILY_COMPILER gcc

export FASTX_DIR=`pwd`
cd libgtextutils-*
export GTEXT_SRC=`pwd`
./configure --prefix=$GTEXT_SRC && make && make install
cd $FASTX_DIR

export TACC_LIBGTEXTUTILS_INC="$GTEXT_SRC/include/gtextutils"
export TACC_LIBGTEXTUTILS_LIB="$GTEXT_SRC/lib"

export GTEXTUTILS_CFLAGS="-I$TACC_LIBGTEXTUTILS_INC"
export GTEXTUTILS_LIBS="-L$TACC_LIBGTEXTUTILS_LIB -lgtextutils"

set +x
echo $TACC_LIBGTEXTUTILS_INC
echo $TACC_LIBGTEXTUTILS_LIB
echo $GTEXTUTILS_CFLAGS
echo $GTEXTUTILS_LIBS
set -x

./configure --prefix=%{INSTALL_DIR} LDFLAGS=" -Wl,-rpath,$GCC_LIB "

make && make DESTDIR=$RPM_BUILD_ROOT install

cp -r libgtextutils* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_BIN for the location of the %{PNAME}
distribution.

Version %{version}
]]
)

whatis("Name: fastx")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing")
whatis("URL: http://hannonlab.cshl.edu/fastx_toolkit/index.html")
whatis("Description: FASTX Toolkit is a collection of command line tools for Short-Reads FASTA/FASTQ files preprocessing.")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",   "%{INSTALL_DIR}/libgtextutils-0.7/lib")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

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

if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
    $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
