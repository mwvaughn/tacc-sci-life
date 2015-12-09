%define PNAME sratoolkit
%define pkg_base_name sratoolkit
%define MODULE_VAR    SRATOOLKIT

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 5
%define micro_version 5

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###

## System Definitions
# TACC LSC uses a set of system defines to make
# our RPM builds portable
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc

## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
%include ./include/name-defines.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
#Name:      %{pkg_name}
Version:   %{pkg_version}
#BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Summary:    The NCBI SRA toolkit
License:    GPL
URL:        http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=software
Packager:   TACC - jawon@tacc.utexas.edu
Source:     http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.5.5/sratoolkit.2.5.5-centos_linux64.tar.gz
Vendor:     NCBI
Group: Applications/Life Sciences
Release:   1

%description
The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

#%define INSTALL_DIR %{APPS}/%{name}/%{version}
#%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
#%define MODULE_VAR  %{MODULE_VAR_PREFIX}SRATOOLKIT
#%define PNAME       sratoolkit

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
#%setup -n %{PNAME}-%{version}
%setup -n sratoolkit.2.5.5-centos_linux64

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

#--------------------------------------
%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    ########### Do Not Remove #############

#--------------------------------------
## Install Steps Start
module purge
module load TACC python

## Install Steps End
#--------------------------------------
cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif
#--------------------------------------

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
The SRA Toolkit module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{name}
distribution. Documentation can be found online at https://github.com/ncbi/sra-tools/wiki

Version %{version}

]])

whatis("Name: sratools")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: archive, ncbi, utility, genomics")
whatis("Description: The SRA Toolkit and SDK from NCBI is a collection of tools and libraries for using data in the INSDC Sequence Read Archives.")
whatis("URL: https://github.com/ncbi/sra-tools")

local sra_dir = "%{INSTALL_DIR}"

setenv("%{MODULE_VAR}_DIR",	sra_dir)
setenv("%{MODULE_VAR}_EXAMPLE",	pathJoin(sra_dir,"example"))

prepend_path("PATH",		pathJoin(sra_dir,"bin"))

EOF
## Modulefile End
#--------------------------------------

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
