#
# W. Cyrus Proctor
# 2015-08-25
# Heavily modified since

%define pkg_name_prefix tacc

# Build relative paths for installation
%if "%{?comp_fam_ver}"
    # Compiler and MPI Specific
    %if "%{?mpi_fam_ver}"
        %define pkg_name       %{pkg_name_prefix}-%{PNAME}-%{comp_fam_ver}-%{mpi_fam_ver}
        %define MODULE_SUFFIX  %{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
        %define INSTALL_SUFFIX %{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
    # Compiler Specific Only
    %else
        %define pkg_name       %{pkg_name_prefix}-%{PNAME}-%{comp_fam_ver}
        %define MODULE_SUFFIX  %{comp_fam_ver}/%{MODULES}/%{PNAME}
        %define INSTALL_SUFFIX %{comp_fam_ver}/%{PNAME}/%{version}
    %endif
# Compiler Non-specific
%else
    %define pkg_name       %{pkg_name_prefix}-%{PNAME}
    %define MODULE_SUFFIX  %{MODULES}/%{PNAME}
    %define INSTALL_SUFFIX %{PNAME}/%{version}
%endif

Name: %{pkg_name}
%define MODULE_DIR      %{APPS}/%{MODULE_SUFFIX}
%define INSTALL_DIR     %{APPS}/%{INSTALL_SUFFIX}

