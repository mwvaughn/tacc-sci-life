# $Id$

Summary: FASTX Toolkit is a collection of command line tools for Short-Reads FASTA/FASTQ files preprocessing.
Name: fastx_toolkit
Version: 0.0.13.2
Release: 1
License: GPL
Group: Applications/Life Sciences
Source0:  fastx_toolkit-%{version}.tar.bz2
Packager: TACC - vaughn@tacc.utexas.edu jfonner@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot
Requires: libgtextutils-0.6-2 = 0.6

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME fastx_toolkit
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_FASTX

%description
The FASTX-Toolkit is a collection of command line tools for Short-Reads FASTA/FASTQ files preprocessing.

%prep
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version}

%build


if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc/4.4.5
module load libgtextutils

export GTEXTUTILS_CFLAGS="-I$TACC_LIBGTEXTUTILS_INC"
export GTEXTUTILS_LIBS="-L$TACC_LIBGTEXTUTILS_LIB -lgtextutils"

./configure --prefix=%{INSTALL_DIR} LDFLAGS=" -Wl,-rpath,$TACC_LIBGTEXTUTILS_LIB,-rpath,$GCC_LIB "
make

%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT install

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

