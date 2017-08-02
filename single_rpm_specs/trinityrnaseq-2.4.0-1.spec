%define PNAME trinityrnaseq
Version: 2.4.0
Release: 1
Summary: Trinity - De novo RNA-Seq Assembler
License: BSD
Group: Applications/Life Sciences
Source: /work/03076/gzynda/rpmbuild/SOURCES/trinityrnaseq-2.4.0.tar.gz
URL: https://github.com/trinityrnaseq/trinityrnaseq
Packager: TACC - gzynda@tacc.utexas.edu

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}TRINITY

## PACKAGE DESCRIPTION
%description
Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads. Trinity partitions the sequence data into many individual de Bruijn graphs, each representing the transcriptional complexity at at a given gene or locus, and then processes each graph independently to extract full-length splicing isoforms and to tease apart transcripts derived from paralogous genes.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

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

module purge
module load TACC
module use /work/03076/gzynda/%{PLATFORM}/public/apps/modulefiles

ml samtools/1.3.1 jellyfish/2.2.6

# Set system specific variables
case %{PLATFORM} in
stampedeknl)
        # Login nodes are CORE-AVX2, compute nodes are MIC-AVX512
        export CFLAGS="-xCORE-AVX2 -axMIC-AVX512 -O3 -ipo"
	pyv="python/2.7.13"
        ;;
ls5)
        # Compute nodes are CORE-AVX2 and largemem nodes are AVX
        export CFLAGS="-xAVX -axCORE-AVX2 -O3 -ipo"
	pyv="python/2.7.12"
        ;;
wrangler)
        # Assume architecture is homogeneous throughout system.
        export CFLAGS="-xHOST -O3 -ipo"
	pyv="python/2.7.9"
        ;;
hikari)
        # Assume architecture is homogeneous throughout system.
        export CFLAGS="-xHOST -O3 -ipo"
	pyv="gcc/5.2.0 python/2.7.11"
        ;;
stampede)
        # Assume architecture is homogeneous throughout system.
        export CFLAGS="-xHOST -O3 -ipo"
	pyv="perl python/2.7.12"
        ;;
esac
export CXXFLAGS="$CFLAGS" CC=icc CXX=icpc LDFLAGS="-Wl,-rpath,${ICC_LIB}"
module load $pyv

#------------------------------------------------
# PATCH FILES
#------------------------------------------------
## Patch plugins
patch trinity-plugins/Makefile -i - << 'EOF'
11a12
> 	rm -rf scaffold_iworm_contigs
14,15c15
< 	ln -sf ${TRIMMOMATIC_CODE} Trimmomatic
< 
---
> 	mv ${TRIMMOMATIC_CODE} Trimmomatic
18,24c18
< 	tar xvf samtools-1.3.1.tar.bz2
< 	cd samtools-1.3.1 && ./configure --without-curses --prefix=`pwd`
< ifeq ($(OS),Darwin)
< 	sed -i.bak s/-rdynamic//g samtools-1.3.1/Makefile
< endif
< 	cd samtools-1.3.1 && $(MAKE)
< 	mv samtools-1.3.1/samtools ./BIN/.
---
> 	rm samtools-1.3.1.tar.bz2
29a24,25
> 	rm -rf seqtk-trinity*
> 	rm BIN/README
32,35c28
< 	tar -zxvf ${JELLYFISH_CODE}.tar.gz && ln -sf ${JELLYFISH_CODE} tmp.jellyfish
< 	cd ./tmp.jellyfish/ && ./configure CC=gcc CXX=g++ --enable-static --disable-shared --prefix=`pwd` && $(MAKE) LDFLAGS="-lpthread -all-static" AM_CPPFLAGS="-Wall -Wnon-virtual-dtor -I"`pwd`"/include"
< 	mv tmp.jellyfish jellyfish
< 
---
> 	rm ${JELLYFISH_CODE}.tar.gz
39c32,33
< 	ln -sf ${PARAFLY_CODE} parafly
---
> 	mkdir -p parafly/bin && mv ${PARAFLY_CODE}/bin/* parafly/bin/
> 	rm -rf ${PARAFLY_CODE}
51c45,47
< 	cd slclust && $(MAKE) install
---
> 	cd slclust/src && make CXX=icpc CXXFLAGS="$(CFLAGS) -I../include -fast" install
> 	mv slclust/bin/* BIN/
> 	rm -rf slclust/* && mkdir slclust/bin && mv BIN/slclust slclust/bin/
54c50
< 	cd COLLECTL && tar xvf ${COLLECTL_CODE}.src.tar.gz && ln -sf ${COLLECTL_CODE} collectl
---
> 	cd COLLECTL && tar xvf ${COLLECTL_CODE}.src.tar.gz && rm ${COLLECTL_CODE}.src.tar.gz && mv ${COLLECTL_CODE} collectl && rm -rf collectl/docs
EOF
## Patch main Makefile
patch Makefile -i - << 'EOF'
10,11c10,11
<  INCHWORM_CONFIGURE_FLAGS = CXX=icpc CXXFLAGS="-fast"
<  CHRYSALIS_MAKE_FLAGS = COMPILER=icpc
---
>  INCHWORM_CONFIGURE_FLAGS = CXX=icpc CXXFLAGS="$(CFLAGS) -no-prec-div"
>  CHRYSALIS_MAKE_FLAGS = COMPILER=icpc SYS_OPT="$(CFLAGS)" DEBUG=no
EOF
## Patch install tests
patch util/support_scripts/trinity_install_tests.sh -i - << 'EOF'
62c62
< if [ -e "trinity-plugins/BIN/samtools" ]
---
> if [ -x "$(which samtools 2>/dev/null)" ]
EOF

#------------------------------------------------
# Make Trinity
#------------------------------------------------
make -j 8 TRINITY_COMPILER=intel
make -j 8 TRINITY_COMPILER=intel plugins

# Remove unnecessary things
rm -rf trinityrnaseq.wiki
rm Makefile
rm -rf Butterfly/[^B]*
back=$PWD
# clean up Chrysalis
cd Chrysalis
mv analysis/ReadsToComponents.pl .
find . -type f ! -executable | xargs -n 1 rm
find . -mindepth 1 -maxdepth 1 -type d | xargs -n 1 rm -rf
# clean up plugins
cd $back/trinity-plugins && rm Makefile
rm README
# clean up Inchworm
cd $back/Inchworm
rm -rf src config* aclocal.m4 depcomp install-sh Make* missing notes stamp-h1
cd $back

# Remove Java stack size parameter
sed -i 's/ -Xss$bflyHeapSpaceInit//' Trinity
# Update jellyfish location
 find . -type f -exec file {} \; | grep text | cut -f 1 -d ":" | xargs -n 1 grep -H "my \$JELLYFISH_DIR" | grep -v cmd | cut -f 1 -d ":" | sort -u | xargs -n 1 sed -i '/my $JELLYFISH_DIR/c\my $JELLYFISH_DIR = $ENV{"TACC_JELLYFISH_DIR"};'
# Delete docker
rm -rf Docker
# Delete galaxy scripts
rm -rf galaxy-plugin

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help (
[[
The %{PNAME} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution

Trinity and all utility scripts are automaticially added to your path.

Documentation can be found online at %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: assembly, transcript, genomics")
whatis("URL: %{url}")
whatis("Description: Trinity - De novo RNA-Seq Assembler")

prepend_path("PATH",			"%{INSTALL_DIR}")
prepend_path("PATH",			"%{INSTALL_DIR}/util")

setenv ("%{MODULE_VAR}_DIR",		"%{INSTALL_DIR}")
setenv ("KMP_AFFINITY",			"scatter")

family("trinity")

always_load("bowtie/2.3.2","samtools/1.3.1","jellyfish/2.2.6")
%if "%{PLATFORM}" == "stampede" 
	always_load("perl","java")
%endif
%if "%{PLATFORM}" == "ls5"
	always_load("perl","java")
%endif
%if "%{PLATFORM}" == "wrangler"
	prereq("intel/15.0.3")
%endif
EOF
## Module File End
#--------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}

## POST 
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
