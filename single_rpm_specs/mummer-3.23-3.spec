#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------
%define PNAME mummer
Summary:    MUMmer - A modular system for the rapid whole genome alignment of finished or draft sequence
Version:    3.23
Release:    4
License:    OSI Certified Open Source Software
Group: Applications/Life Sciences
Source: http://sourceforge.net/projects/mummer/files/mummer/%{version}/MUMmer%{version}.tar.gz
Packager:   TACC - vaughn@tacc.utexas.edu

# Force the module to NOT be relocatable
# See the hack in the install section for why this is not a portable RPM
Prefix: /opt/apps

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}MUMMER

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
MUMmer is a system for rapidly aligning entire genomes, whether in complete or draft form. For example, MUMmer 3.0 can find all 20-basepair or longer exact matches between a pair of 5-megabase genomes in 13.7 seconds, using 78 MB of memory, on a 2.4 GHz Linux desktop computer. MUMmer can also align incomplete genomes; it can easily handle the 100s or 1000s of contigs from a shotgun sequencing project, and will align them to another set of contigs or a genome using the NUCmer program included with the system. If the species are too divergent for a DNA sequence alignment to detect similarity, then the PROmer program can generate alignments based upon the six-frame translations of both input sequences

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

# Unpack source
%setup -n MUMmer%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start
# CFLAGS='-march=sandybridge -mtune=haswell' CXXFLAGS='-march=sandybridge -mtune=haswell'
make CFLAGS='-march=sandybridge -mtune=haswell' CXXFLAGS='-march=sandybridge -mtune=haswell'

# Manually fix paths for Mummer. This means the RPM will not be relocatable but
# the underlying scripts are too dumb for this to work otherwise

OWD=$PWD
TARGET_DIR=%{INSTALL_DIR}
SCRIPTS=$(find . -maxdepth 2 -type f -exec grep -Iq . {} \; -and -print)
for X in $SCRIPTS
    do
    echo $X
    sed -i "s|$OWD|$TARGET_DIR|g" $X
done

rm -rf src Makefile
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Modulefile Begin

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{pname} built with gcc. Documentation is available online at

http://mummer.sourceforge.net/

The MUMmer executables can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: mummer")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Assembly")
whatis("Description: MUMmer - A modular system for the rapid whole genome alignment of finished or draft sequence")
whatis("URL: http://mummer.sourceforge.net/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")

prepend_path("PATH"       ,"%{INSTALL_DIR}/")
prepend_path("PERL5LIB"       ,"%{INSTALL_DIR}/scripts")

EOF

# Modulefile End


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