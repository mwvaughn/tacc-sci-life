## LSC RPM Overview

The Life Sciences Computing group at the Texas Advanced Computing Center (TACC) uses this repository to build modules for TACC's supercomputing systems

Older modules are in the "archive" directory.  The "scripts" directory contains helpful utility scripts.  The "include" directory contains system specific information that gets loaded during the RPM build process. SPEC files follow a specific naming convention to keep track of the version and revision information.  In general, new revisions are made because the previous version of the SPEC file contained an error (or in the case of Amber, the app updates itself with bugfixes as part of the build process).  The naming convention follows this pattern:

`<application name>-<major version>.<minor version>.<patch>-<spec revision number>.spec`

## Packaging Environment

Building RPMs requires a specific directory structure and system specific include files. To build RPMs for Stampede2, please use our environment, which has been adapted from the work of [TACC HPC](https://github.com/TACC/hpc_spec/tree/knl2/). We recommend that you keep the packaging environment on `$STOCKYARD` so it is accessible from all systems. Begin by creating an `rpmbuild` folder.

```
$ cd $STOCKYARD && mkdir rpmbuild && cd rpmbuild
```

This is where the entire packaging environment will live. Now checkout our rpm SPEC repsoitory, which contains spec files, include files, and helper scripts.

```
$ git clone https://github.com/TACC/lifesci_spec.git SPECS
Cloning into 'SPECS'...
remote: Counting objects: 1568, done.
remote: Total 1568 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (1568/1568), 5.78 MiB | 3.61 MiB/s, done.
Resolving deltas: 100% (730/730), done.
```

Enter the `SPECS` directory and checkout the `separate-rpms` branch for building RPMs on Stampede2.

```
$ cd SPECS
$ git checkout separate-rpms
```

Now that you are on the correct development branch, you just need to build your directory tree for building RPMs.

```
$ ./scripts/buildDirectories.sh
An rpmbuild directory already exists here:
/work/12345/user/rpmbuild

Would you like to have the directory tree under this existing directory? (y/n) [n]
y
Creating rpmbuild heirarchy in the /work/12345/user/rpmbuild directory.
```

Done! Notice that there is a single `SOURCE` diretory that is linked to every system folder in the tree. This enables you to download a source tarball once and use it everywhere.

## Building a module

In this section, we will be building the zlib  module from scratch, and we will cover all sections of the `example.spec` template that you need to modify to create a functional package. If you are simply looking for a "good" example, please refer to the `zlib-1.2.8-1.spec` file.

### Downloading sources

We will be building zlib version 1.2.8, so lets grab that from their [release page](http://zlib.net).

```
$ cd ../SOURCES
$ wget http://zlib.net/fossils/zlib-1.2.8.tar.gz
$ cd ../SPECS
```

### Writing the spec file

Lets start by modifying the `example.spec` file to build the zlib RPM.

> If your application does not use any compiler specific libraries, you can use `example-no-compiler-deps.spec`

```
$ cp example.spec zlib-1.2.8-1.spec
```

Open new spec file in the text editor of your choice and make the following changes.
```shell
example.spec                                                    zlib-1.2.8-1.spec
==============================================================  ==============================================================

#								#
# Name							      |	# Greg Zynda
# 2017-08-01							# 2017-08-01
#								#
# Important Build-Time Environment Variables (see name-define	# Important Build-Time Environment Variables (see name-define
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM		# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM	# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#								#
# Important Install-Time Environment Variables (see post-defi	# Important Install-Time Environment Variables (see post-defi
# RPM_DBPATH      -> Path To Non-Standard RPM Database Locati	# RPM_DBPATH      -> Path To Non-Standard RPM Database Locati
#								#
# Typical Command-Line Example:					# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec					# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64						# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_6	# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_6
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x8	# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x8
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64	# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

%define shortsummary This is a short summary		      |	%define shortsummary A Massively Spiffy Yet Delicately Unobtrusive Compression Library
Summary: %{shortsummary}					Summary: %{shortsummary}

# Give the package a base name					# Give the package a base name
%define pkg_base_name example				      |	%define pkg_base_name zlib

# Create some macros (spec file variables)			# Create some macros (spec file variables)
%define major_version 1						%define major_version 1
%define minor_version 1					      |	%define minor_version 2
%define patch_version 1					      |	%define patch_version 8

%define pkg_version %{major_version}.%{minor_version}.%{patch	%define pkg_version %{major_version}.%{minor_version}.%{patch

### Toggle On/Off ###						### Toggle On/Off ###
%include ./include/system-defines.inc				%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/name-defines.inc			%include ./include/%{PLATFORM}/name-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc                  	%include ./include/%{PLATFORM}/rpm-dir.inc                  
%include ./include/%{PLATFORM}/compiler-defines.inc		%include ./include/%{PLATFORM}/compiler-defines.inc
%include ./include/%{PLATFORM}/mpi-defines.inc		      |	#%include ./include/%{PLATFORM}/mpi-defines.inc
########################################			########################################
############ Do Not Remove #############			############ Do Not Remove #############
########################################			########################################

############ Do Not Change #############			############ Do Not Change #############
Name:      %{pkg_name}						Name:      %{pkg_name}
Version:   %{pkg_version}					Version:   %{pkg_version}
########################################			########################################

Release:   1							Release:   1
License:   BSD							License:   BSD
Group:     Applications/Life Sciences			      |	Group:     Libraries
URL:       https://github.com/TACC/lifesci_spec		      |	URL:       http://zlib.net
Packager:  TACC - email@tacc.utexas.edu			      |	Packager:  TACC - gzynda@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz		Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode					# Turn off debug package mode
%define debug_package %{nil}					%define debug_package %{nil}
%define dbg           %{nil}					%define dbg           %{nil}


%package %{PACKAGE}						%package %{PACKAGE}
Summary: %{shortsummary}					Summary: %{shortsummary}
Group:   Applications/Life Sciences			      |	Group:   Libraries
%description package						%description package
%{name}: %{shortsummary}					%{name}: %{shortsummary}

%package %{MODULEFILE}						%package %{MODULEFILE}
Summary: The modulefile RPM					Summary: The modulefile RPM
Group:   Lmod/Modulefiles					Group:   Lmod/Modulefiles
%description modulefile						%description modulefile
Module file for %{name}						Module file for %{name}

%description							%description
%{name}: %{shortsummary}					%{name}: %{shortsummary}

#---------------------------------------			#---------------------------------------
%prep								%prep
#---------------------------------------			#---------------------------------------

#------------------------					#------------------------
%if %{?BUILD_PACKAGE}						%if %{?BUILD_PACKAGE}
#------------------------					#------------------------
  # Delete the package installation directory.			  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}				  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------					#-----------------------
%endif # BUILD_PACKAGE |					%endif # BUILD_PACKAGE |
#-----------------------					#-----------------------

#---------------------------					#---------------------------
%if %{?BUILD_MODULEFILE}					%if %{?BUILD_MODULEFILE}
#---------------------------					#---------------------------
  #Delete the module installation directory.			  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}				  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------					#--------------------------
%endif # BUILD_MODULEFILE |					%endif # BUILD_MODULEFILE |
#--------------------------					#--------------------------

# Comment this out if pulling from git				# Comment this out if pulling from git
%setup -n %{pkg_base_name}-%{pkg_version}			%setup -n %{pkg_base_name}-%{pkg_version}

#---------------------------------------			#---------------------------------------
%build								%build
#---------------------------------------			#---------------------------------------


#---------------------------------------			#---------------------------------------
%install							%install
#---------------------------------------			#---------------------------------------

# Setup modules							# Setup modules
%include ./include/%{PLATFORM}/system-load.inc			%include ./include/%{PLATFORM}/system-load.inc
##################################				##################################
# If using build_rpm						# If using build_rpm
##################################				##################################
%include ./include/%{PLATFORM}/compiler-load.inc		%include ./include/%{PLATFORM}/compiler-load.inc
%include ./include/%{PLATFORM}/mpi-load.inc		      |	#%include ./include/%{PLATFORM}/mpi-load.inc
%include ./include/%{PLATFORM}/mpi-env-vars.inc		      |	#%include ./include/%{PLATFORM}/mpi-env-vars.inc
##################################				##################################
# Manually load modules						# Manually load modules
##################################				##################################
# module load							# module load
##################################				##################################

echo "Building the package?:    %{BUILD_PACKAGE}"		echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"		echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------					#------------------------
%if %{?BUILD_PACKAGE}						%if %{?BUILD_PACKAGE}
#------------------------					#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}			  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  								  
  #######################################			  #######################################
  ##### Create TACC Canary Files ########			  ##### Create TACC Canary Files ########
  #######################################			  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary	  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################			  #######################################
  ########### Do Not Remove #############			  ########### Do Not Remove #############
  #######################################			  #######################################

  #========================================			  #========================================
  # Insert Build/Install Instructions Here			  # Insert Build/Install Instructions Here
  #========================================			  #========================================

							      >	# Source IPP
							      >	tar -xzf $IPPROOT/examples/components_and_examples_lin_ps.tgz ./components/interfaces/ipp_zlib/zlib-1.2.8.path
							      >	source /opt/intel/compilers_and_libraries_2017.4.196/linux/ipp/bin/ippvars.sh intel64
							      >
							      >	# Patch zlib
							      >	patch -p1 < components/interfaces/ipp_zlib/zlib-%{version}.patch
							      >
							      >	# Compile zlib
							      >	source /opt/intel/compilers_and_libraries_2017.4.196/linux/bin/compilervars.sh intel64
							      >	export CFLAGS="-O3 %{TACC_OPT} -fPIC -m64 -DWITH_IPP -I$IPPROOT/include"
							      >	export LDFLAGS="$IPPROOT/lib/intel64/libippdc.a $IPPROOT/lib/intel64/libipps.a $IPPROOT/lib/intel64/libippcore.a"
./configure --prefix=%{INSTALL_DIR}				./configure --prefix=%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT -j 4			      |	make shared
make DESTDIR=$RPM_BUILD_ROOT -j 4 install		      |	make DESTDIR=${RPM_BUILD_ROOT} install

#-----------------------  					#-----------------------  
%endif # BUILD_PACKAGE |					%endif # BUILD_PACKAGE |
#-----------------------					#-----------------------


#---------------------------					#---------------------------
%if %{?BUILD_MODULEFILE}					%if %{?BUILD_MODULEFILE}
#---------------------------					#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}			  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  								  
  #######################################			  #######################################
  ##### Create TACC Canary Files ########			  ##### Create TACC Canary Files ########
  #######################################			  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary	  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################			  #######################################
  ########### Do Not Remove #############			  ########### Do Not Remove #############
  #######################################			  #######################################
  								  
# Write out the modulefile associated with the application	# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EO	cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EO
local help_message = [[						local help_message = [[
The %{pkg_base_name} module file defines the following enviro	The %{pkg_base_name} module file defines the following environment va

 - %{MODULE_VAR}_DIR						 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN					      <
 - %{MODULE_VAR}_LIB						 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_INC						 - %{MODULE_VAR}_INC

for the location of the %{pkg_base_name} distribution.		for the location of the %{pkg_base_name} distribution.

							      >	For static linking on Linux* OS, 
							      >
							      >	  gcc -O3 -o zpipe_ipp.out zpipe.c -I$IPPROOT/include -I$%{MO
							      >
							      >	For static linking on Linux* OS, 
							      >
							      >	  gcc -O3 -o zpipe_ipp.out zpipe.c -I$%{MODULE_VAR}_INC -L$%{
							      >
Documentation: %{url}						Documentation: %{url}

Version %{version}						Version %{version}
]]								]]

help(help_message,"\n")						help(help_message,"\n")

whatis("Name: %{name}")						whatis("Name: %{name}")
whatis("Version: %{version}")					whatis("Version: %{version}")
whatis("Category: computational biology, genomics")	      |	whatis("Category: applications, compression")
whatis("Keywords: Biology, Genomics")			      |	whatis("Keywords: compressino, deflate")
whatis("Description: %{shortsummary}")				whatis("Description: %{shortsummary}")
whatis("URL: %{url}")						whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")	      <
prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")		prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")	prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")		setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")	      <
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")		setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")	setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")
EOF								EOF
  								  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'E	cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'E
#%Module3.1.1################################################	#%Module3.1.1################################################
##								##
## version file for %{BASENAME}%{version}			## version file for %{BASENAME}%{version}
##								##

set     ModulesVersion      "%{version}"			set     ModulesVersion      "%{version}"
EOF								EOF
  								  
  # Check the syntax of the generated lua modulefile		  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/scripts/checkModuleSyntax $RPM_BUILD_ROOT/%{MOD	  %{SPEC_DIR}/scripts/checkModuleSyntax $RPM_BUILD_ROOT/%{MOD

#--------------------------					#--------------------------
%endif # BUILD_MODULEFILE |					%endif # BUILD_MODULEFILE |
#--------------------------					#--------------------------


#------------------------					#------------------------
%if %{?BUILD_PACKAGE}						%if %{?BUILD_PACKAGE}
%files package							%files package
#------------------------					#------------------------

  %defattr(-,root,install,)					  %defattr(-,root,install,)
  # RPM package contains files within these directories		  # RPM package contains files within these directories
  %{INSTALL_DIR}						  %{INSTALL_DIR}

#-----------------------					#-----------------------
%endif # BUILD_PACKAGE |					%endif # BUILD_PACKAGE |
#-----------------------					#-----------------------
#---------------------------					#---------------------------
%if %{?BUILD_MODULEFILE}					%if %{?BUILD_MODULEFILE}
%files modulefile 						%files modulefile 
#---------------------------					#---------------------------

  %defattr(-,root,install,)					  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories	  # RPM modulefile contains files within these directories
  %{MODULE_DIR}							  %{MODULE_DIR}

#--------------------------					#--------------------------
%endif # BUILD_MODULEFILE |					%endif # BUILD_MODULEFILE |
#--------------------------					#--------------------------


########################################			########################################
## Fix Modulefile During Post Install ##			## Fix Modulefile During Post Install ##
########################################			########################################
%post %{PACKAGE}						%post %{PACKAGE}
export PACKAGE_POST=1						export PACKAGE_POST=1
%include ./include/%{PLATFORM}/post-defines.inc			%include ./include/%{PLATFORM}/post-defines.inc
%post %{MODULEFILE}						%post %{MODULEFILE}
export MODULEFILE_POST=1					export MODULEFILE_POST=1
%include ./include/%{PLATFORM}/post-defines.inc			%include ./include/%{PLATFORM}/post-defines.inc
%preun %{PACKAGE}						%preun %{PACKAGE}
export PACKAGE_PREUN=1						export PACKAGE_PREUN=1
%include ./include/%{PLATFORM}/post-defines.inc			%include ./include/%{PLATFORM}/post-defines.inc
########################################			########################################
############ Do Not Remove #############			############ Do Not Remove #############
########################################			########################################

#---------------------------------------			#---------------------------------------
%clean								%clean
#---------------------------------------			#---------------------------------------
rm -rf $RPM_BUILD_ROOT						rm -rf $RPM_BUILD_ROOT
```
### Compiling the RPMs

To take advantage of `compiler-defines.inc`, we need to use the `build_rpm.sh` script and also specify which compiler to use.
While this will restrict your module to only loading with a specific compiler environment, it also means much less work writing system-specific compiler arguments. 
Since we will be compiling on Stampede2, we should use the latest version of the Intel compiler.

```
$ build_rpm.sh -i17 zlib-1.2.8-1.spec
```

To help decide which directories you want to include in your modulefile, inspect your built RPM with

```
rpm -qlp ../stampede2/RPMS/x86_64/tacc-zlib-1.2.8-package-1.2.8-1.x86_64.rpm
```

and match or delete the

```
prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")
```

variables as necessary.

If all goes well, you should be left with two RPMS:

- The RPM that contains all LMOD module files
  - tacc-zlib-1.2.8-modulefile-1.2.8-1.x86_64.rpm
- The RPM that contains all program files
  - tacc-zlib-1.2.8-package-1.2.8-1.x86_64.rpm

## Testing the RPM

Now that you have functional RPMs, you can test them by installing them locally using the `scripts/myRpmInstall` script. Use it as follows:

```
scripts/myRpmInstall <install directory> <module RPM> <package RPM>
```

We can install our zlib RPMs as follows

```
$ mkdir -p $WORK/public/apps
$ scripts/myRpmInstall $WORK/public/apps ../stampede2/RPMS/x86_64/tacc-zlib-1.2.8-modulefile-1.2.8-1.x86_64.rpm ../stampede2/RPMS/x86_64/tacc-zlib-1.2.8-package-1.2.8-1.x86_64.rpm
Installing RPMs
WARN: Modulefile RPM was installed while using non-standard RPM database location.
WARN: Package RPM is being installed while using non-standard RPM database location.
WARN: You're off the map! Good luck, friend.
INSTALLED! - ignore the warnings
Checking the $MODULEPATH variable.
looks like the $MODULEPATH environment variable needs updating.
Check the README.md file if you aren't sure how to do that.
```

The warnings look a little scary, but this is a successful installation. Update your module path to include the new location and then load the zlib module.

```
staff.stampede2(102)$ ml use $WORK/public/apps/intel17/modulefiles
staff.stampede2(103)$ ml zlib
staff.stampede2(104)$ ml show zlib
--------------------------------------------------------------------------------------------------------------
   /work/03076/gzynda/stampede2/public/apps/intel17/modulefiles/zlib/1.2.8.lua:
--------------------------------------------------------------------------------------------------------------
help([[The zlib module file defines the following environment variables:

 - TACC_ZLIB_DIR
 - TACC_ZLIB_LIB
 - TACC_ZLIB_INC

for the location of the zlib distribution.

For static linking on Linux* OS,

  gcc -O3 -o zpipe_ipp.out zpipe.c -I$TACC_ZLIB_INC $TACC_ZLIB_LIB/libz.a

For static linking on Linux* OS,

  gcc -O3 -o zpipe_ipp.out zpipe.c -I$TACC_ZLIB_INC -L$TACC_ZLIB_LIB -lz

Documentation: http://zlib.net

Version 1.2.8
]], [[
]])
whatis("Name: tacc-zlib-1.2.8-intel17")
whatis("Version: 1.2.8")
whatis("Category: applications, compression")
whatis("Keywords: compressino, deflate")
whatis("Description: A Massively Spiffy Yet Delicately Unobtrusive Compression Library")
whatis("URL: http://zlib.net")
prepend_path("PATH","/work/03076/gzynda/stampede2/public/apps/intel17/zlib/1.2.8/bin")
prepend_path("LD_LIBRARY_PATH","/work/03076/gzynda/stampede2/public/apps/intel17/zlib/1.2.8/lib")
prepend_path("MANPATH","/work/03076/gzynda/stampede2/public/apps/intel17/zlib/1.2.8/share/man")
setenv("TACC_ZLIB_DIR","/work/03076/gzynda/stampede2/public/apps/intel17/zlib/1.2.8")
setenv("TACC_ZLIB_BIN","/work/03076/gzynda/stampede2/public/apps/intel17/zlib/1.2.8/bin")
setenv("TACC_ZLIB_LIB","/work/03076/gzynda/stampede2/public/apps/intel17/zlib/1.2.8/lib")
setenv("TACC_ZLIB_INC","/work/03076/gzynda/stampede2/public/apps/intel17/zlib/1.2.8/include")
```

If everything goes well with your tests, you can use the `moveRpm` helper script to deposit the RPMs in their appropriate location.

```
staff.stampede2(105)$ scripts/moveRpm ../stampede2/RPMS/x86_64/tacc-zlib-1.2.8-modulefile-1.2.8-1.x86_64.rpm ../stampede2/RPMS/x86_64/tacc-zlib-1.2.8-package-1.2.8-1.x86_64.rpm

Move:
 - ../stampede2/RPMS/x86_64/tacc-zlib-1.2.8-intel17-modulefile-1.2.8-1.x86_64.rpm
to
 - /admin/build/admin/rpms/stampede2/RPMS/x86_64/?
[Y/n] y

Move:
 - ../stampede2/RPMS/x86_64/tacc-zlib-1.2.8-intel17-package-1.2.8-1.x86_64.rpm
to
 - /admin/build/admin/rpms/stampede2/RPMS/x86_64/?
[Y/n] y

Please request the following for installation:

  rpm -ivh --nodeps --relocate /tmpmod=/opt/apps /admin/build/admin/rpms/stampede2/RPMS/x86_64/tacc-zlib-1.2.8-intel17-modulefile-1.2.8-1.x86_64.rpm
  rpm -ivh --nodeps --relocate /tmprpm=/home1/apps /admin/build/admin/rpms/stampede2/RPMS/x86_64/tacc-zlib-1.2.8-intel17-package-1.2.8-1.x86_64.rpm

```

Done! You can now submit a collab ticket for the RPMs to be installed. After you submit your collab ticket, remember to commit your new spec file back to the repo.

```
git pull origin separate-rpms
git add your-new.spec
git commit -am "Just completed a new spec file"
git push origin separate-rpms
```
