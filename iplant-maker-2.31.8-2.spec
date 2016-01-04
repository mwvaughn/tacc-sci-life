# http://www.yandell-lab.org/software/maker-p.html
Name:       iplant_maker
Version:    2.31.8
Release:    2
License:    Perl Artistic License 2.0
Group: Applications/Life Sciences
Source:     maker-%{version}.tgz
Packager:   TACC - vaughn@tacc.utexas.edu
Summary:    A portable and easy-to-configure genome annotation pipeline
#Prefix: /opt/apps

# Build using build_rpm.sh --intel=14 --mvapich2=2_0 maker-version.spec

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc
## Compiler Family Definitions
%include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
%include ./include/%{PLATFORM}/mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR  %{MODULE_VAR_PREFIX}MAKER
%define PNAME       iplant_maker

# Maker is a special module. It comes bundled with a lot of
# reference data used in the annotation. That data is maintained
# on a shared directory. To ensure this policy, later on in the
# spec, an error is thrown if the data directory is not found
%define MAKER_DATADIR /scratch/projects/tacc/bio/maker/%{version}

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
%package -n iplant_maker-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: A portable and easy to configure genome annotation pipeline
Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n iplant_maker-%{comp_fam_ver}-%{mpi_fam_ver}
MAKER is a portable and easily configurable genome annotation pipeline. It's purpose is to allow smaller eukaryotic and prokaryotic genome projects to independently annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab-initio gene predictions and automatically synthesizes these data into gene annotations having evidence-based quality values.

## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# for DIR in "" RepeatMasker RepeatMasker/rmblast blast augustus snap exonerate
# do
#     if [ ! -d "%{MAKER_DATADIR}/${DIR}" ]; then
#         echo "%{MAKER_DATADIR}/${DIR} was not found. Aborting rpmbuild."
#         exit 1
#     fi
# done

## SETUP
%setup -n maker

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
module load perl/5.16.2
module swap $TACC_FAMILY_COMPILER intel/14.0.1.106

CWD=`pwd`

cd ./src
cpan << EOF
o conf init
yes







follow




















4
4


quit
EOF

perl Build.PL << EOF
y
$MPICH_HOME/bin/mpicc
$MPICH_HOME/include
EOF

./Build installdeps << EOF
y
y
n
a
n
Y
EOF
rm -f ../perl/lib/Carp/Heavy.pm
./Build installdeps << EOF
y
Y
EOF

./Build install
## Install Steps End
#------------------------------------------------

cd $CWD
cp -R ./bin ./data ./GMOD ./lib ./LICENSE ./MWAS ./perl ./README $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#------------------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
A portable and easy to configure genome annotation pipeline. MAKER allows smaller eukaryotic genome projects and prokaryotic genome projects to annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab initio gene predictions and automatically synthesizes these data into gene annotations with evidence-based quality values. MAKER is also easily trainable: outputs of preliminary runs can be used to automatically retrain its gene prediction algorithm, producing higher quality gene-models on subsequent runs. MAKER's inputs are minimal. Its outputs are in GFF3 or FASTA format, and can be directly loaded into Chado, GBrowse, JBrowse or Apollo. Documentation can be found at http://gmod.org/wiki/MAKER.

Version %{version}
]])

whatis("Name: iplant_maker")
whatis("Version: %{version}")
whatis("Category: Biology, sequencing")
whatis("Keywords:  Genome, Sequencing, Annotation")
whatis("Description: Maker - a portable and easily configurable genome annotation pipeline.")
whatis("http://www.yandell-lab.org/software/maker.html")

append_path("PATH",              "%{INSTALL_DIR}/bin")
append_path("PATH",              "%{INSTALL_DIR}/pgsql/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv ( "TACC_MAKER_DATADIR",      "%{MAKER_DATADIR}")
append_path("PATH",         "%{MAKER_DATADIR}/RepeatMasker")
append_path("PATH",         "%{MAKER_DATADIR}/RepeatMasker/rmblast/bin")
append_path("PATH",         "%{MAKER_DATADIR}/blast/bin")
setenv ("AUGUSTUS_CONFIG_PATH",     "%{MAKER_DATADIR}/augustus/config")
append_path("PATH",         "%{MAKER_DATADIR}/augustus/bin")
append_path("PATH",         "%{MAKER_DATADIR}/snap")
setenv ("ZOE",        "%{MAKER_DATADIR}/snap/Zoe")
append_path("PATH",         "%{MAKER_DATADIR}/exonerate/bin")
prereq("perl/5.16.2")

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
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF



#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n iplant_maker-%{comp_fam_ver}-%{mpi_fam_ver}

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

