#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME gaussian
Version:   09rE.01
Release:   1
License:   Gaussian
Group:     Applications/Life Sciences
Source:    A64-114X.tgz
Packager:  jfonner@tacc.utexas.edu
Summary:   Gaussian 09 quantum mechanics package


## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}GAUSSIAN


#%include compiler-defines.inc
#%include mpi-defines.inc

%define PNAME gaussian
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}

%description
Gaussian 09 is the latest in the Gaussian series of programs. It provides
state-of-the-art capabilities for electronic structure modeling. Gaussian 09 is
licensed for a wide variety of computer systems.

%prep
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n g09

%build

#%include compiler-load.inc
#%include mpi-load.inc

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
#mkdir -p %{INSTALL_DIR}
#tacctmpfs -m %{INSTALL_DIR}

pwd
./bsd/install
cp -rp ../g09 $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/g09/tests

#tacctmpfs -u %{INSTALL_DIR}


#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_message = [[
The use of Gaussian is restricted to TACC users who have formally agreed to
the associated Confidentiality Agreement document supplied by TACC. For
questions about access, please email jfonner@tacc.utexas.edu.

The %{PNAME} module file defines %{MODULE_VAR}_DIR in the environment, sets
g09root to that directory and sets GAUSS_SCRDIR to /tmp/, which is local
scratch space on all the nodes. If you think you want to store temporary files
in your personal SCRATCH directory, set the GAUSS_SCRDIR in your job submission
script or local environment.

Linda is not included in the module, so Gaussian should be set to use the max
number of cores on a single node, which is set by the NProcShared variable in
your input file.  Gaussian does not use ibrun.  Your command will look
something like this:

g09 < input > output

Gaussian online documentation is here:
http://www.gaussian.com/g_tech/g_ur/g09help.htm

Version %{version}
]]

local err_message = [[
You do not have access to Gaussian 09.

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
whatis("Version: %{version} rev D.01")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Biology, Quantum Mechanics, QM")
whatis("URL: http://www.gaussian.com/")
whatis("Description: Gaussian 09 quantum chemistry package")

help(help_message)

if (found) then
append_path( "PATH",              "%{INSTALL_DIR}/g09")
   setenv (  "g09root",           "%{INSTALL_DIR}/")
   setenv (  "GAUSS_SCRDIR",      "/tmp/")
   setenv (  "GAUSS_EXEDIR",      "%{INSTALL_DIR}/g09")
   setenv (  "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
   setenv (  "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/g09")

else
   LmodError(err_message,"\n")
end

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
%defattr(750,root,G-813687)
%{INSTALL_DIR}
%defattr(755,root,install)
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT

