%define		PNAME	singularity
Version:	2.2.99
Release:	1
License:	BSD-3-Clause-LBNL
URL:		http://singularity.lbl.gov
Source:		%{PNAME}-%{version}.tar.gz
Packager:	TACC - gzynda@tacc.utexas.edu
Group:		Applications
Summary: 	Application and environment virtualization

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

%define _prefix	%{INSTALL_DIR}
%define _sysconfdir	%{INSTALL_DIR}/etc
%define _bindir	%{INSTALL_DIR}/bin
%define _mandir	%{INSTALL_DIR}/share/man
%define _libdir	%{INSTALL_DIR}/lib64
%define _libexecdir	%{INSTALL_DIR}/libexec
%define _localstatedir	%{INSTALL_DIR}/libexec

#%define MODULE_VAR      %{MODULE_VAR_PREFIX}LZ4
# This was changed to automatically reflect PNAME
%define MODULE_VAR      %{MODULE_VAR_PREFIX}SINGULARITY

## PACKAGE DESCRIPTION
%description
Singularity provides functionality to build the smallest most minimal
possible containers, and running those containers as single application
environments.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}	#Delete the install directory
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}	#Delete the build directory

## SETUP
# No tar to unpack, this pulls from git
%setup -n %{PNAME}-%{version}

## BUILD
%build
if [ ! -f configure ]; then
  ./autogen.sh
  ./configure --prefix=%{INSTALL_DIR}
fi

#%configure \
#%if %slurm
#  --with-slurm
#%else
#  --without-slurm
#%endif

%{__make} %{?mflags}


#---------------------------------------
%install
#---------------------------------------

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Purge environment and reload TACC defaults
module purge
module load TACC

%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
rm -f $RPM_BUILD_ROOT/%{_libdir}/singularity/lib*.la
cp -r examples AUTHORS COPYING ChangeLog INSTALL LICENSE NEWS README.md $RPM_BUILD_ROOT/%{INSTALL_DIR}

sed -i "s/\/opt\/apps\/singularity\/2.2.99/\$%{MODULE_VAR}_DIR/g" $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/*

## Install Steps End
#--------------------------------------

#--------------------------------------

#--------------------------------------
## Modulefile Start
#--------------------------------------
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:

 - %{MODULE_VAR}_DIR
 - %{MODULE_VAR}_BIN
 - %{MODULE_VAR}_LIB
 - %{MODULE_VAR}_INC
 - %{MODULE_VAR}_LEXE
 - %{MODULE_VAR}_ETC
 - %{MODULE_VAR}_EXAMPLES

for the location of the %{PNAME} distribution.

Documentation: %{url}

Version %{version}
]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: applications, virtualization")
whatis("Keywords: virtualization, applications")
whatis("Description: Application and environment virtualization")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH",		"%{INSTALL_DIR}/lib64")
prepend_path("MANPATH",		"%{INSTALL_DIR}/share/man")

setenv("%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_EXAMPLES",     "%{INSTALL_DIR}/examples")
setenv("%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_ETC",	"%{INSTALL_DIR}/etc")
setenv("%{MODULE_VAR}_INC",	"%{INSTALL_DIR}/include")
setenv("%{MODULE_VAR}_LIB",	"%{INSTALL_DIR}/lib64")
setenv("%{MODULE_VAR}_LEXE",	"%{INSTALL_DIR}/libexec")
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

%defattr(-, root, root)
#%doc examples AUTHORS COPYING ChangeLog INSTALL LICENSE NEWS README.md
%attr(0755, root, root) %dir %{_sysconfdir}/singularity
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/singularity/*
%dir %{_localstatedir}/lib/singularity
%dir %{_localstatedir}/lib/singularity/mnt

%{_bindir}/singularity
%{_bindir}/run-singularity
%{_mandir}/man1/*
%{_libdir}/singularity/lib*.so.*
%{_sysconfdir}/bash_completion.d/singularity

#SUID programs
%attr(4755, root, root) %{_libexecdir}/singularity/bin/action-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/create-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/copy-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/expand-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/export-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/import-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/mount-suid

# Binaries
%{_libexecdir}/singularity/bin/action
%{_libexecdir}/singularity/bin/bootstrap
%{_libexecdir}/singularity/bin/cleanupd
%{_libexecdir}/singularity/bin/copy
%{_libexecdir}/singularity/bin/create
%{_libexecdir}/singularity/bin/expand
%{_libexecdir}/singularity/bin/export
%{_libexecdir}/singularity/bin/get-section
%{_libexecdir}/singularity/bin/import
%{_libexecdir}/singularity/bin/mount

# Scripts
%{_libexecdir}/singularity/functions
%{_libexecdir}/singularity/image-handler.sh

# Directories
%{_libexecdir}/singularity/bootstrap-scripts
%{_libexecdir}/singularity/cli
%{_libexecdir}/singularity/python

## POST
%post

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT
