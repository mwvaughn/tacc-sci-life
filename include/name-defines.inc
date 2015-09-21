#
# W. Cyrus Proctor
# 2015-08-25

# Build relative paths for installation
%if "%{?comp_fam_ver}"
    # Compiler and MPI Specific
    %if "%{?mpi_fam_ver}"
        %define MODULE_SUFFIX  %{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}
        %define INSTALL_SUFFIX %{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
    # Compiler Specific Only
    %else
        %define MODULE_SUFFIX  %{comp_fam_ver}/%{MODULES}/%{name}
        %define INSTALL_SUFFIX %{comp_fam_ver}/%{name}/%{version}
    %endif
# Compiler Non-specific
%else
    %define MODULE_SUFFIX  %{MODULES}/%{name}
    %define INSTALL_SUFFIX %{name}/%{version}
%endif

# NOTES:
# Leave MODULE_PREFIX and INSTALL_PREFIX as /tmpmod and /tmprpm!
# These are temporary placeholders that allow for install-time
# relocation via rpm. They must be unique and *not* nested. 
# /tmpmod and /tmprpm should *never* be the final install locations.

# Module macros
%define MODULE_PREFIX   /tmpmod 
%define MODULE_DIR      %{MODULE_PREFIX}/%{MODULE_SUFFIX}
%define MODULE_FILENAME %{version}.lua

# Install macros
%define INSTALL_PREFIX  /tmprpm
%define INSTALL_DIR     %{INSTALL_PREFIX}/%{INSTALL_SUFFIX}

# Subpackage macros
%define PACKAGE             package
%define MODULEFILE          modulefile
%define BUILD_PACKAGE       %( if [ ${NO_PACKAGE:=0}    = 0 ]; then echo "1"; else echo "0"; fi )
%define BUILD_MODULEFILE    %( if [ ${NO_MODULEFILE:=0} = 0 ]; then echo "1"; else echo "0"; fi )
%define RPM_PACKAGE_NAME    %{name}-%{PACKAGE}-%{version}-%{release}
%define RPM_MODULEFILE_NAME %{name}-%{MODULEFILE}-%{version}-%{release}

#---------------------------------------
# Must install with with:
# "rpm --relocate"  
Prefix:    %{MODULE_PREFIX}
Prefix:    %{INSTALL_PREFIX}
#---------------------------------------

