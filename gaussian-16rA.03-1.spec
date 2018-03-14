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

# INITIAL DEFINITIONS
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

%define shortsummary Gaussian 16 quantum mechanics package
Summary: %{shortsummary}
%define pkg_base_name gaussian
%define pkg_version 16rA.03

%define MODULE_VAR  %{MODULE_VAR_PREFIX}GAUSSIAN
%define PNAME gaussian
Release:   1
License:   Gaussian
Group:     Applications/Life Sciences
Source:    E6B-132X.tbz
Packager:  jfonner@tacc.utexas.edu
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc

## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc

## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

## directory and name definitions for relocatable RPMs
%include ./include/%{PLATFORM}/name-defines.inc

Name:      %{pkg_name}
Version:   %{pkg_version}

# Turn off debug package mode
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

%if %{?BUILD_PACKAGE}
    # Delete the package installation directory.
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# -n <subdirectory name inside the Source tarball>
%setup -n g16
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
%endif

%if %{?BUILD_MODULEFILE}
    #Delete the module installation directory.
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif
#---------------------------------------

%build

#---------------------------------------
%install

%include ./include/%{PLATFORM}/system-load.inc
#%include ./include/%{PLATFORM}/compiler-load.inc
#%include ./include/%{PLATFORM}/mpi-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"


%if %{?BUILD_PACKAGE}

    # Create TACC Canary File. DO NOT REMOVE NEXT LINE
    mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
    touch $RPM_BUILD_ROOT%{INSTALL_DIR}/.tacc_install_canary

    # Insert Build/Install Instructions Here
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


    ./bsd/install
    cp -rp ../g16 $RPM_BUILD_ROOT%{INSTALL_DIR}
    rm -rf $RPM_BUILD_ROOT%{INSTALL_DIR}/g16/tests

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

%endif # BUILD_PACKAGE


%if %{?BUILD_MODULEFILE}

    rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
    mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
    # Create TACC Canary File. DO NOT REMOVE NEXT LINE
    touch $RPM_BUILD_ROOT%{MODULE_DIR}/.tacc_module_canary

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv    
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_message = [[
The use of Gaussian is restricted to TACC users who have formally agreed to
the associated Usage Agreement document supplied by TACC. For questions about 
access or a copy of the required form, please email jfonner@tacc.utexas.edu.

This compilation of %{PNAME} %{version} is not optimized for the Intel Xeon Phi
processor, but it is compatible.  TACC is provisionally supplying it until a Phi
optimized version becomes available.

The %{PNAME} module file defines %{MODULE_VAR}_DIR in the environment, sets
g19root to that directory and sets GAUSS_SCRDIR to /tmp/, which is local
scratch space on all the nodes. If you think you want to store temporary files
in your personal SCRATCH directory, set the GAUSS_SCRDIR in your job submission
script or local environment.

Linda is not included in the module, so Gaussian should be set to use the max
number of cores on a single node, which is set by the NProcShared variable in
your input file.  Gaussian does not use ibrun.  Your command will look
something like this:

g16 < input > output

Gaussian online documentation is here:
http://gaussian.com/man/

Version %{version}
]]

local err_message = [[
You do not have access to Gaussian 16.

The use of Gaussian is restricted to TACC users who have formally agreed to
the associated Confidentiality Agreement document supplied by TACC. For
questions about access or a copy of the required form, please email
jfonner@tacc.utexas.edu.

]]

local group = "G-813687"
local grps  = capture("groups")
local found = false
local isRoot = tonumber(capture("id -u")) == 0
for g in grps:split("[ \n]") do
    if (g == group or isRoot)  then
        found = true
        break
    end
end

whatis("Name: Gaussian")
whatis("Version: %{version} rev A.03")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Biology, Quantum Mechanics, QM")
whatis("URL: http://www.gaussian.com/")
whatis("Description: Gaussian 16 quantum chemistry package")

help(help_message,"\n")

if (found) then
append_path( "PATH",              "%{INSTALL_DIR}/g16")
    setenv (  "g16root",           "%{INSTALL_DIR}/")
    setenv (  "GAUSS_SCRDIR",      "/tmp/")
    setenv (  "GAUSS_EXEDIR",      "%{INSTALL_DIR}/g16")
    setenv (  "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
    setenv (  "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/g16")

else
    LmodError(err_message,"\n")
end

EOF

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#  Version file.
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

# Check the syntax of the generated lua modulefile
%{SPEC_DIR}/scripts/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%endif # BUILD_MODULEFILE
#---------------------------------------

%if %{?BUILD_PACKAGE}
%files package
%defattr(750,root,G-813687)
# RPM package contains files within these directories
%{INSTALL_DIR}
%endif # BUILD_PACKAGE

%if %{?BUILD_MODULEFILE}
%files modulefile
%defattr(-,root,install,)
# RPM modulefile contains files within these directories
%{MODULE_DIR}
%endif # BUILD_MODULEFILE


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

%clean
rm -rf $RPM_BUILD_ROOT

