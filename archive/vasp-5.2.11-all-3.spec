Summary: VASP

Name:      vasp
Version:   5.2.11
Release:   3
License: VASP
Vendor:    Vienna University
Group:     Application
Source:    vasp.5.2.11_all_TACC.tar.gz
Packager:  TACC - hliu@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot


%define version_unit 5211

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%package -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: VAMP/VASP is a package for performing ab-initio quantum-mechanical molecular dynamics (MD) using pseudopotentials and a plane wave basis set.
Group:  Application
%description -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}


%description


%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%prep

#%setup -n %{name}.%{version}
%setup -n vasp.5.2.11_all_TACC


%build

%include compiler-load.inc
%include mpi-load.inc


module load fftw3
module load mkl
module load scalapack

cd vasp.5.lib
make 

cd ../vasp.5.2

make -f Makefile_Ranger_VASP5211_std_hliu clean
make -f Makefile_Ranger_VASP5211_std_hliu
mv vasp vasp_std

make -f Makefile_Ranger_VASP5211_gamma_hliu clean
make -f Makefile_Ranger_VASP5211_gamma_hliu
mv vasp vasp_gamma


make -f Makefile_Ranger_VASP5211_ncl_hliu clean
make -f Makefile_Ranger_VASP5211_ncl_hliu
mv vasp vasp_ncl

cd ../vasp.5.2.vtst

make -f Makefile_Ranger_VASP5211_std_vtst_hliu clean
make -f Makefile_Ranger_VASP5211_std_vtst_hliu
mv vasp vasp_std_vtst

make -f Makefile_Ranger_VASP5211_gamma_vtst_hliu clean
make -f Makefile_Ranger_VASP5211_gamma_vtst_hliu
mv vasp vasp_gamma_vtst


make -f Makefile_Ranger_VASP5211_ncl_vtst_hliu clean
make -f Makefile_Ranger_VASP5211_ncl_vtst_hliu
mv vasp vasp_ncl_vtst

%install

rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/*
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

cd vasp.5.2
cp vasp_std $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_gamma $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_ncl $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cd ../vasp.5.2.vtst
cp vasp_std_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_gamma_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_ncl_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cd ..
cp -r vtstscripts $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.


rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_message = [[
The TACC VASP module appends the path to the vasp executables
to the PATH environment variable.  Also TACC_VASP_DIR, and 
TACC_VASP_BIN are set to VASP home and bin directories.
 
Users have to show their licenses and be confirmed by 
VASP team that they are registered users under that licenses
Scan a copy the license and send to hliu@tacc.utexas.edu
 
The VASP executables are 
vasp_std: compiled with pre processing flag: -DNGZhalf 
vasp_gamma: compiled with pre processing flag: -DNGZhalf -DwNGZhalf 
vasp_ncl: compiled without above pre processing flags 
vasp_std_vtst: vasp_std with TST 
vasp_gamma_vtst: vasp_gamma with TST 
vasp_ncl_vtst: vasp_ncl with TST 
vtstscripts/: utility scripts of TST 
 

Version 5.2.11
]]


local err_message = [[
You do not access to VASP.5.2.11!


Users have to show their licenses and be confirmed by 
VASP team that they are registered users under that licenses
Scan a copy the license and send to hliu@tacc.utexas.edu
]]

local group = "G-802400"
local grps  = capture("groups")
local found = false
for g in grps:split("[ \n]") do
   if (g == group)  then
      found = true
      break
   end
end

whatis("Name: VASP")
whatis("Version: 5.2.11")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics")
whatis("URL:http://cms.mpi.univie.ac.at/vasp/")
whatis("Description: Vienna Ab-Initio Simulation Package")

help(help_message)

if (found) then
  local vasp_dir="%{INSTALL_DIR}"
  setenv("TACC_VASP_DIR",vasp_dir)
  setenv("TACC_VASP_BIN",pathJoin(vasp_dir,"bin"))
  append_path("PATH",pathJoin(vasp_dir,"bin"))

else
   LmodError(err_message,"\n")
end

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for VASP %version
##

set     ModulesVersion      "%{version}"
EOF


#############################################################################

%files -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(750,root,G-802400)
%{INSTALL_DIR}
%defattr(755,root,install)
%{MODULE_DIR}

%post

%clean
#rm -rf $RPM_BUILD_ROOT

