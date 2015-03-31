Name:      bsmap
Summary:   BSMAP for Methylation
Version:   2.89
Release:   1
License:   GPL
Vendor:    Brown University
Group:     Applications/Life Sciences
Source:    http://lilab.research.bcm.edu/dldcc-web/lilab/yxi/bsmap/bsmap-%{version}.tgz
Packager:  TACC - gzynda@tacc.utexas.edu
Prefix:    /opt/apps

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
%define MODULE_VAR  %{MODULE_VAR_PREFIX}BSMAP
%define PNAME       bsmap

%package -n %{name}-%{comp_fam_ver}
Summary:   BSMAP for Methylation
Group:     Applications/Life Sciences

## PACKAGE DESCRIPTION
%description
%description -n %{name}-%{comp_fam_ver}
BSMAP is a short reads mapping program for bisulfite sequencing in DNA methylation study.  Bisulfite treatment coupled with next generation sequencing could estimate the methylation ratio of every single Cytosine location in the genome by mapping high throughput bisulfite reads to the reference sequences.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}

## SETUP
%setup -n %{PNAME}-%{version}

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
%include ./include/compiler-load.inc

# patch mising include
patch param.h -i - <<EOF
11a10
> #include<unistd.h>
EOF
# patch CC to be CXX
sed -i "s/CC/CXX/g" makefile

# Make and install
make CC=$CC CXX=$CXX
make CC=$CC CXX=$CXX BIN=$RPM_BUILD_ROOT/%{INSTALL_DIR} install

## Install Steps End

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
Documentation for %{PNAME} is available online at the publisher website: https://code.google.com/p/bsmap/

For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include %{PNAME}.

Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics, methylation, aligner")
whatis("Keywords: Biology, Genomics, Mapping")
whatis("Description: BSMAP - short reads mapping software for bisulfite sequencing reads")
whatis("URL: https://code.google.com/p/bsmap/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")
prereq("samtools","python")
]])
EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# VERSON FILE
#------------------------------------------------
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}-%{comp_fam_ver}
#%files 

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}
#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Remove the installation files now that the RPM has been generated
cd /tmp && rm -rf $RPM_BUILD_ROOT
