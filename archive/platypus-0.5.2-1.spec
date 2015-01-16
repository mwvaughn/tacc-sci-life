## Platypus
Summary: Platypus - A Haplotype-Based Variant Caller For Next Generation Sequence Data
Name: Platypus
Version: 0.5.2
Release: 1
License: GPL
Vendor: Welcome Trust Centre for Human Genetics
Group: Applications/Life Sciences
Source: Platypus-latest.tgz
Packager: TACC - jcarson@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include ../rpm-dir.inc
%include ../system-defines.inc

%description
Platypus (http://www.well.ox.ac.uk/platypus) is a haplotype-based variant caller. The program integrates the calling of SNP and indel variants of up to 50 bp, using a 3-step process. First, candidates for SNP and indel polymorphisms are generated from the input reads from all population samples and their alignment to the reference sequence. Second, haplotypes are generated from sets of these candidate variants restricted to small windows, and all reads are re-aligned to these haplotypes. Third, an EM algorithm estimates the frequencies of the haplotypes in the population, and determines which haplotypes are supported by the data; the set of haplotypes that have support determine the variants that are reported to be segregating in the population.
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_GATK

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}_%{version} 

%build

%install

%include ../system-load.inc
module purge
module load TACC
module load python

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

echo "Hello echo"
echo $LD_LIBRARY_PATH

./buildPlatypus.sh

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
Platypus (http://www.well.ox.ac.uk/platypus) is a haplotype-based variant caller. The program integrates the calling of SNP and indel variants of up to 50 bp, using a 3-step process. First, candidates for SNP and indel polymorphisms are generated from the input reads from all population samples and their alignment to the reference sequence. Second, haplotypes are generated from sets of these candidate variants restricted to small windows, and all reads are re-aligned to these haplotypes. Third, an EM algorithm estimates the frequencies of the haplotypes in the population, and determines which haplotypes are supported by the data; the set of haplotypes that have support determine the variants that are reported to be segregating in the population.
]]
)

whatis("Name: Platypus")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics");
whatis("Keywords:  Biology, Genomics, Variant Caller")
whatis("URL: http://www.well.ox.ac.uk/platypus")
whatis("Platypus is a haplotype-based variant caller.")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
append_path("PATH",              "%{INSTALL_DIR}/")
prereq ("python")

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
