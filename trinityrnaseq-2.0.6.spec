Name:       trinityrnaseq
Summary:    Trinity De novo RNA-Seq Assembler
Version:    2.0.6
Release:    1
License:    BSD
Vendor:     Broad Institute
Group:      Applications/Life Sciences
Source:     v%{version}.tar.gz
Packager:   TACC - gzynda@tacc.utexas.edu
Prefix:    /opt/apps

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}TRINITY
%define PNAME       %{name}

%package -n %{name}-%{comp_fam_ver}
Summary:    Trinity De novo RNA-Seq Assembler
Group:      Applications/Life Sciences

%define __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:/usr/lib/rpm/redhat/brp-strip %{__strip}} \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}
# Turn off dependency checking. Trinity bundles so much that it's 
# frankly preposterous to do this
AutoReqProv: no

## PACKAGE DESCRIPTION
%description
%description -n %{name}-%{comp_fam_ver}
Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads. Trinity partitions the sequence data into many individual de Bruijn graphs, each representing the transcriptional complexity at at a given gene or locus, and then processes each graph independently to extract full-length splicing isoforms and to tease apart transcripts derived from paralogous genes.

## PREP
%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}

## SETUP
%setup -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start
module purge
module load TACC
%include ./include/compiler-load.inc

if [ -n "$GCC_LIB" ] || [[ `hostname` == *.ls4.tacc.utexas.edu ]]
then
	make -j 4
else  
	module load intel/14.0.1.106
	# make inchworm
	make inchworm_target TRINITY_COMPILER=intel INCHWORM_CONFIGURE_FLAGS='CXXFLAGS="-mkl" CXX=icpc'
	# make chrysalis
	make chrysalis_target TRINITY_COMPILER=intel SYS_OPT="" SYS_LIBS="-mkl -pthread"
	# make plugins
	cd trinity-plugins/
	# make jellyfish - all tests passed
	JELLYFISH_CODE=jellyfish-2.1.4
	tar -zxvf ${JELLYFISH_CODE}.tar.gz && ln -sf ${JELLYFISH_CODE} tmp.jellyfish
        cd ./tmp.jellyfish/ && ./configure CC=icc CXX=icpc --enable-static --disable-shared --prefix=`pwd` && make LDFLAGS="-pthread" AM_CPPFLAGS="-Wall -Wnon-virtual-dtor -mkl -std=c++11 -I"`pwd`"/include"
	cd ..
        mv tmp.jellyfish jellyfish
	# make rsem
	RSEM_CODE=rsem-1.2.19
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

rm -rf Inchworm/src
rm -rf trinity-plugins/jellyfish/jellyfish
rm -rf trinity-plugins/jellyfish/lib
rm -rf Chrysalis/obj
find . -name \*.tar.gz | xargs -n 1 rm
find . -name \*.[ch]pp | xargs -n 1 rm
find . -name \*.[oc] | xargs -n 1 rm
cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}/
chmod -R a+rX $RPM_BUILD_ROOT/%{INSTALL_DIR}

## Install Steps End

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
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
if [ -n "$GCC_LIB" ] || [[ `hostname` == *.ls4.tacc.utexas.edu ]]
then
	cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
setenv("OMP_NUM_THREADS","12")
prereq("samtools","gcc/4.7.1","bowtie/1.1.1")
EOF
else
	cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
setenv("MKL_MIC_ENABLE"	, "1")
setenv("OMP_NUM_THREADS","16")
setenv("MIC_OMP_NUM_THREADS","240")
prereq("intel/14.0.1.106","bowtie/1.1.1","samtools")
EOF
fi

## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# VERSON FILE
#------------------------------------------------
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}-%{comp_fam_ver}
#%files 

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}
#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Remove the installation files now that the RPM has been generated
cd /tmp && rm -rf $RPM_BUILD_ROOT
