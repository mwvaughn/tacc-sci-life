Name: sratoolkit
Summary: SRA Toolkit
Version: 2.5.2
Release: 1
License: Public Domain
Vendor: National Center for Biotechnology Information
Group: Applications/Life Sciences
Source: http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.5.2/sratoolkit.2.5.2-centos_linux64.tar.gz
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
%define MODULE_VAR TACC_SRATOOLKIT
%define PNAME sratoolkit

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n %{name}.%{version}-centos_linux64

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

echo "SRA Toolkit is distributed as compiled binary for Centos 64bit. No compilation was necessary."

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
Documentation can be found online at http://www.ncbi.nlm.nih.gov/books/NBK158900/
The executables can be found in %{MODULE_VAR}_BIN

Version %{version}
]]
)

whatis("Name: NCBI SRA Toolkit")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Quality Control, Utility, Sequencing, NCBI, SRA")
whatis("URL: http://www.ncbi.nlm.nih.gov/books/NBK158900/")
whatis("Description: The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the NCBI Sequence Read Archives.")

--- do not touch this lua code
local thisFile = myFileName()
local moduleName = myModuleFullName()
local  basePath = string.sub(thisFile,1,thisFile:find(moduleName,1,true)-2)
local appPath = pathJoin(string.gsub(basePath, "(.*/).*", "%1"),moduleName)
--- do not touch this lua code

setenv( "%{MODULE_VAR}_DIR", appPath )
setenv( "%{MODULE_VAR}_BIN", pathJoin(appPath,"bin") )
prepend_path( "PATH"     , pathJoin(appPath,"bin") )

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
