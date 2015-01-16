#
# Spec file for mafft
#
Summary:   MAFFT a sequence alignment code
Name:      mafft
Version:   6.853 
Release:   1
License:   BSD
Group: Applications/Life Sciences
Source:    mafft_6.853.tar.gz
Packager:  TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary:   MAFFT - a multiple sequence alignment program
Group: Applications/Life Sciences

%description
%description -n %{name}-%{comp_fam_ver}

MAFFT is a multiple sequence alignment program for unix-like operating systems.  
It offers a range of multiple alignment methods, L-INS-i (accurate; for alignment 
of <#200 sequences), FFT-NS-2 (fast; for alignment of <#10,000 sequences), etc. 

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n mafft_%{version}


%build

%include compiler-load.inc

# Use mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}
#Build core
export PREFIX=%{INSTALL_DIR}
cd core
make clean
make  

#Build extensions
cd ../extensions
make clean
make  

%install
export PREFIX=%{INSTALL_DIR}
cd core
make install
cd ../extensions
make install

#  Kluge, the make install, installs in the mounted directory
# copy to the rpm directory
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
#Unmount tmpfs
umount                                   %{INSTALL_DIR}

## Module for mafft
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The mafft modulefile defines the following environment variables,
TACC_MAFFT_DIR, TACC_MAFFT_BIN, TACC_MAFFT_LIB, and TACC_MAFFT_MAN
for the location of the mafft directory, binaries, scripts, and man 
page.

The modulefile also appends TACC_MAFFT_BIN directory to PATH, 
adds TACC_MAFFT_LIB to LD_LIBRARY_PATH, and adds TACC_MAFFT_MAN to
MANPATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: MAFFT")
whatis("Version: %{version}")
whatis("Category: application, biology")
whatis("Keywords: Biology, Alignment, Genomics, Application")
whatis("URL:  http://mafft.cbrc.jp/alignment/software/")
whatis("Description: Multiple alignment program for amino acid or nucleotide sequences")

setenv("TACC_MAFFT_DIR"       ,"%{INSTALL_DIR}")
setenv("TACC_MAFFT_BIN"      ,"%{INSTALL_DIR}/bin")
setenv("TACC_MAFFT_LIB"      ,"%{INSTALL_DIR}/libexec")
setenv("TACC_MAFFT_MAN"      ,"%{INSTALL_DIR}/share/man")

prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/libexec/mafft")
prepend_path("MANPATH","%{INSTALL_DIR}/share/man")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for mafft
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n %{name}-%{comp_fam_ver}
%defattr(755,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT
