#
# Name
# 2017-08-01
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

%define shortsummary Memory-efficient short read (NGS) aligner
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name bowtie

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 3
%define patch_version 2

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
URL:       http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
Packager:  TACC - gzynda@tacc.utexas.edu
Source:    %{pkg_base_name}2-%{pkg_version}-source.zip

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
%setup -n %{pkg_base_name}2-%{pkg_version}
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
# module load
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

sed -i 's/$(PTHREAD_LIB) -ltbb -ltbbmalloc_proxy/-ltbb -lstdc++ -lpthread/g' Makefile
patch -p1 << "EOF"
diff --git a/endian_swap.h b/endian_swap.h
index aec6295..591aa4a 100644
--- a/endian_swap.h
+++ b/endian_swap.h
@@ -90,10 +90,8 @@ static inline T endianizeU(T u, bool toBig) {
 	}
 	if(sizeof(T) == 4) {
 		return endianSwapU32((uint32_t)u);
-	} else if(sizeof(T) == 8) {
-		return endianSwapU64((uint64_t)u);
 	} else {
-		assert(false);
+		return endianSwapU64((uint64_t)u);
 	}
 }
 
@@ -108,10 +106,8 @@ static inline T endianizeI(T i, bool toBig) {
 	}
 	if(sizeof(T) == 4) {
 		return endianSwapI32((int32_t)i);
-	} else if(sizeof(T) == 8) {
-		return endianSwapI64((int64_t)i);
 	} else {
-		assert(false);
+		return endianSwapI64((int64_t)i);
 	}
 }
 
diff --git a/word_io.h b/word_io.h
index b2752a3..1ce977c 100644
--- a/word_io.h
+++ b/word_io.h
@@ -56,10 +56,8 @@ static inline T readU(std::istream& in, bool swap) {
 	if(swap) {
 		if(sizeof(T) == 4) {
 			return endianSwapU32(x);
-		} else if(sizeof(T) == 8) {
-			return endianSwapU64(x);
 		} else {
-			assert(false);
+			return endianSwapU64(x);
 		}
 	} else {
 		return x;
@@ -76,10 +74,8 @@ static inline T readU(FILE* in, bool swap) {
 	if(swap) {
 		if(sizeof(T) == 4) {
 			return endianSwapU32(x);
-		} else if(sizeof(T) == 8) {
-			return endianSwapU64(x);
 		} else {
-			assert(false);
+			return endianSwapU64(x);
 		}
 	} else {
 		return x;
@@ -94,10 +90,8 @@ static inline T readI(std::istream& in, bool swap) {
 	if(swap) {
 		if(sizeof(T) == 4) {
 			return endianSwapI32(x);
-		} else if(sizeof(T) == 8) {
-			return endianSwapI64(x);
 		} else {
-			assert(false);
+			return endianSwapI64(x);
 		}
 	} else {
 		return x;
@@ -113,10 +107,8 @@ static inline T readI(FILE* in, bool swap) {
 	if(swap) {
 		if(sizeof(T) == 4) {
 			return endianSwapI32(x);
-		} else if(sizeof(T) == 8) {
-			return endianSwapI64(x);
 		} else {
-			assert(false);
+			return endianSwapI64(x);
 		}
 	} else {
 		return x;
-- 
2.9.0
EOF
TR=$TBBROOT
# Since LDFLAGS is not used in bowtie's compilation, we hijack EXTRA_FLAGS to carry the rpath payload

case "%{PLATFORM}" in
	ls5)
		TL=${TR}/lib/intel64/gcc4.4
		TI=${TR}/include
		;;
	stampede2)
		TL=${TR}/lib/intel64/gcc4.7
		TI=${TR}/include
		;;
	stampede)
		TL=${TR}/lib/intel64/gcc4.4
		TI=${TR}/include
		;;
	hikari)
		TL=${TR}/lib/intel64/gcc4.4
		TI=${TR}/include
		;;
	*)
		echo "Please handle %{PLATFORM}"; exit 1
		;;
esac

make RELEASE_BIN=1 CC=icc CXX=icpc AR=xiar WITH_AFFINITY=1 RELEASE_FLAGS="-O3 -m64 %{TACC_OPT} -ipo" EXTRA_FLAGS="-I${TI} -L${TL} -Wl,-rpath,${TL}" prefix=%{INSTALL_DIR} DESTDIR=${RPM_BUILD_ROOT} -j1
make RELEASE_BIN=1 CC=icc CXX=icpc AR=xiar WITH_AFFINITY=1 RELEASE_FLAGS="-O3 -m64 %{TACC_OPT} -ipo" EXTRA_FLAGS="-I${TI} -L${TL} -Wl,-rpath,${TL}" prefix=%{INSTALL_DIR} DESTDIR=${RPM_BUILD_ROOT} -j1 install

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

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN

for the location of the %{pkg_base_name} distribution.

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing, NGS")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")

%if "%{PLATFORM}" == "stampede2"
always_load("zlib")
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
