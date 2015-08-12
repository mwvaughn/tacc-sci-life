Name: mach
Summary: Markov Chain based haplotyper
Version: 1.0.18
Release: 3
License: Unknown
Group: Applications/Life Sciences/genetics
Source: http://csg.sph.umich.edu/abecasis/MACH/download/mach.1.0.18.source.tgz
Packager: TACC - vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_MACH
%define PNAME mach

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
MACH is a fast Markov Chain based haplotyper

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -c -n %{name}-%{version}

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

# Original CFLAGS contained -static which was causing failure
make all 'CFLAGS=-O2 -I./libsrc -I./mach1 -I./thunder -D__ZLIB_AVAILABLE__  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE'

# May want to revisit placement of this, or alternative implementation
export DONT_STRIP=1

cp executables/mach1 executables/thunder $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
MACH 1.0 is a Markov Chain based haplotyper. It can resolve long haplotypes or infer
missing genotypes in samples of unrelated individuals. The current version is a pre-release.
Documentation is available at http://www.sph.umich.edu/csg/abecasis/MACH
The executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: MACH")
whatis("Version: %{version}")
whatis("Category: Computational biology, genetics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing, Genetics, GWAS, Imputation")
whatis("Description: Markov Chain based haplotyper")
whatis("URL: http://www.sph.umich.edu/csg/abecasis/MACH")

--- do not touch this lua code
local thisFile = myFileName()
local moduleName = myModuleFullName()
local  basePath = string.sub(thisFile,1,thisFile:find(moduleName,1,true)-2)
local appPath = pathJoin(string.gsub(basePath, "(.*/).*", "%1"),moduleName)
--- do not touch this lua code

setenv("%{MODULE_VAR}_DIR", appPath)
prepend_path("PATH"     , appPath)

EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

## VERSION FILE
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
#%files -n %{name}-%{comp_fam_ver}
%files

# Define files permissions, user, and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

## CLEAN UP
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
