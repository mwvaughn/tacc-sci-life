## GenomeAnalysisToolKit
Summary: GATK - Genome Analysis Toolkit
Name: gatk
#Illegal char '-' in version if it is 3.1-1
Version: 3.1.1
Release: 1
License: MIT License
Vendor: Broad Institute
Group: Applications/Life Sciences
Source: GenomeAnalysisTK-3.1-1.tar.bz2
Packager: TACC - mattcowp@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include ../rpm-dir.inc
%include ../system-defines.inc

%description
The GATK is a structured software library that makes writing efficient analysis tools using next-generation sequencing data very easy, and second it is a suite of tools for working with human medical resequencing projects such as 1000 Genomes and The Cancer Genome Atlas. These tools include things like a depth of coverage analyzers, a quality score recalibrator, a SNP/indel caller and a local realigner.
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_GATK

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n GenomeAnalysisTK-3.1-1

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
"The GATK is a structured software library that makes writing efficient analysis tools using next-generation sequencing data very easy, and second it is a suite of tools for working with human medical resequencing projects such as 1000 Genomes and The Cancer Genome Atlas. These tools include things like a depth of coverage analyzers, a quality score recalibrator, a SNP/indel caller and a local realigner.

GATK 3.1 is a special build released, co-developed by the Broad Institute and Intel, as part of an ongoing effort to improve the performance of GATK.

In version 3.1, the HaplotypeCaller is the first GATK function to be AVX optimized.  NOTE THAT THIS IS STILL AN EXPERIIMENTAL IMPLEMENTATION AND YOUR RESULTS MAY BE AFFECTED;  PROCEED WITH CAUTION.

To enable AVX in the HaplotypeCaller, you must add the following flag: '-pairHMM VECTOR_LOGLESS_CACHING'.  Also, note that the new HaplotypeCaller does not scale well with the number of threads, so `-nct` flags should removed or set to a value no greater than 2.  In our testing, `-nct > 2` actually imposed performance penalties.  This will be resolved in the next GATK release.

A final note, in limited testing TACC staff were experiencing a ~2X performance boost of the HaplotypeCaller when running with AVX enabled.

For more information:  http://www.broadinstitute.org/gatk/blog?id=3930

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
whatis("The GATK is a structured software library that makes writing efficient analysis tools using next-generation sequencing data very easy, and second it is a suite of tools for working with human medical resequencing projects such as 1000 Genomes and The Cancer Genome Atlas. These tools include things like a depth of coverage analyzers, a quality score recalibrator, a SNP/indel caller and a local realigner.")

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
