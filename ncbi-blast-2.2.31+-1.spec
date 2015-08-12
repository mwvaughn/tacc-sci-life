Name: blast
Summary: NCBI BLAST+ sequence alignment package. The program compares nucleotide or protein sequences to sequence databases and calculates the statistical significance of matches.
Version: 2.2.31
Release: 1
License: GPL
Group: Applications/Life Sciences
Source: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.2.31+-x64-linux.tar.gz
Packager: vaughn@tacc.utexas.edu

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_BLAST
%define PNAME blast

## PACKAGE DESCRIPTION
%description
NCBI BLAST+ sequence alignment package. The program compares nucleotide or protein sequences to sequence databases and calculates the statistical significance of matches

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n ncbi-%{PNAME}-%{version}+

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

echo "ncbi-blast-%{version}+ is distributed as a compiled binary. We do not compile it from source."

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start
module purge
module load TACC

# Simple copy
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
For detailed assistance, please refer to the BLAST® Command Line Applications User Manual at http://www.ncbi.nlm.nih.gov/books/NBK279690/
This module defines the following environment variables: %{MODULE_VAR}_DIR, %{MODULE_VAR}_BIN
You may need to set the BLASTDB, DATA_LOADERS, BLASTDB_PROT_DATA_LOADER, BLASTDB_NUCL_DATA_LOADER, WINDOW_MASKER_PATH variables depending on your specific use case.

Version %{version}
]]
)

whatis("Name: NCBI BLAST+")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment")
whatis("URL: http://www.ncbi.nlm.nih.gov/BLAST")
whatis("Description: NCBI BLAST+ sequence alignment package. The program compares nucleotide or protein sequences to sequence databases and calculates the statistical significance of matches.")

--- do not touch this lua code
local thisFile = myFileName()
local moduleName = myModuleFullName()
local  basePath = string.sub(thisFile,1,thisFile:find(moduleName,1,true)-2)
local appPath = pathJoin(string.gsub(basePath, "(.*/).*", "%1"),moduleName)
--- do not touch this lua code

setenv( "%{MODULE_VAR}_DIR", appPath )
setenv ( "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}" )
setenv ( "%{MODULE_VAR}_BIN", pathJoin(appPath,"bin") )
prepend_path("PATH", pathJoin(appPath,"bin") )

EOF
## Modulefile End
#------------------------------------------------

## Mandatory Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
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
#%files -n %{name}-%{comp_fam_ver}
%files

# Define files permisions, user and group
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
