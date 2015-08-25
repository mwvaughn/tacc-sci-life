Name: bowtie
Version: 2.2.5
Release: 3
License: GPL
Source:  http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.5/bowtie2-2.2.5-source.zip
Packager: TACC - jfonner@tacc.utexas.edu
Summary: Memory-efficient short read (NGS) aligner

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

%define MODULE_VAR  %{MODULE_VAR_PREFIX}BOWTIE
%define PNAME       bowtie

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

#------------------------------------------------
# THIS SECTION SHOULD BE CONSTANT
#------------------------------------------------
# Module macros
%define MODULE_PREFIX   /tmpmod 
%define MODULE_DIR      %{MODULE_PREFIX}/%{MODULE_SUFFIX}
# Let's get rid of MODULE_FILENAME.  Too fancy by half. It must always be <version>.lua
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

%package %{PACKAGE}
Summary: Memory-efficient short read (NGS) aligner
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary: Memory-efficient short read (NGS) aligner
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. It is particularly good at aligning reads of about 50 up to 100s or 1,000s of characters, and particularly good at aligning to relatively long (e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM Index to keep its memory footprint small: for the human genome, its memory footprint is typically around 3.2 GB. Bowtie 2 supports gapped, local, and paired-end alignment modes.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif

## SETUP
%setup -n %{PNAME}2-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

#--------------------------------------
%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    ########### Do Not Remove #############

#--------------------------------------
## Install Steps Start
module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc

# Since LDFLAGS is not used in bowtie's compilation, we hijack EXTRA_FLAGS to carry the rpath payload
make EXTRA_FLAGS="-Wl,-rpath,$GCC_LIB"
## Install Steps End
#--------------------------------------

    cp -R ./bowtie2* ./doc ./scripts $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif
#--------------------------------------

#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
%if %{?BUILD_MODULEFILE}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
    ########### Do Not Remove #############

#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{name}
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/bowtie2/

NOTE: Bowtie2 indexes are not backwards compatible with Bowtie1 indexes. 

This module provides the bowtie2, bowtie2-align, bowtie2-build, and bowtie2-inspect binaries + scripts

Version %{version}

]])

whatis("Name: Bowtie")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: http://bowtie-bio.sourceforge.net/bowtie2/")
whatis("Description: Ultrafast, memory-efficient short read aligner")

setenv("%{MODULE_VAR}_DIR",              %{INSTALL_DIR})
setenv("%{MODULE_VAR}_SCRIPTS", pathJoin(%{INSTALL_DIR},"scripts"))
prepend_path("PATH",                     %{INSTALL_DIR})

prereq("perl")

EOF
## Modulefile End
#--------------------------------------

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

%endif
#--------------------------------------

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
%defattr(-,root,install,)
%{INSTALL_DIR}
%endif # ?BUILD_PACKAGE

%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE}
%defattr(-,root,install,)
%{MODULE_DIR}
%endif # ?BUILD_MODULEFILE


%post %{PACKAGE}
R='\033[1;31m'
G='\033[1;32m'
B='\033[1;34m'
W='\033[0m'
NC='\033[0m'
F='\033[0m'
printf "${F}======================================================================${NC}\n"
printf "${F}||${B} TTTTTTTTTTTTTTT     AAAAA      ${W}    /@@@@@@@\        /@@@@@@@\    ${F}||${NC}\n"
printf "${F}||${B} TTTTTTTTTTTTTTT    /AAAAA\     ${W}  @@@@@@@@@@@@\    @@@@@@@@@@@@\  ${F}||${NC}\n"
printf "${F}||${B}      TTTTT        /AA/${W}A${B}\AA\    ${W} @@@@@/   \@@@@|  @@@@@/   \@@@@| ${F}||${NC}\n"
printf "${F}||${B}      TTTTT       /AA/${W}A@A${B}\AA\   ${W}|@@@@/      '''' |@@@@/      '''' ${F}||${NC}\n"
printf "${F}||${B}      TTTTT      ,${W}^V@@@@@@@V^${B},  ${R}|CCCC            |CCCC            ${F}||${NC}\n"
printf "${F}||${B}      TTTTT      AAAV${W}@@@@@${B}VAAA  ${R} CCCCC    ,CCCC|  CCCCC    ,CCCC| ${F}||${NC}\n"
printf "${F}||${B}      TTTTT     /AAV${W}|@/^\@|${B}VAA\ ${R}  CCCCCCCCCCCCC    CCCCCCCCCCCCC  ${F}||${NC}\n"
printf "${F}||${B}      TTTTT    /AAA|${W}/     \\\\${B}|AAA\\\\${R}    ^CCCCCCC^        ^CCCCCCC^    ${F}||${NC}\n"
printf "${F}======================================================================${NC}\n"

echo "This is the %{RPM_PACKAGE_NAME} subpackage postinstall script"
# Query rpm after installation for location of canary files ---------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                       # |
    export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                  # |
    export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                   # |
    echo "Using default RPM database path:                             %{_dbpath}"                                            # |
else                                                                                                                          # |
    export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)           # |
    export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)            # |
    echo "Using user-specified RPM database path:                      ${RPM_DBPATH}"                                         # |
fi                                                                                                                            # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")              # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                # |
# -------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
echo "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       "                       > /dev/stderr # |
echo "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      "                       > /dev/stderr # |
echo "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          "                       > /dev/stderr # |
echo "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         "                       > /dev/stderr # |
if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                      # |
    echo -e "${R}ERROR: POST_INSTALL_PREFIX is currently null or unset${NC}"                                      > /dev/stderr # |
    echo -e "${R}ERROR: tacc_install_canary was not found${NC}"                                                   > /dev/stderr # |
    echo -e "${R}ERROR: Something is not right. Exiting!${NC}"                                                    > /dev/stderr # |
    exit -1                                                                                                                     # |
else                                                                                                                            # |
    echo "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} "                   > /dev/stderr # |
    echo "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"  > /dev/stderr # |
fi                                                                                                                              # |
if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                       # |
    echo -e "${G}POST_MODULE_PREFIX is currently null or unset${NC}"                                              > /dev/stderr # |
    echo -e "${G}Has %{RPM_MODULEFILE_NAME} been installed in this rpm database yet?${NC}"                        > /dev/stderr # |
    echo -e "${G}Install %{RPM_MODULEFILE_NAME} to automatically update %{MODULE_SUFFIX}/%{version}.lua${NC}"     > /dev/stderr # |
else                                                                                                                            # |
    echo "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  "                   > /dev/stderr # |
    echo "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  "  > /dev/stderr # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
    echo "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       "                   > /dev/stderr # |
    echo "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         "                   > /dev/stderr # |
    sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{version}.lua                 # |
    sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{version}.lua                   # |
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                 # |
    cat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{version}.lua            | \
        GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
        GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                       > /dev/stderr # |
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                 # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------

%post %{MODULEFILE}
R='\033[1;31m'
G='\033[1;32m'
B='\033[1;34m'
W='\033[0m'
NC='\033[0m'
F='\033[0m'
printf "${F}======================================================================${NC}\n"
printf "${F}||${B} TTTTTTTTTTTTTTT     AAAAA      ${W}    /@@@@@@@\        /@@@@@@@\    ${F}||${NC}\n"
printf "${F}||${B} TTTTTTTTTTTTTTT    /AAAAA\     ${W}  @@@@@@@@@@@@\    @@@@@@@@@@@@\  ${F}||${NC}\n"
printf "${F}||${B}      TTTTT        /AA/${W}A${B}\AA\    ${W} @@@@@/   \@@@@|  @@@@@/   \@@@@| ${F}||${NC}\n"
printf "${F}||${B}      TTTTT       /AA/${W}A@A${B}\AA\   ${W}|@@@@/      '''' |@@@@/      '''' ${F}||${NC}\n"
printf "${F}||${B}      TTTTT      ,${W}^V@@@@@@@V^${B},  ${R}|CCCC            |CCCC            ${F}||${NC}\n"
printf "${F}||${B}      TTTTT      AAAV${W}@@@@@${B}VAAA  ${R} CCCCC    ,CCCC|  CCCCC    ,CCCC| ${F}||${NC}\n"
printf "${F}||${B}      TTTTT     /AAV${W}|@/^\@|${B}VAA\ ${R}  CCCCCCCCCCCCC    CCCCCCCCCCCCC  ${F}||${NC}\n"
printf "${F}||${B}      TTTTT    /AAA|${W}/     \\\\${B}|AAA\\\\${R}    ^CCCCCCC^        ^CCCCCCC^    ${F}||${NC}\n"
printf "${F}======================================================================${NC}\n"
echo "This is the %{RPM_MODULEFILE_NAME} subpackage postinstall script"
# Query rpm after installation for location of canary files ---------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                       # |
  export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                    # |
  export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                     # |
  echo "Using default RPM database path:                             %{_dbpath}"                                              # |
else                                                                                                                          # |
  export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)             # |
  export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)              # |
  echo "Using user-specified RPM database path:                      ${RPM_DBPATH}"                                           # |
fi                                                                                                                            # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")              # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                # |
# -------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
echo "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       "                       > /dev/stderr # |
echo "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      "                       > /dev/stderr # |
echo "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          "                       > /dev/stderr # |
echo "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         "                       > /dev/stderr # |
if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                      # |
  echo -e "${G}POST_INSTALL_PREFIX is set but null or unset${NC}"                                                 > /dev/stderr # |
  echo -e "${G}Has %{RPM_PACKAGE_NAME} been installed in this rpm database yet?${NC}"                             > /dev/stderr # |
  echo -e "${G}Install %{RPM_PACKAGE_NAME} to automatically update %{MODULE_SUFFIX}/%{version}.lua${NC}"          > /dev/stderr # |
else                                                                                                                            # |
  echo "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} "                     > /dev/stderr # |
  echo "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"    > /dev/stderr # |
fi                                                                                                                              # |
if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                       # |
  echo -e "${R}ERROR: POST_MODULE_PREFIX is currently set but null or unset"                                      > /dev/stderr # |
  echo -e "${R}ERROR: tacc_module_canary was not found"                                                           > /dev/stderr # |
  echo -e "${R}ERROR: Something is not right. Exiting!"                                                           > /dev/stderr # |
  exit -1                                                                                                                       # |
else                                                                                                                            # |
  echo "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  "                     > /dev/stderr # |
  echo "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  "    > /dev/stderr # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
  echo "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       "                     > /dev/stderr # |
  echo "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         "                     > /dev/stderr # |
  sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{version}.lua                   # |
  sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{version}.lua                     # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
  cat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{version}.lua            | \
      GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
      GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                         > /dev/stderr # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------



## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

