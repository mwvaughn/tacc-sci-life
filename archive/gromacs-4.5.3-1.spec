#
# Spec file for gromacs 4.5.3 
#
Summary: gromacs local binary install 
Name: gromacs 
Version: 4.5.3 
Release: 6
License: GPL
Vendor: www.gromacs.org 
Group: Applications/Biology
Source: gromacs-4.5.3.tar.gz 
Packager: bdkimh@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary: gromacs local binary install
Group: Applications/Biology 

%description
%description -n %{name}-%{comp_fam_ver}
GROMACS is a versatile and extremely well optimized package
to perform molecular dynamics computer simulations and
subsequent trajectory analysis. It is developed for
biomolecules like proteins, but the extremely high 
performance means it is used also in several other fields
like polymer chemistry and solid state physics. This
version has the dynamic libs and executables; to hack new
utility programs you also need the headers and static
libs in gromacs-dev. 

%prep
rm -rf $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


%setup -n %{name}-%{version}

%build

%include compiler-load.inc

  module load intel
#  module load gotoblas
  module load mvapich2
  module load fftw3

# export LDFLAGS="${TACC_GOTOBLAS_LIB}/libgoto_lp64.a -L${TACC_FFTW3_LIB} -lfftw3 -lsvml -lifcore -limf -lm"
 export LDFLAGS="-L${TACC_FFTW3_LIB} -lfftw3 -lsvml -lifcore -limf -lm"
 export CFLAGS="-I${TACC_FFTW3_INC}"

 export  CC=`which icc || /bin/true`
 export CXX=`which icpc || /bin/true`
 export F77=`which ifort || /bin/true`

# Also build shared libs with --enable-shared
# Single precision 
./configure --enable-shared --without-x --with-fft=fftw3 --prefix=%{INSTALL_DIR}
make -j 2
make DESTDIR=$RPM_BUILD_ROOT install
make clean

# Double precision
./configure --enable-shared --without-x --with-fft=fftw3 --prefix=%{INSTALL_DIR} --enable-double
make -j 2
make DESTDIR=$RPM_BUILD_ROOT install
make clean

 export  CC=`which mpicc || /bin/true`
 export CXX=`which mpicxx || /bin/true`
 export F77=`which mpif90 || /bin/true`

# Single precision MPI-enabled mdrun
./configure --without-x --with-fft=fftw3 --prefix=%{INSTALL_DIR} --enable-mpi --program-suffix=_mpi
make -j 2 mdrun
make DESTDIR=$RPM_BUILD_ROOT install-mdrun
make clean

# Double precision MPI-enabled mdrun
./configure --without-x --with-fft=fftw3 --prefix=%{INSTALL_DIR} --enable-mpi --enable-double --program-suffix=_dbl_mpi
make -j 2 mdrun
make DESTDIR=$RPM_BUILD_ROOT install-mdrun
make clean


#./configure --enable-shared --enable-threads --with-openmp --enable-single --prefix=%{INSTALL_DIR}
#make -j 2
#make DESTDIR=$RPM_BUILD_ROOT install

%install

## Module for gromacs-4.5.3 
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[

The %{name} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_BIN %{MODULE_VAR}_DOC, %{MODULE_VAR}_LIB, and %{MODULE_VAR}_INC
for the location of the %{name} distribution, binaries, documentation,
libraries, and include files, respectively. Also, GMXLIB has been set to the
topology-file directory in %{INSTALL_DIR}/share/gromacs/top.

The only parallel component of gromacs is the molecular dynamics module,
mdrun_mpi. It can be invoked in a job script with the command:

 ibrun mdrun_mpi -s topol.tpr -o traj.trr -c confout.gro -e ener.edr -g md.log

The topology file topol.tpr, mdout.md, and deshuf.ndx should be generated with the
grompp command:

 grompp ... -po mdout.mdp -deshuf deshuf.ndx -o topol.tpr

'In GROMACS 4.x, grompp no longer accepts the -np flag (or related ones like -sort or
-shuffle), since the load-balancing is done at run-time (and by default, dynamically).
The number of processors is determined from your MPI environment and/or your command
line parameters to mpirun.'
(http://www.gromacs.org/Documentation/Gromacs_Utilities/grompp#Parallel_calculations)

Also, as of gromacs 4.0.5, TACC also provides a double-precision version of the
mdrun application, called mdrun_dbl_mpi.  To use the double-precision version,
simply replace mdrun_mpi in the commands above with mdrun_dbl_mpi.

To use the %{name} libraries, compile the source code with the option:

 -I\$%{MODULE_VAR}_INC

and add the following options to the link step: 

 -L\$%{MODULE_VAR}_LIB -l%{name}

Here is an example command to compile test.c:

 icc -I\$%{MODULE_VAR}_INC test.c -L\$%{MODULE_VAR}_LIB -l%{name}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: gromacs")
whatis("Version: %{version}")
whatis("Category: Application, Biology")
whatis("Keywords: Biology, Chemistry, Molecular Dynamics, Application")
whatis("URL: http://www.gromacs.org")
whatis("Description: molecular dynamics simulation package")

local gromacs_dir="%{INSTALL_DIR}"

setenv("TACC_GROMACS_DIR",gromacs_dir)
setenv("TACC_GROMACS_BIN",pathJoin(gromacs_dir,"bin"))
setenv("TACC_GROMACS_LIB",pathJoin(gromacs_dir,"lib"))
setenv("TACC_GROMACS_INC",pathJoin(gromacs_dir,"include"))
setenv("TACC_GROMACS_DOC",pathJoin(gromacs_dir,"share"))
setenv("GMXLIB",pathJoin(gromacs_dir,"share/gromacs/top"))

append_path("LD_LIBRARY_PATH",pathJoin(gromacs_dir,"lib"))
append_path("PATH",pathJoin(gromacs_dir,"bin"))
append_path("MANPATH",pathJoin(gromacs_dir,"share/man"))
append_path("PKG_CONFIG_PATH",pathJoin(gromacs_dir,"lib/pkgconfig"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for GROMACS 
##

set     ModulesVersion      "%version"
EOF


%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}


%post
%clean
rm -rf $RPM_BUILD_ROOT
