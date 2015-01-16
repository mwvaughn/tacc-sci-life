# $Id$

Summary: FASTX Toolkit is a collection of command line tools for Short-Reads FASTA/FASTQ files preprocessing.
Name: fastx_toolkit
Version: 0.0.13.2
Release: 2
License: GPL
Group: Applications/Life Sciences
Source0:  fastx_toolkit-%{version}.tar.bz2
Packager: TACC - vaughn@tacc.utexas.edu jfonner@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot
# Requires: libgtextutils-0.6-2 = 0.6

%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME fastx_toolkit
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_FASTX

%description
The FASTX-Toolkit is a collection of command line tools for Short-Reads FASTA/FASTQ files preprocessing.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{PNAME}-%{version}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc/4.7.1

export FASTX_DIR=`pwd`
wget "http://hannonlab.cshl.edu/fastx_toolkit/libgtextutils-0.6.1.tar.bz2"
tar -jxvf libgtextutils-0.6.1.tar.bz2
cd libgtextutils-0.6.1
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

./configure --prefix=%{INSTALL_DIR} LDFLAGS=" -Wl,-rpath,$TACC_LIBGTEXTUTILS_LIB,-rpath,/opt/apps/gcc/4.7.1/lib64 "

make && make DESTDIR=$RPM_BUILD_ROOT install

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

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

