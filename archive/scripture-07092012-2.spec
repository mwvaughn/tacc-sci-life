# $Id$

## Scripture
## mkdir scripture-ddmmyyy && cd scripture-ddmmyy
## wget "ftp://ftp.broadinstitute.org/pub/papers/lincRNA/scripture.jar"
## cd .. && tar -czvf scripture-07092012.tgz scripture-07092012

Summary: Scripture
Name: scripture
Version: 07092012
Release: 2
License: BSD
Vendor: Broad Institute
Group: Applications/Life Sciences
Source:  scripture-07092012.tgz
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

# Disable Java jar repacking
%define __jar_repack %{nil}

%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_SCRIPTURE

%description
Scripture is a method for transcriptome reconstruction that relies solely on RNA-Seq reads and an assembled genome to build a transcriptome ab initio. The statistical methods to estimate read coverage significance are also applicable to other sequencing data. Scripture also has modules for ChIP-Seq peak calling.

%prep
rm   -rf $RPM_BUILD_ROOT

%setup -n scripture-07092012

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load TACC

echo "Scripture is distributed as compiled Java. No compilation necessary."

cp -R ./scripture.jar $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME} distribution.

Invoke as follows:

java <jvm-args> -jar $%{MODULE_VAR}_DIR/scripture.jar -task <task name> [parameters]

Version %{version}
]]
)

whatis("Name: Scripture")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics");
whatis("Keywords:  Biology, Genomics, Genotyping, RNAseq, ChIPseq")
whatis("URL: http://www.broadinstitute.org/software/scripture/")
whatis("Scripture is a method for transcriptome reconstruction that relies solely on RNA-Seq reads and an assembled genome to build a transcriptome ab initio. The statistical methods to estimate read coverage significance are also applicable to other sequencing data. Scripture also has modules for ChIP-Seq peak calling.")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

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

