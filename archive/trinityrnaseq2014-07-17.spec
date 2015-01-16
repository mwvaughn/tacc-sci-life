Summary:    Trinity De novo RNA-Seq Assembler
Name:       trinityrnaseq
Version:    r20140717
Release:    1
License:    BSD
Vendor:     Broad Institute
Group: Applications/Life Sciences
Source:     %{name}_%{version}.tar.gz
Packager:   TACC - gzynda@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include ../rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define APPS    /opt/apps
%define MODULES modulefiles
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define PNAME %{name}
%define MODULE_VAR TACC_TRINITY

%define __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:/usr/lib/rpm/redhat/brp-strip %{__strip}} \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}
# Turn off dependency checking. Trinity bundles so much that it's 
# frankly preposterous to do this
AutoReqProv: no

%description
Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads. Trinity partitions the sequence data into many individual de Bruijn graphs, each representing the transcriptional complexity at at a given gene or locus, and then processes each graph independently to extract full-length splicing isoforms and to tease apart transcripts derived from paralogous genes.

## PREP
%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
%setup -n %{name}_%{version}

%build
%include ../system-load.inc
module purge
module load TACC
if [[ `hostname` == *.ls4.tacc.utexas.edu ]]
then
	module swap intel gcc/4.7.1
	make -j 4
else
	module load intel/14.0.1.106
	# make inchworm
	make inchworm_target TRINITY_COMPILER=intel INCHWORM_CONFIGURE_FLAGS='CXXFLAGS="-mkl" CXX=icpc'
	# make chrysalis
	make chrysalis_target TRINITY_COMPILER=intel SYS_OPT="" SYS_LIBS="-mkl -pthread"
	# make plugins
	cd trinity-plugins/
	# make jellyfish
	JELLYFISH_CODE=jellyfish-2.1.3
	tar -zxvf ${JELLYFISH_CODE}.tar.gz && ln -sf ${JELLYFISH_CODE} tmp.jellyfish
        cd ./tmp.jellyfish/ && ./configure CC=icc CXX=icpc --enable-static --disable-shared --prefix=`pwd` && make LDFLAGS="-pthread" AM_CPPFLAGS="-Wall -Wnon-virtual-dtor -mkl -std=c++11 -I"`pwd`"/include"
	cd ..
        mv tmp.jellyfish jellyfish
	# make rsem
	RSEM_CODE=rsem-1.2.15
	tar -zxvf ${RSEM_CODE}.tar.gz && ln -sf ${RSEM_CODE} tmp.rsem
        cd ./tmp.rsem && make CC=icc CFLAGS="-Wall -c -I. -mkl -static" COFLAGS="-Wall -fast -mkl -c -static -I."
	cd ..
        mv tmp.rsem rsem
	# make transdecoder
	TRANSDECODER_CODE=TransDecoder_r20140704
	tar -zxvf ${TRANSDECODER_CODE}.tar.gz && ln -sf ${TRANSDECODER_CODE} tmp.transdecoder
        mv ./tmp.transdecoder transdecoder
	# make parafly
	cd TransDecoder_r20140704/3rd_party/parafly
	./configure --prefix=$PWD/../../util CC=icc CXX=icpc
	make install CPPFLAGS="-fast"
	cd ../../../
	# make cdhit
	cd TransDecoder_r20140704/3rd_party/cd-hit
	make CXXFLAGS="-openmp -mkl -O3" LDFLAGS="-o" CC=icpc
	make install PREFIX=../../util/bin
	cd ../../../../
	# make tests
	make all
fi

%install
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf Inchworm/src
rm trinity-plugins/rsem-1.2.15/*.h trinity-plugins/rsem-1.2.15/*.cpp
rm -rf trinity-plugins/jellyfish/jellyfish
rm -rf trinity-plugins/jellyfish/lib
rm -rf Chrysalis/obj
find . -name *.tar.gz | xargs -n 1 rm
cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}/
chmod -R a+rX $RPM_BUILD_ROOT/%{INSTALL_DIR}

##################################################
#	Module Section
##################################################
# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_BUTTERFLY, %{MODULE_VAR}_CHRYSALIS, %{MODULE_VAR}_INCHWORM and %{MODULE_VAR}_INCHWORM_BIN for the location of the %{PNAME} distribution.

Please refer to http://trinityrnaseq.sourceforge.net/#running_trinity for help running trinity.

BioITeam also provides a script for efficient job submission - %{MODULE_VAR}_SUBMIT
	%{MODULE_VAR}_SUBMIT -h

Version %{version}
]])
whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, transcriptomics")
whatis("Keywords: Biology, Assembly, RNAseq, Transcriptome")
whatis("URL: http://trinityrnaseq.sourceforge.net/")
whatis("Description: Package for RNA-Seq de novo Assembly")

prepend_path("PATH"       	, "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_DIR"	, "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_SUBMIT"	, "/corral-repl/utexas/BioITeam/bin/assemble_trinity")
setenv("%{MODULE_VAR}_BUTTERFLY", "%{INSTALL_DIR}/Butterfly")
setenv("%{MODULE_VAR}_CHRYSALIS", "%{INSTALL_DIR}/Chrysalis")
setenv("%{MODULE_VAR}_INCHWORM"	, "%{INSTALL_DIR}/Inchworm")
setenv("%{MODULE_VAR}_INCHWORM_BIN", "%{INSTALL_DIR}/Inchworm/bin")
setenv("%{MODULE_VAR}_UTIL"	, "%{INSTALL_DIR}/util")
setenv("%{MODULE_VAR}_PLUGINS"	, "%{INSTALL_DIR}/trinity-plugins")
EOF

echo "Finished first cat\n"

if [[ `hostname` == *.stampede.tacc.utexas.edu ]]
then
	cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
setenv("MKL_MIC_ENABLE"	, "1")
setenv("OMP_NUM_THREADS","16")
setenv("MIC_OMP_NUM_THREADS","240")
prereq("intel/14.0.1.106","bowtie/1.1.1","samtools")
EOF
else
	cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
setenv("OMP_NUM_THREADS","12")
prereq("samtools","gcc/4.7.1","bowtie/1.1.1")
EOF
fi

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
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
