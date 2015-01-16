# $Id$

# Trinity can only be built on login3, and only if an admin has lifted the
# peruser process limit on your account. This is because the Trinity build
# process spawns an amazing number of forks during build
#
# Also, force Trinity to build/live under gcc4_4 - heterogeneous Intel/GCC is too messy
# Fonner added flags to rpath the GCC libraries, so GCC is no longer a dependency

Summary: Trinity De novo RNA-Seq Assembler
Name: trinityrnaseq
Version: r20121005
Release: 2
License: Copyright (c) 2012, The Broad Institute, Inc. All rights reserved.
Group: Applications/Life Sciences
Source0:  trinityrnaseq_r2012-10-05.tgz
Patch1: Trinity.pl.patch
Packager: vaughn@tacc.utexas.edu
# BuildRoot: /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# %define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
#%include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define debug_package %{nil}
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME %{name}

#%package -n %{name}-%{version}
#%package -n %{name}
#Group: Applications/Life Sciences
#Summary: De novo RNA-Seq Assembler

%description
#%description -n %{name}-%{version}
Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_TRINITY

%prep

%setup -n trinityrnaseq_r2012-10-05
%patch1 -p5

%build


if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles:/share1/apps/teragrid/modulefiles
  . $BASH_ENV
fi

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc

make LDFLAGS="-Wl,-rpath,$GCC_LIB" SYS_LIBS="-lm -pthread -Wl,-rpath,$GCC_LIB"

%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
cp -R * $RPM_BUILD_ROOT%{INSTALL_DIR}
chmod -R a+rX $RPM_BUILD_ROOT%{INSTALL_DIR}

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_BUTTERFLY, %{MODULE_VAR}_CHRYSALIS, %{MODULE_VAR}_INCHWORM and %{MODULE_VAR}_INCHWORM_BIN for the location of the %{PNAME}
distribution.

Version %{version}
]]
)

whatis("Name: Trinity RNA-Seq de novo assembler")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly, RNAseq, Transcriptome Profiling")
whatis("URL: http://trinityrnaseq.sourceforge.net/")
whatis("Description: Package for RNA-Seq de novo Assembly")


append_path("PATH",              "%{INSTALL_DIR}")
append_path("PATH",              "%{INSTALL_DIR}/Inchworm/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BUTTERFLY", "%{INSTALL_DIR}/Butterfly")
setenv (     "%{MODULE_VAR}_CHRYSALIS", "%{INSTALL_DIR}/Chrysalis")
setenv (     "%{MODULE_VAR}_INCHWORM", "%{INSTALL_DIR}/Inchworm")
setenv (     "%{MODULE_VAR}_INCHWORM_BIN", "%{INSTALL_DIR}/Inchworm/bin")

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
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean 
rm -rf $RPM_BUILD_ROOT
