# $Id$

# To build
## 1) Hard-link to Intel Boost 1.49.0
## 2) Build and install my OWN samtools in $RPMBUILD/deps

Summary: TopHat2 - fast splice junction mapper for RNA-Seq reads.
Name: tophat
Version: 2.0.4
Release: 1
License: GPLv2
Group: Applications/Life Sciences
Source0:  tophat-2.0.4.tar.gz
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME tophat
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_TOPHAT

%description
TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons. 

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n tophat-2.0.4

%build

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi


module purge
module load TACC
module swap intel gcc
module load samtools

./configure --prefix=%{INSTALL_DIR} --enable-intel64  --with-boost=/opt/apps/intel11_1/boost/1.49.0 --with-bam=/home1/01374/vaughn/a/deps

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

whatis("Name: TopHat")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, RNAseq, Transcriptome profiling, Alignment")
whatis("URL: http://tophat.cbcb.umd.edu/")
whatis("Description: TopHat2 is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons.")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

prereq ("bowtie")

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

