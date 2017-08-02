Summary:    iRODS is a open source data management software
Name:       irods
Version:    4.2.1
Release:    2%{?dist}
License:    GPLv2
Vendor:     irods Consortium
Group:      DMC
Packager:   TACC - siva@tacc.utexas.edu
Prefix:     /opt/apps

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%define PNAME irods
%define MODULE_VAR	TACC_IRODS
%define INSTALL_DIR	/opt/apps/%{PNAME}/%{version}
%define MODULE_DIR	/opt/apps/modulefiles/%{PNAME}

%description
The Integrated Rule-Oriented Data System (iRODS) is open source data management software used by research organizations and government agencies worldwide.
iRODS is released as a production-level distribution aimed at deployment in mission critical environments.


%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
#%setup -n %{PNAME}.%{version}-centos_linux64

## BUILD
%build
#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
irods Icommands provides icommands required to access the datastore

Version %{version}
]])

setenv("IRODS_IMG", "/scratch/03076/gzynda/irods.img")

set_alias("ibun","singularity exec ${IRODS_IMG} ibun")
set_alias("icd","singularity exec ${IRODS_IMG} icd")
set_alias("ichksum","singularity exec ${IRODS_IMG} ichksum")
set_alias("ichmod","singularity exec ${IRODS_IMG} ichmod")
set_alias("icp","singularity exec ${IRODS_IMG} icp")
set_alias("ienv","singularity exec ${IRODS_IMG} ienv")
set_alias("iexecmd","singularity exec ${IRODS_IMG} iexecmd")
set_alias("iexit","singularity exec ${IRODS_IMG} iexit")
set_alias("ifsck","singularity exec ${IRODS_IMG} ifsck")
set_alias("iget","singularity exec ${IRODS_IMG} iget")
set_alias("ihelp","singularity exec ${IRODS_IMG} ihelp")
set_alias("iinit","singularity exec ${IRODS_IMG} iinit")
set_alias("ils","singularity exec ${IRODS_IMG} ils")
set_alias("ilsresc","singularity exec ${IRODS_IMG} ilsresc")
set_alias("imcoll","singularity exec ${IRODS_IMG} imcoll")
set_alias("imiscsvrinfo","singularity exec ${IRODS_IMG} imisc")
set_alias("imkdir","singularity exec ${IRODS_IMG} imkdir")
set_alias("imv","singularity exec ${IRODS_IMG} imv")
set_alias("ipasswd","singularity exec ${IRODS_IMG} ipasswd")
set_alias("iphybun","singularity exec ${IRODS_IMG} iphybun")
set_alias("iphymv","singularity exec ${IRODS_IMG} iphymv")
set_alias("ips","singularity exec ${IRODS_IMG} ips")
set_alias("iput","singularity exec ${IRODS_IMG} iput")
set_alias("ipwd","singularity exec ${IRODS_IMG} ipwd")
set_alias("iqdel","singularity exec ${IRODS_IMG} iqdel")
set_alias("iqmod","singularity exec ${IRODS_IMG} iqmod")
set_alias("iqstat","singularity exec ${IRODS_IMG} iqstat")
set_alias("iquest","singularity exec ${IRODS_IMG} iquest")
set_alias("iquota","singularity exec ${IRODS_IMG} iquota")
set_alias("ireg","singularity exec ${IRODS_IMG} ireg")
set_alias("irepl","singularity exec ${IRODS_IMG} irepl")
set_alias("irm","singularity exec ${IRODS_IMG} irm")
set_alias("irmtrash","singularity exec ${IRODS_IMG} irmtrash")
set_alias("irsync","singularity exec ${IRODS_IMG} irsync")
set_alias("irule","singularity exec ${IRODS_IMG} irule")
set_alias("iscan","singularity exec ${IRODS_IMG} iscan")
set_alias("isysmeta","singularity exec ${IRODS_IMG} isysmeta")
set_alias("itrim","singularity exec ${IRODS_IMG} itrim")
set_alias("iuserinfo","singularity exec ${IRODS_IMG} iuserinfo")
set_alias("ixmsg","singularity exec ${IRODS_IMG} ixmsg")
set_alias("izonereport","singularity exec ${IRODS_IMG} izonereport")

always_load("tacc-singularity/2.3.1")
EOF

## Modulefile End
#--------------------------------------
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << ‘EOF’
#%Module1.0####################################################################
##
## Version file for R version %{version}
##
set ModulesVersion “%version”
EOF

#----------------------------------------------------------
# Lua syntax check 
#----------------------------------------------------------
if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
    $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files
%defattr(-,root,install)
%{MODULE_DIR}

%post

%clean
