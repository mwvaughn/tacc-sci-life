# $Id$

# Updated build based on Dresden and IU improvements. Builds using ICC now.
# However, ICC build is plagued with segfault error in ParaFly so dropping back to GCC 4.4x
# This is supposed to be faster but due to new serial code, its actually 10% slower on the Dme13g data set

Summary: Trinity De novo RNA-Seq Assembler
Name: trinityrnaseq
Version: r20120608
Release: 1
License: Copyright (c) 2012, The Broad Institute, Inc. All rights reserved.
Group: Applications/Life Sciences
Source0:  trinityrnaseq_r2012-06-08.tgz
Packager: vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define PNAME trinityrnaseq
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_TRINITY

%description
Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads

%prep

%setup -n trinityrnaseq_r2012-06-08

%build


if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc
module load jdk64

#./configure
make
#make DESTDIR=$RPM_BUILD_ROOT install

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
whatis("Keywords:  Biology, Genomics, Assembly, RNAseq, Transcriptome Profiling")
whatis("URL: http://trinityrnaseq.sourceforge.net/")
whatis("Description: Package for RNA-Seq de novo Assembly")


prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BUTTERFLY", "%{INSTALL_DIR}/Butterfly")
setenv (     "%{MODULE_VAR}_CHRYSALIS", "%{INSTALL_DIR}/Chrysalis")
setenv (     "%{MODULE_VAR}_INCHWORM", "%{INSTALL_DIR}/Inchworm")
setenv (     "%{MODULE_VAR}_INCHWORM_BIN", "%{INSTALL_DIR}/Inchworm/bin")

prereq ("jdk64")

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
