## GenomeAnalysisToolKit
Summary: GATK - Genome Analysis Toolkit
Name: gatk
Version: 2.3.9
Release: 1
License: MIT License
Vendor: Broad Institute
Group: Applications/Life Sciences
Source: GenomeAnalysisTK-2.3-9.tar.bz2
Packager: TACC - jiao@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc
%include ../system-defines.inc

%description
The GATK is a structured software library that makes writing efficient analysis tools using next-generation sequencing data very easy, and second it's a suite of tools for working with human medical resequencing projects such as 1000 Genomes and The Cancer Genome Atlas. These tools include things like a depth of coverage analyzers, a quality score recalibrator, a SNP/indel caller and a local realigner.
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_GATK

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n GenomeAnalysisTK-2.3-9-ge5ebf34

%build

%install

%include ../system-load.inc
module purge
module load TACC

echo "GATK is distributed as compiled Java. No compilation necessary."

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{name} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{name} distribution.


Invoke as follows:

java <jvm-args> -jar $%{MODULE_VAR}_DIR/GenomeAnalysisTK.jar -T <function>  [opts]

Version %{version}
]]
)

whatis("Name: GenomeAnalysisTK")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics");
whatis("Keywords:  Biology, Genomics, Genotyping, Resequencing, SNP")
whatis("URL: http://www.broadinstitute.org/gsa/wiki/index.php/The_Genome_Analysis_Toolkit")
whatis("Description:  The GATK is a structured software library that makes writing efficient analysis tools using next-generation sequencing data very easy, and second it's a suite of tools for working with human medical resequencing projects such as 1000 Genomes and The Cancer Genome Atlas. These tools include things like a depth of coverage analyzers, a quality score recalibrator, a SNP/indel caller and a local realigner.")

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

