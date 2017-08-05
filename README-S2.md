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

```
$ cp example.spec zlib-1.2.8-1.spec
```

Open new spec file in the text editor of your choice and make the following changes.

<table>
<thead><tr>
	<th>example.spec</th><th>zlib-1.2.8-1.spec</th>
</tr></thead>
<tbody><tr>
<td>
<pre><code>
"#
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

%define shortsummary ""
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name example

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 1
%define patch_version 1

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/name-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
%include ./include/%{PLATFORM}/compiler-defines.inc
%include ./include/%{PLATFORM}/mpi-defines.inc
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
URL:       https://github.com/TACC/lifesci_spec
Packager:  TACC - email@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: %{shortsummary}
Group: Applications/Life Sciences
%description package
%{name}: %{shortsummary}

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Module file for %{name}

%description
%{name}: %{shortsummary}

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

# Comment this out if pulling from git
%setup -n %{pkg_base_name}-%{pkg_version}

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
%include ./include/%{PLATFORM}/mpi-load.inc
%include ./include/%{PLATFORM}/mpi-env-vars.inc
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

./configure --prefix=%{INSTALL_DIR}
make DESTDIR=$RPM_BUILD_ROOT -j 4
make DESTDIR=$RPM_BUILD_ROOT -j 4 install

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
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN
 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_INC

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")
prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")
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
rm -rf $RPM_BUILD_ROOT"
</code></pre>
</td>
<td>
<pre><code>
"  #
| # Greg Zynda
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

| %define shortsummary "A Massively Spiffy Yet Delicately Unobtrusive Compression Library"
  Summary: %{shortsummary}

  # Give the package a base name
| %define pkg_base_name zlib

  # Create some macros (spec file variables)
  %define major_version 1
| %define minor_version 2
| %define patch_version 8

  %define pkg_version %{major_version}.%{minor_version}.%{patch_version}

  ### Toggle On/Off ###
  %include ./include/system-defines.inc
  %include ./include/%{PLATFORM}/name-defines.inc
  %include ./include/%{PLATFORM}/rpm-dir.inc
  %include ./include/%{PLATFORM}/compiler-defines.inc
| #%include ./include/%{PLATFORM}/mpi-defines.inc
  ########################################
  ############ Do Not Remove #############
  ########################################

  ############ Do Not Change #############
  Name:      %{pkg_name}
  Version:   %{pkg_version}
  ########################################

  Release:   1
  License:   BSD
| Group:     Libraries
| URL:       http://zlib.net
| Packager:  TACC - gzynda@tacc.utexas.edu
  Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

  # Turn off debug package mode
  %define debug_package %{nil}
  %define dbg           %{nil}


  %package %{PACKAGE}
  Summary: %{shortsummary}
| Group:     Libraries
  %description package
  %{name}: %{shortsummary}

  %package %{MODULEFILE}
  Summary: The modulefile RPM
  Group: Lmod/Modulefiles
  %description modulefile
  Module file for %{name}

  %description
  %{name}: %{shortsummary}

  #---------------------------------------
  %prep
  #---------------------------------------

  #------------------------
  %if %{?BUILD_PACKAGE}
  #------------------------
    # Delete the package installation directory.
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

  # Comment this out if pulling from git
  %setup -n %{pkg_base_name}-%{pkg_version}

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
| #%include ./include/%{PLATFORM}/mpi-load.inc
| #%include ./include/%{PLATFORM}/mpi-env-vars.inc
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

>  # Source IPP
>  tar -xzf $IPPROOT/examples/components_and_examples_lin_ps.tgz ./components/interfaces/ipp_zlib/zlib-1.2.8.patch
>  source /opt/intel/compilers_and_libraries_2017.4.196/linux/ipp/bin/ippvars.sh intel64
>
>  # Patch zlib
>  patch -p1 < components/interfaces/ipp_zlib/zlib-%{version}.patch
>
>  # Compile zlib
>  source /opt/intel/compilers_and_libraries_2017.4.196/linux/bin/compilervars.sh intel64
>  export CFLAGS="-O3 %{TACC_OPT} -fPIC -m64 -DWITH_IPP -I$IPPROOT/include"
>  export LDFLAGS="$IPPROOT/lib/intel64/libippdc.a $IPPROOT/lib/intel64/libipps.a $IPPROOT/lib/intel64/libippcore.a"
>  ./configure --prefix=%{INSTALL_DIR}
>  make shared
>  make DESTDIR=${RPM_BUILD_ROOT} install

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
  The %{PNAME} module file defines the following environment variables:

   - %{MODULE_VAR}_DIR
<
   - %{MODULE_VAR}_LIB
   - %{MODULE_VAR}_INC

  for the location of the %{PNAME} distribution.

>  For static linking on Linux* OS,
>
>    gcc -O3 -o zpipe_ipp.out zpipe.c -I$IPPROOT/include -I$%{MODULE_VAR}_INC $%{MODULE_VAR}_LIB/libz.a $IPPROOT/lib/intel64/libipp{dc,s,core}.a
>
>  For static linking on Linux* OS,
>
>    gcc -O3 -o zpipe_ipp.out zpipe.c -I$%{MODULE_VAR}_INC -L$%{MODULE_VAR}_LIB -lz
>

  Documentation: %{url}

  Version %{version}
  ]]

  help(help_message,"\n")

  whatis("Name: %{name}")
  whatis("Version: %{version}")
| whatis("Category: applications, compression")
| whatis("Keywords: compressino, deflate")
  whatis("Description: %{shortsummary}")
  whatis("URL: %{url}")

<
  prepend_path("LD_LIBRARY_PATH",	"%{INSTALL_DIR}/lib")
  prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

  setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
<
  setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib")
  setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")
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
  rm -rf $RPM_BUILD_ROOT"
</code></pre>
</td>
</tr></tbody>
</table>

### Compiling the RPMs
