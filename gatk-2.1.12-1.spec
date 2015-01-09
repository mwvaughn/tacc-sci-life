# $Id$

## GenomeAnalysisToolKit

Summary: GATK - Genome Analysis Toolkit
Name: gatk
Version: 2.1.12 
Release: 1
License: MIT License
Vendor: Broad Institute
Group: Applications/Life Sciences
Source: GenomeAnalysisTK-2.1-12.tar.bz2 
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME gatk
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_GATK

%description
The GATK is a structured software library that makes writing efficient analysis tools using next-generation sequencing data very easy, and second it's a suite of tools for working with human medical resequencing projects such as 1000 Genomes and The Cancer Genome Atlas. These tools include things like a depth of coverage analyzers, a quality score recalibrator, a SNP/indel caller and a local realigner.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n GenomeAnalysisTK-2.1-12-ga99c19d 

%build

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi


module purge
module load TACC

echo "GATK is distributed as compiled Java. No compilation necessary."

%install
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
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME} distribution.

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
whatis("The GATK is a structured software library that makes writing efficient analysis tools using next-generation sequencing data very easy, and second it's a suite of tools for working with human medical resequencing projects such as 1000 Genomes and The Cancer Genome Atlas. These tools include things like a depth of coverage analyzers, a quality score recalibrator, a SNP/indel caller and a local realigner.")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

prereq ("jdk64")

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

