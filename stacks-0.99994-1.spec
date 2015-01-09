Summary:    Stacks - short-read genomics pipeline
Name:       stacks
Version:    0.99994
Release:    1
License:    GPLv3
Vendor:     Cresko Lab at U Oregon
Group:      Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jfonner@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc
%include ../system-defines.inc

%define PNAME stacks
%define MODULE_VAR TACC_STACKS
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}

%description

# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-%{version}

%build

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include ../system-load.inc

module purge
module load TACC
module load samtools

#%if "%{PLATFORM}" == "stampede"
  ./configure CC=icc CXX=icpc --prefix=%{INSTALL_DIR} --enable-bam --with-bam-include-path=$TACC_SAMTOOLS_INC --with-bam-lib-path=$TACC_SAMTOOLS_LIB
#%endif

#%if "%{PLATFORM}" == "lonestar"
#  ./configure CC=icc CXX=icpc --prefix=%{INSTALL_DIR} --enable-bam --with-bam-include-path=$TACC_SAMTOOLS_INC/bam --with-bam-lib-path=$TACC_SAMTOOLS_LIB
#%endif

make
make DESTDIR=$RPM_BUILD_ROOT install

cp LICENSE README ChangeLog $RPM_BUILD_ROOT/%{INSTALL_DIR}

# MODULEFILE CREATION
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with icc.
Documentation for %{name} is available online at the website: http://creskolab.uoregon.edu/stacks/
The stacks executable can be found in %{MODULE_VAR}_BIN

Version %{version}
]])

whatis("Name: bwa")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing")
whatis("Description: Stacks - short-read genomics pipeline")
whatis("URL: http://creskolab.uoregon.edu/stacks/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin/")
append_path("PATH"       ,"%{INSTALL_DIR}/bin")

EOF

#--------------
#  Version file.
#--------------

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
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
rm -rf $RPM_BUILD_ROOT
