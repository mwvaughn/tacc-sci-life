#
# $Id: blast-plus.spec 506 2011-01-13 04:55:47Z bdkim $
#

Summary: ncbi-blast+ 

%define major_version 2
%define minor_version 2 
%define micro_version 24

Name: ncbi-blast
Version: %{major_version}.%{minor_version}.%{micro_version}
Release: 1
License: GPLv2
Group: Applications/Life Sciences 
Source: ncbi-blast-%{major_version}.%{minor_version}.%{micro_version}.tar.gz
Packager: TACC - {bdkim}@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

# TACC %defines

%define APPS /opt/apps
%define MODULES modulefiles

%include rpm-dir.inc
%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

# For system gcc, install in /opt/apps instead of /opt/apps/comp_fam_ver

#%if "%{is_gcc}" == "1"
#  %define INSTALL_DIR %{APPS}/%{name}/%{version}
#  %define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
#%endif

%package -n %{name}-%{comp_fam_ver}
Summary: NCBI-BLAST+ 
Group: Applications/Life Sciences 

%description
%description -n %{name}-%{comp_fam_ver}
BLAST+ is a new suite of BLAST tools that utilizes the NCBI C++ Toolkit. The BLAST+ applications have a number of performance and feature improvements over the legacy BLAST applications.The legacy BLAST executables (blastall et al.) are based on the NCBI C Toolkit. While no new features will be added to these applications, periodic bugfix releases will be available in the interim from ftp://ftp.ncbi.nlm.nih.gov/blast/executables/release/LATEST/.
BLAST databases are updated daily and may be downloaded via FTP from ftp://ftp.ncbi.nlm.nih.gov/blast/db/. Database sets may be retrieved automatically with update_blastdb.pl. Please refer to the BLAST database documentation for more details.

%prep

rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


##
## SETUP (The -n is needed here because boost untars to
## a directory with a different name than the tar file.)
##

%setup -n %{name}-%{major_version}.%{minor_version}.%{micro_version}+-src/c++

##
## BUILD
##

%build

%include compiler-load.inc

# module load boost

%if "%{is_intel11}" == "1"
	# environment used for configure with intel compiler
	# export CFLAGS="-O3 -xO" 
        # Ranger Intel9: -xW (safer)
        # Ranger Intel10: -xO (generates different SSE instructions than xW, may be riskier)

	# fix for intel-11 malloc
	#####export CONFIGURE_FLAGS=--with-toolset=intel-linux
	export CONFIGURE_FLAGS=--with-toolset=intel-11.1
   export CFLAGS='-O2 -xSSE4.2 -fp-model fast=2'
   export CPPFLAGS='-O2 -xSSE4.2 -fp-model fast=2'
#  export BOOST_INCLUDE='-I/${TACC_BOOST_INC}'
#  export BOOST_LIBPATH='-L/${TACC_BOOST_LIB} -Wl,-rpath,${TACC_BOOST_LIB}'

%endif

# is_gcc   == system GCC 4.1.2
%if "%{is_gcc}" == "1"
  export CFLAGS= -O2
  export CPPFLAGS= -O2
#  export BOOST_INCLUDE='-I/${TACC_BOOST_INC}'
#  export BOOST_LIBPATH='-L/${TACC_BOOST_LIB} -Wl,-rpath,${TACC_BOOST_LIB}'
%endif


# is_gcc44 == GCC 4.4.x
%if "%{is_gcc44}" == "1"
  module load gcc/4.4.5
#  export CFLAGS= -O2
#  export CPPFLAGS= -O2
#  export BOOST_INCLUDE='-I/${TACC_BOOST_INC}'
#  export BOOST_LIBPATH='-L/${TACC_BOOST_LIB} -Wl,-rpath,${TACC_BOOST_LIB}' 
%endif

#cd c++
./configure --without-debug --prefix=%{INSTALL_DIR}
make

%install 
#cd c++
make DESTDIR=$RPM_BUILD_ROOT install
#make install

## Module for blast-2.2.24+ 
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[

The blast module file defines the following environment variables:
TACC_BLAST_BIN, TACC_BLAST_INC, TACC_BLAST_LIB for the location of the BLAST+ binaries, header files, and libraries respectively.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: blast")
whatis("Version: %{version}")
whatis("Category: Application, Biology")
whatis("Keywords: Biology, Application, Genomics")
whatis("URL: http://www.ncbi.nlm.nih.gov")
whatis("Description: a new suite of BLAST tools that utilizes the NCBI C++ Toolkit.")

local blast_dir="%{INSTALL_DIR}"

setenv("TACC_BLAST_DIR",blast_dir)
setenv("TACC_BLAST_BIN",pathJoin(blast_dir,"bin")
setenv("TACC_BLAST_LIB",pathJoin(blast_dir,"lib"))
setenv("TACC_BLAST_INC",pathJoin(blast_dir,"include"))

append_path("LD_LIBRARY_PATH",pathJoin(blast_dir,"lib"))
append_path("PATH",pathJoin(blast_dir,"bin"))
append_path("MANPATH",pathJoin(blast_dir,"share/man"))
append_path("PKG_CONFIG_PATH",pathJoin(blast_dir,"lib/pkgconfig"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for BLAST
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
