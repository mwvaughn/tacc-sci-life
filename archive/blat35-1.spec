# $Id$

Summary:   BLAT: BLAST like alignment tool
Name:      blat
Version:   35
Release:   1
License:   freely distributable
Group: Applications/Life Sciences
Source0:   blatSrc35.zip
Packager:  jfonner@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME blat
%include ../system-defines.inc

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_BLAT

%description
BLAST like alignment tool

%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n blatSrc

%build

%install

%include ../system-load.inc

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc

# I'm using the old gcc here.  The make file has -Wall and -Werror
# on, so I'll have to edit the makefile for it to work with the newer 
# gcc.  I think we should wait until we have a test system, and then 
# look at performance changes from changing the compiler.  This at 
# least makes the tool available.

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
make BINDIR=$RPM_BUILD_ROOT/%{INSTALL_DIR} MACHTYPE=x86_64 
# L="$L -Wl,-Bdynamic -L/usr/lib64 -lpng -Wl,-Bstatic"



#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module adds the variable %{MODULE_VAR}_DIR to your environment.
This directory contains the following executables:
blat
faToNib
faToTwoBit
gfClient
gfServer
nibFrag
pslPretty
pslReps
pslSort
twoBitInfo
twoBitToFa

Documentation is available online here: 
http://genome.ucsc.edu/goldenPath/help/blatSpec.html

Version %{version}
]]
)

whatis("Name: blat")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics ")
whatis("Keywords: Biology, Blast, Genomics")
whatis("URL: http://users.soe.ucsc.edu/~kent/src/")
whatis("Description: BLAST like alignment tool")


prepend_path("PATH",              "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

EOF

#--------------
#  Version file. 
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
