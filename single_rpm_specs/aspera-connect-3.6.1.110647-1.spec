%define PNAME aspera-connect
Version: 3.6.1.110647
Release: 1
License: IBM License
Vendor: IBM
Packager: TACC - gzynda@tacc.utexas.edu
Source: http://download.asperasoft.com/download/sw/connect/3.6.1/aspera-connect-3.6.1.110647-linux-64.tar.gz
Summary: Aspera Connect client
Group: Applications/Life Sciences
Url: http://download.asperasoft.com/download/docs/ascp/3.5.2/html/index.html#dita/ascp_usage.html

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}ASPERA

## PACKAGE DESCRIPTION
%description
The ascp (Aspera secure copy) executable is a command-line fasp transfer program.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

## SETUP
%setup -n %{PNAME}-%{version}-linux-64 -c

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

if [ "%{PLATFORM}" != "ls5" ]
then
	module purge
	module load TACC
fi

export PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR}

## Patch
patch aspera-connect-3.6.1.110647-linux-64.sh -i - <<'EOF'
11c11
< INSTALL_DIR=~/.aspera/connect
---
> INSTALL_DIR=$PREFIX
EOF

bash aspera-connect-3.6.1.110647-linux-64.sh

rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/etc/asperaconnect.path
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/var
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/res
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/localization
# comes with a libc that breaks things
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:

	%{MODULE_VAR}_DIR - the location of the %{PNAME} distribution
	%{MODULE_VAR}_ASCP - the location of the ascp program
	%{MODULE_VAR}_OPENSSH - the location of the openssh key

Additinal documentation can be found online at %{URL}.

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: transfer, ncbi, utility, genomics")
whatis("Description: Aspera Connect client")
whatis("URL: http://asperasoft.com/software/transfer-clients/")

setenv("%{MODULE_VAR}_DIR",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_ASCP",	"%{INSTALL_DIR}/bin/ascp")
setenv("%{MODULE_VAR}_KEY",	"%{INSTALL_DIR}/etc/asperaweb_id_dsa.openssh")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")

EOF
## Modulefile End
#--------------------------------------

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
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files
%defattr(-,root,install,)
%{INSTALL_DIR}
%{MODULE_DIR}

## POST 
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
