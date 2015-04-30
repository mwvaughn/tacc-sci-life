Name:      mummer
Summary:   MUMmer - A modular system for the rapid whole genome alignment of finished or draft sequence
Version:   3.23
Release:   3
License:   OSI Certified Open Source Software
Vendor:    Johns Hopkins University
Group:     Applications/Life Sciences
Source:    http://sourceforge.net/projects/mummer/files/mummer/%{version}/MUMmer%{version}.tar.gz
Packager:  TACC - gzynda@tacc.utexas.edu
Prefix:    /opt/apps

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}MUMMER
%define PNAME       mummer

%package -n %{name}-%{comp_fam_ver}
Summary:    MUMmer - A modular system for the rapid whole genome alignment of finished or draft sequence
Group:     Applications/Life Sciences

## PACKAGE DESCRIPTION
%description
%description -n %{name}-%{comp_fam_ver}
MUMmer is a system for rapidly aligning entire genomes, whether in complete or draft form. For example, MUMmer 3.0 can find all 20-basepair or longer exact matches between a pair of 5-megabase genomes in 13.7 seconds, using 78 MB of memory, on a 2.4 GHz Linux desktop computer. MUMmer can also align incomplete genomes; it can easily handle the 100s or 1000s of contigs from a shotgun sequencing project, and will align them to another set of contigs or a genome using the NUCmer program included with the system. If the species are too divergent for a DNA sequence alignment to detect similarity, then the PROmer program can generate alignments based upon the six-frame translations of both input sequences

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}

## SETUP
%setup -n MUMmer%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
## Install Steps Start
module purge
module load TACC
%include ./include/compiler-load.inc

# Make and install
RPATH="-Wl,-rpath,"$ICC_LIB
make CC=$CC CXX=$CXX AR=xiar LDFLAGS=$RPATH
# Change static paths to environment variables
for f in `find . -type f -exec grep -Il "$PWD" {} \;`; do sed -i "s|$PWD|\$ENV{'%{MODULE_VAR}_DIR'}|g" $f; done
# Delete source files
lfs find . -name \*.c -name \*.o -name \*.h -name \*.cc -name \*.hh -name Makefile | xargs -n 1 rm
# Copy files int install dir
cp -R * $RPM_BUILD_ROOT/%{INSTALL_DIR}


## Install Steps End

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
# Modulefile Start
#------------------------------------------------
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with intel/15.0.2. Documentation is available online at the publisher's website:

http://mummer.sourceforge.net/

The MUMmer executables can be found in %{MODULE_VAR}_DIR

Dependencies: MUMmer is a complex workflow system, with many potential dependencies. 

Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Assembly")
whatis("Description: MUMmer - A modular system for the rapid whole genome alignment of finished or draft sequence")
whatis("URL: http://mummer.sourceforge.net/")


prereq ("perl")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")
prepend_path("PERL5LIB"       ,"%{INSTALL_DIR}/scripts")
EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# VERSON FILE
#------------------------------------------------
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
%files -n %{name}-%{comp_fam_ver}
#%files 

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}
#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Remove the installation files now that the RPM has been generated
cd /tmp && rm -rf $RPM_BUILD_ROOT
