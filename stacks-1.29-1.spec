Name:       stacks
Version:    1.29
Release:    1
License:    GPLv3
Vendor:     Cresko Lab at U Oregon
Group:      Applications/Life Sciences
Source0:    http://creskolab.uoregon.edu/stacks/source/stacks-1.29.tar.gz
Source1:    http://sourceforge.net/projects/samtools/files/samtools/0.1.19/samtools-0.1.19.tar.bz2
Packager:   TACC - jfonner@tacc.utexas.edu
Summary:    Stacks - short-read genomics pipeline
Prefix:     /opt/apps

# build with: 
#   build_rpm.sh --gcc=47 stacks-1.29-1.spec
#   build_rpm.sh --intel=15 stacks-1.29-1.spec

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR %{MODULE_VAR_PREFIX}STACKS
%define PNAME stacks

%package -n %{name}-%{comp_fam_ver}
Summary: Stacks - short-read genomics pipeline
Group:   Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}
Stacks is a software pipeline for building loci from short-read sequences, such as those generated on the Illumina platform.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n %{name}-%{version}

# The next command unpacks Source1
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source). 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -T -D -a 1

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start
module purge
module load TACC
# won't build under intel 13
%include ./include/compiler-load.inc

mv samtools* samtools
cd samtools
MY_SAMTOOLS_DIR=$PWD
make
cd ..
./configure CC=$CC CXX=$CXX --prefix=%{INSTALL_DIR} --enable-bam --with-bam-include-path=$MY_SAMTOOLS_DIR --with-bam-lib-path=$MY_SAMTOOLS_DIR

if [ -n "$GCC_LIB" ]; then
  make CC=$CC CXX=$CXX LDFLAGS="-Wl,-rpath,$GCC_LIB"
  make CC=$CC CXX=$CXX DESTDIR=$RPM_BUILD_ROOT LDFLAGS="-Wl,-rpath,$GCC_LIB" install
else  
  make CC=$CC CXX=$CXX
  make CC=$CC CXX=$CXX DESTDIR=$RPM_BUILD_ROOT install
fi

cp LICENSE README ChangeLog $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/samtools
cp -R ./samtools*/{samtools,bcftools,misc,libbam.a,*.h} $RPM_BUILD_ROOT/%{INSTALL_DIR}/samtools
## Install Steps End
#------------------------------------------------

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
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
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
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
%files -n %{name}-%{comp_fam_ver}
# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

## CLEAN UP
%post -n %{name}-%{comp_fam_ver}
%clean
rm -rf $RPM_BUILD_ROOT
