#
# $Id: nwchem-511.spec,2009/06/22 hliu $
#

Summary: NWChem is a computational chemistry package that is designed to run on high-performance parallel supercomputers. 

###
Name:      nwchem
Version:   6.0
Release:   2
License: ECL
Vendor:    EMSL/PNL
Group:     Applications/Chemistry
Source:    Nwchem-6.0.tar.gz
Packager:  hliu@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

URL: http://www.emsl.pnl.gov/docs/nwchem
Distribution: RedHat Linux


%define version_unit 60
%include rpm-dir.inc
%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%description
NWChem is a computational chemistry package that is designed to run on
high-performance parallel supercomputers as well as conventional workstation
clusters. It aims to be scalable both in its ability to treat large problems
efficiently, and in its usage of available parallel computing resources.
NWChem has been developed by the Molecular Sciences Software group of the
Theory, Modeling & Simulation program of the Environmental Molecular Sciences
Laboratory (EMSL) at the Pacific Northwest National Laboratory (PNNL). Most
of the implementation has been funded by the EMSL Construction Project.


%package     -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}-dev
Summary: Suite %{name}-%{version}  for login nodes.
Group:   Applications/Chemistry
%description -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}-dev
QA suite for %{name}-%{version}

%package     -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: Suite %{name}-%{version} for compute nodes.
Group:   Applications/Chemistry
%description -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
Less QA suite for %{name}-%{version}.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup 


%build

%include compiler-load.inc
%include mpi-load.inc

export NWCHEM_TOP=$RPM_BUILD_DIR/%{name}-%{version}/
export NWCHEM_MODULES=all
export NWCHEM_TARGET=LINUX64

export TARGET=LINUX64
export ARMCI_NETWORK=OPENIB
export IB_HOME=/opt/ofed
export IB_INCLUDE=$IB_HOME/include
export IB_LIB=$IB_HOME/lib64
export IB_LIB_NAME="-libverbs -libumad -lpthread"

export MA_USE_ARMCI_MEM=1
export LARGE_FILES=TRUE
export LIB_DEFINES='-DDFLT_TOT_MEM=16777216'

export MPI_HOME=$MPICH_HOME
export MPI_LIB=$MPI_HOME/lib
export MPI_INCLUDE=$MPI_HOME/include
export LIBMPI="-lmpich"
export USE_MPI=y


cd $NWCHEM_TOP/src
make realclean
make nwchem_config 
make FC=ifort CC=icc 

%install
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
mkdir    $RPM_BUILD_ROOT/%{INSTALL_DIR}/data


###
### Installation of basis sets and libraries
###
cp -r $RPM_BUILD_DIR/%{name}-%{version}/src/basis/libraries             $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
cp -r $RPM_BUILD_DIR/%{name}-%{version}/src/data                        $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r $RPM_BUILD_DIR/%{name}-%{version}/src/nwpw/libraryps/pspw_default $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
cp -r $RPM_BUILD_DIR/%{name}-%{version}/src/nwpw/libraryps/paw_default  $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
cp -r $RPM_BUILD_DIR/%{name}-%{version}/src/nwpw/libraryps/TM           $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
cp -r $RPM_BUILD_DIR/%{name}-%{version}/src/nwpw/libraryps/HGH_LDA      $RPM_BUILD_ROOT/%{INSTALL_DIR}/data

###
### Not sure if this is necessary anymore
###
cat >   $RPM_BUILD_ROOT/%{INSTALL_DIR}/data/default.nwchemrc << 'EOF'
   ffield amber
   amber_1  %{INSTALL_DIR}/data/amber_s/
   amber_2  %{INSTALL_DIR}/data/amber_q/
   amber_3  %{INSTALL_DIR}/amber_x/
   amber_4  %{INSTALL_DIR}/data/amber_u/
   spce     %{INSTALL_DIR}/data/solvents/spce.rst
   charmm_s %{INSTALL_DIR}/data/charmm_s/
   charmm_x %{INSTALL_DIR}/data/charmm_x/
EOF

###
### Install QA testing suite 
###
mkdir -p                                                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/QA
#cp -r $RPM_BUILD_DIR/%{name}-%{version}/examples           $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r $RPM_BUILD_DIR/%{name}-%{version}/QA/tests           $RPM_BUILD_ROOT/%{INSTALL_DIR}/QA
cp    $RPM_BUILD_DIR/%{name}-%{version}/bin/LINUX64/nwchem $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
chmod -Rf u+rwX,g+rwX,o=rX                           $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## Module section
##
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[

The default envs of the installed NWCHEM 
NWCHEM_TOP  %{INSTALL_DIR}/
NWCHEM_NWPW_LIBRARY  %{INSTALL_DIR}/data/
NWCHEM_BASIS_LIBRARY %{INSTALL_DIR}/data/libraries

To run NWChem, please include the following lines in
your job script, using the appropriate input file name:
module load nwchem
ibrun nwchem input.nw

You need to reset envs BY YOUR OWN if your calculation needs configuration  
and input beyond the above defaults

Version %{version}
]]

help(help_message,"\n")

whatis "Version: %{version}"
whatis "Category: application, chemistry"
whatis "Keywords: Biology, Chemistry, Quantum Mechanics, Molecular Dynamics, Application"
whatis "URL: http://www.emsl.pnl.gov/docs/nwchem/nwchem.html"
whatis "Description: General computational chemistry package (quantum chemistry and molecular dynamics)"

local nwchem_dir="%{INSTALL_DIR}"

setenv("TACC_NWCHEM_DIR",nwchem_dir)
setenv("TACC_NWCHEM_BIN",pathJoin(nwchem_dir,"bin"))
setenv("NWCHEM_NWPW_LIBRARY",pathJoin(nwchem_dir,"data"))
setenv("NWCHEM_BASIS_LIBRARY",pathJoin(nwchem_dir,"data/libraries"))
append_path("PATH",pathJoin(nwchem_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for %{name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF


%files -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}/bin
%{INSTALL_DIR}/data
%{MODULE_DIR}

%files -n %{name}%{version_unit}-%{comp_fam_ver}-%{mpi_fam_ver}-dev
%defattr(-,root,install)
%{INSTALL_DIR}/QA
#%{INSTALL_DIR}/examples

%post
%clean

# $Log: $
