Name: exonerate-gff3
Version: 2.3.0
Release: 1
License: GPL
Group: Applications/Life Sciences
Source:  https://github.com/hotdogee/exonerate-gff3/archive/2.3.0.tar.gz
Packager: NAL - monica.poelchau@ars.usda.gov
Summary: This is an exonerate fork with added gff3 support. Original website with user guides: http://www.ebi.ac.uk/~guy/exonerate/
Prefix: /opt/apps

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

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}EXONERATE-GFF3
%define PNAME       exonerate-gff3

## PACKAGE DESCRIPTION
%description
This is an exonerate fork with added gff3 support. Original website with user guides: http://www.ebi.ac.uk/~guy/exonerate/. New Option: --gff3 [FALSE]. Using the "--gff3 yes" option with the "--showtargetgff yes" option will output GFF3. Without the "--gff3 yes" option, everything works just as before so previous scripts relying on the old output format won’t break. 

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n %{PNAME}-%{version}

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
module swap $TACC_FAMILY_COMPILER gcc

./configure --prefix=%{INSTALL_DIR}
make
make DESTDIR=$RPM_BUILD_ROOT install
#check to make sure this works
#make DESTDIR=$RPM_BUILD_ROOT install
## Install Steps End
#------------------------------------------------

#cp -R ./bowtie2* ./doc ./scripts $RPM_BUILD_ROOT/%{INSTALL_DIR}
#this may not be necesary if you can do make install as above
#cp ./src/program/exonerate $RPM_BUILD_ROOT/%{INSTALL_DIR}    
#cp -R ./doc $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -R ./test $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{name}
distribution. Documentation can be found online at https://github.com/hotdogee/exonerate-gff3

Version %{version}

]])

whatis("Name: exonerate-gff3")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: https://github.com/hotdogee/exonerate-gff3")
whatis("Description: exonerate fork with added gff3 support ")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
prepend_path("PATH"       ,"%{INSTALL_DIR}/bin")

prereq("perl")

EOF
## Modulefile End
#------------------------------------------------

## Lua syntax check
if [ -f $SPEC_DIR/checkModuleSyntax ]; then
    $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

##  VERSION FILE
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
#%files -n %{name}-%{comp_fam_ver}
%files 

# Define files permisions, user and group
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

