#export RPM_BUILD_DIR=/admin/build/admin/rpms/stampede/
Summary: FreeSurfer - a set of tools for analysis and visualization of structural and functional brain imaging data. 
Name:	freesurfer
Version:  5.3.0
Release:   3	
Group:	Applications/Life Sceinces
License:  MGH
Source: freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0.tar.gz 
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc

%include ../system-defines.inc
%define PNAME freesurfer
#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
FreeSurfer is a set of tools for analysis and visualization of structural and functional brain imaging data. FreeSurfer contains a fully automatic structural imaging stream for processing cross sectional and longitudinal data.

FreeSurfer provides many anatomical analysis tools, including: representation of the cortical surface between white and gray matter, representation of the pial surface, segmentation of white matter from the rest of the brain, skull stripping, B1 bias field correction, nonlinear registration of the cortical surface of an individual with a stereotaxic atlas, labeling of regions of the cortical surface, statistical analysis of group morphometry differences, and labeling of subcortical brain structures and much more ...
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_FREESURFER
#big data dir
%define TACC_FREESURFER_DATADIR /scratch/projects/tacc/bio/%{name}/%{version}
#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

if [ ! -d "%{TACC_FREESURFER_DATADIR}" ]; then
    echo "The data directory %{TACC_FREESURFER_DATADIR} was not found. Aborting rpmbuild."
    exit 1
fi

rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n freesurfer

%build

%install

%include ../system-load.inc

module purge
module load TACC

mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

#which direcotires are needed for precompiled version, chimeraext, python?
#Syntax error, chimeraext/FilterKit/Filter.py

cp -R ASegStatsLUT.txt AUTHORS bin build-stamp.txt data DefectLUT.txt diffusion docs FreeSurferColorLUT.txt fsafd fsfast lib LICENSE matlab mni NOTICE README SegmentNoLUT.txt sessions Simple_surface_labels2009.txt tkmeditParcColorsCMA tktools $RPM_BUILD_ROOT/%{INSTALL_DIR}
ln -s %{TACC_FREESURFER_DATADIR}/average $RPM_BUILD_ROOT/%{INSTALL_DIR}/average
ln -s %{TACC_FREESURFER_DATADIR}/subjects $RPM_BUILD_ROOT/%{INSTALL_DIR}/subjects
ln -s %{TACC_FREESURFER_DATADIR}/trctrain $RPM_BUILD_ROOT/%{INSTALL_DIR}/trctrain
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/.license << 'EOF'
jiao@tacc.utexas.edu
13706
*CpqVQL31xgFA
EOF

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help ( 
[[
This module loads %{name}. This module makes available the %{name} executables. Documentation for %{name} is available online at the publisher\'s website: http://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferWiki 
These executables can be found in %{MODULE_VAR}_DIR, e.g. recon-all. Need to run SetUpFreeSurfer.sh before running anything.

Version %{version}
]])

whatis("Name: FreeSurfer")
whatis("Version: %{version}")
whatis("Category: computational biology, Imaging")
whatis("Keywords:  Biology, fMRI, Reconstruction")
whatis("Description: freesurfer - a set of tools for analysis and visualization of structural and functional brain imaging data. Common commands include recon-all, etc.") 
whatis("URL: http://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferWiki")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv (     "TACC_FREESURFER_DATADIR",     "/scratch/projects/tacc/bio/%{name}/%{version}")
setenv (     "FREESURFER_HOME",           "%{INSTALL_DIR}")
setenv (     "SUBJECTS_DIR",    "%{INSTALL_DIR}/subjects") 
setenv (     "MNI_DIR",         "%{INSTALL_DIR}/mni")
setenv (     "FSFAST_HOME",     "%{INSTALL_DIR}/fsfast")
setenv (     "FSF_OUTPUT_FORMAT", "nii")
prepend_path("PATH",              "%{INSTALL_DIR}/mni/bin")
prepend_path("PERL5LIB",    "%{INSTALL_DIR}/mni/lib/perl5/5.8.5")

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
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

