Summary:    Stacks - short-read genomics pipeline
Name:       stacks
Version:    1.06
Release:    1
License:    GPLv3
Vendor:     Cresko Lab at U Oregon
Group:      Applications/Life Sciences
Source0:     %{name}-%{version}.tar.gz
Source1:  http://sourceforge.net/projects/samtools/files/samtools/0.1.19/samtools-0.1.19.tar.bz2
Packager:   TACC - jfonner@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc
%include ../system-defines.inc

%define PNAME stacks
%define MODULE_VAR %{MODULE_VAR_PREFIX}STACKS
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}

%description
Stacks is a software pipeline for building loci from short-read sequences, such as those generated on the Illumina platform.
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-%{version}

# The next command unpacks Source1
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source). 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -T -D -a 1

%build

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include ../system-load.inc

module purge
module load TACC

%if "%{PLATFORM}" == "stampede"
  module load samtools
  ./configure CC=icc CXX=icpc --prefix=%{INSTALL_DIR} --enable-bam --with-bam-include-path=$TACC_SAMTOOLS_INC --with-bam-lib-path=$TACC_SAMTOOLS_LIB
  make CC=icc CXX=icpc
  make CC=icc CXX=icpc DESTDIR=$RPM_BUILD_ROOT install
  cp LICENSE README ChangeLog $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if "%{PLATFORM}" == "lonestar"
  module swap $TACC_FAMILY_COMPILER gcc
  cd samtools*
  MY_SAMTOOLS_DIR=$PWD
  make
  cd ..
  #./configure --prefix=%{INSTALL_DIR} --enable-bam --with-bam-include-path=$TACC_SAMTOOLS_INC --with-bam-lib-path=$TACC_SAMTOOLS_LIB
  ./configure --prefix=%{INSTALL_DIR} --enable-bam --with-bam-include-path=$MY_SAMTOOLS_DIR --with-bam-lib-path=$MY_SAMTOOLS_DIR
  make
  make DESTDIR=$RPM_BUILD_ROOT install
  cp LICENSE README ChangeLog $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/samtools
  cp -R ./samtools*/{samtools,bcftools,misc,libbam.a,*.h} $RPM_BUILD_ROOT/%{INSTALL_DIR}/samtools
%endif


# MODULEFILE CREATION
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{PNAME} built with icc.
Documentation for %{PNAME} is available online at http://creskolab.uoregon.edu/stacks/
The stacks executable can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing")
whatis("Description: Stacks - short-read genomics pipeline")
whatis("URL: http://creskolab.uoregon.edu/stacks/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin/")
append_path("PATH"       ,"%{INSTALL_DIR}/bin")

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

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
rm -rf $RPM_BUILD_ROOT
