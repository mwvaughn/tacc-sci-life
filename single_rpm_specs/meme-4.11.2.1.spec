%define		PNAME	meme
Version:	4.11.2_1
Release:	1
License:	GNU
URL:		http://meme-suite.org
Source:		http://meme-suite.org/meme-software/4.11.2/%{PNAME}_%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications/Life Sciences
Summary:	Motif-based sequence analysis tools
Prefix:		/work/03076/gzynda/public/apps

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
#%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
#%include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR      %{MODULE_VAR_PREFIX}MEME
%define APPS /work/03076/gzynda/public/apps

## PACKAGE DESCRIPTION
%description
The MEME Suite allows the biologist to discover novel motifs in collections of unaligned nucleotide or protein sequences, and to perform a wide variety of other motif-based analyses.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
%setup -n %{PNAME}_4.11.2

## BUILD
%build

#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

# Paths are hardcoded, so can't move from prefix
ID=${WORK}/public/apps/meme/4.11.2_1
#BI=${RPM_BUILD_ROOT}/%{INSTALL_DIR}
BI=${RPM_BUILD_ROOT}/$ID

mkdir -p $BI/{bin,lib}

module purge
module load TACC
module load perl python/2.7.9

PATH="$BI/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="$BI/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="${BI}${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base \"${BI}\""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=${BI}"; export PERL_MM_OPT;

PT=$WORK/rpmbuild/SOURCES/meme_perl_deps.tar.gz
if [ -e $PT ]
then
	tar -xzf $PT -C $BI
else
	cpan HTML::Template
	cpan XML::Simple
	cpan XML::Parser::Expat
	cpan XML::Compile::SOAP11
	cpan XML::Compile::WSDL11
	cpan XML::Compile::Transport::SOAPHTTP
	cpan Math::CDF
	( cd $BI && tar -czf $PT lib )
fi

# Install databases
mkdir -p $BI/{LOGS,db}
for url in http://meme-suite.org/meme-software/Databases/motifs/motif_databases.12.12.tgz http://meme-suite.org/meme-software/Databases/gomo/gomo_databases.3.2.tgz
do
	wget $url
	tar -xzf $(basename $url) -C $BI/db
done

if [ "%{PLATFORM}" != "ls5" ]
then
	
	#./configure CC=mpicc CXX=mpicxx CFLAGS="-O3 -xHOST" --with-mpidir=$MPICH_HOME --prefix=%{INSTALL_DIR}
	#./configure CC=icc CXX=icpc CFLAGS="-O3 -xHOST" --prefix=%{INSTALL_DIR} --enable-serial --with-db=$BI/db --with-logs=$BI/LOGS
	./configure CC=icc CXX=icpc CFLAGS="-O3 -xHOST" --prefix=$ID --enable-serial
else
	./configure CC=mpicc CXX=mpicxx CFLAGS="-O3 -xAVX -axCORE-AVX2" --with-mpidir=$MPICH_HOME --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

patch Makefile -i - <<"EOF"
1161c1161
< 	mkdir -p $(MEME_DB)
---
> 	mkdir -p $(DESTDIR)/$(MEME_DB)
1168,1169c1168,1169
< 	mkdir -p $(MEME_LOGS)
< 	chmod a+w $(MEME_LOGS)
---
> 	mkdir -p $(DESTDIR)/$(MEME_LOGS)
> 	chmod a+w $(DESTDIR)/$(MEME_LOGS)
EOF

make -j 16 DESTDIR=${RPM_BUILD_ROOT}
#make -j 16 test
make install DESTDIR=${RPM_BUILD_ROOT}

for fname in packlist perllocal.pod
do
	find /home1/03076/gzynda/rpmbuild/BUILDROOT/tacc-meme-4.11.2_1-1.x86_64/ -type f -name \*${fname} | xargs -n 1 sed -i 's#'/home1/03076/gzynda/rpmbuild/BUILDROOT/tacc-meme-4.11.2_1-1.x86_64'##g'
done

## Install Steps End
#--------------------------------------

#--------------------------------------

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN
 - %{MODULE_VAR}_LIB

for the location of the %{PNAME} distribution. This version of MEME uses the following databases

 - Motif v12.12
 - Gomo  v3.2

located in %{MODULE_VAR}_DB

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Motif")
whatis("Description: Motif-based sequence analysis tools")
whatis("URL: %{url}")

always_load("python/2.7.9","perl")

prepend_path("PATH",		pathJoin("%{INSTALL_DIR}", "bin"))
prepend_path("LD_LIBRARY_PATH",	pathJoin("%{INSTALL_DIR}", "lib"))
prepend_path("PERL5LIB",	pathJoin("%{INSTALL_DIR}", "lib/perl5"))

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_DB",     "%{INSTALL_DIR}/db")
setenv("%{MODULE_VAR}_BIN",	pathJoin("%{INSTALL_DIR}", "bin"))
setenv("%{MODULE_VAR}_LIB",	pathJoin("%{INSTALL_DIR}", "lib"))
EOF
## Modulefile End
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
