#
# Greg zynda
# 2018-01-03
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

%define shortsummary De novo RNA-Seq Assembler
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name trinityrnaseq

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 5
%define patch_version 1

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc                  
%include ./include/%{PLATFORM}/compiler-defines.inc
#%include ./include/%{PLATFORM}/mpi-defines.inc
%include ./include/%{PLATFORM}/name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
########################################

Release:   1
License:   BSD
Group:     Applications/Life Sciences
URL:       https://github.com/trinityrnaseq/trinityrnaseq
Packager:  TACC - email@tacc.utexas.edu
Source:    Trinity-v%{pkg_version}.tar.gz

%package %{PACKAGE}
Summary: %{shortsummary}
Group:   Applications/Life Sciences
%description package
%{pkg_base_name}: %{shortsummary}

%package %{MODULEFILE}
Summary: The modulefile RPM
Group:   Lmod/Modulefiles
%description modulefile
Module file for %{pkg_base_name}

%description
%{pkg_base_name}: %{shortsummary}

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Comment this out if pulling from git
%setup -n trinityrnaseq-Trinity-v%{pkg_version}
# If using multiple sources. Make sure that the "-n" names match.
#%setup -T -D -a 1 -n %{pkg_base_name}-%{pkg_version}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include ./include/%{PLATFORM}/system-load.inc
##################################
# If using build_rpm
##################################
%include ./include/%{PLATFORM}/compiler-load.inc
#%include ./include/%{PLATFORM}/mpi-load.inc
#%include ./include/%{PLATFORM}/mpi-env-vars.inc
##################################
# Manually load modules
##################################
module load samtools/1.6 jellyfish/2.2.6 python
##################################

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================

export CXXFLAGS="-O3 %{TACC_OPT} -ipo"
export LDFLAGS="-Wl,-rpath,${ICC_LIB}"

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
40a32
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

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message = [[
The %{pkg_base_name} module file defines the following environment variables:
	%{MODULE_VAR}_DIR - the location of the %{pkg_base_name} distribution

Trinity and all utility scripts are automaticially added to your path.

Documentation can be found online at %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: assembly, transcript, genomics")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

prepend_path("PATH",			"%{INSTALL_DIR}")
prepend_path("PATH",			"%{INSTALL_DIR}/util")

setenv ("%{MODULE_VAR}_DIR",		"%{INSTALL_DIR}")
setenv ("KMP_AFFINITY",			"scatter")

family("trinity")

always_load("bowtie/2.3.4","samtools/1.6","jellyfish/2.2.6","python")
%if "%{PLATFORM}" == "stampede" 
	always_load("perl","java")
%endif
%if "%{PLATFORM}" == "ls5"
	always_load("perl","java")
%endif
EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/scripts/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include ./include/%{PLATFORM}/post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include ./include/%{PLATFORM}/post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include ./include/%{PLATFORM}/post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT
