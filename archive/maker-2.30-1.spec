#export RPM_BUILD_DIR=/home1/0000/build/rpms/
Summary:    maker -- a portable and easy to configure genome annotation pipeline
Name:       maker
Version:    2.30
Release:    1
License:    GNU General Public License
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
%include ../system-defines.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define PNAME maker

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
MAKER is a portable and easily configurable genome annotation pipeline. It's purpose is to allow smaller eukaryotic and prokaryotic genome projects to independently annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab-initio gene predictions and automatically synthesizes these data into gene annotations having evidence-based quality values. 
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_MAKER
%define MAKER_DATADIR /scratch/projects/tacc/bio/%{name}/2.28b
#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

if [ ! -d "%{MAKER_DATADIR}" ]; then
    echo "The data directory %{MAKER_DATADIR} was not found. Aborting rpmbuild."
    exit 1
fi
if [ ! -d "%{MAKER_DATADIR}/RepeatMasker" ]; then
    echo "RepeatMasker is missing from %{MAKER_DATADIR}. Aborting rpmbuild."
    exit 1
fi
if [ ! -d "%{MAKER_DATADIR}/RepeatMasker/rmblast" ]; then
    echo "rmblast is missing from RepeatMasker. Aborting rpmbuild."
    exit 1
fi
if [ ! -d "%{MAKER_DATADIR}/blast" ]; then
    echo "ncbi-blast is missing from %{MAKER_DATADIR}. Aborting rpmbuild."
    exit 1
fi
if [ ! -d "%{MAKER_DATADIR}/augustus" ]; then
    echo "Augustus is missing from %{MAKER_DATADIR}. Aborting rpmbuild."
    exit 1
fi
if [ ! -d "%{MAKER_DATADIR}/snap" ]; then
    echo "snap is missing from %{MAKER_DATADIR}. Aborting rpmbuild."
    exit 1
fi
if [ ! -d "%{MAKER_DATADIR}/exonerate" ]; then
    echo "exonerate is missing from %{MAKER_DATADIR}. Aborting rpmbuild."
    exit 1
fi

#chown -R root:G-800657 %{MAKER_DATADIR}/
#chmod -R 755 %{MAKER_DATADIR}

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}-%{version}

%build   
%install
%include ../system-load.inc          
    
# Load additional modules here (as needed)
module purge 
module load TACC
module swap mvapich2 openmpi

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
/opt/apps/intel11_1/openmpi/1.4.3/bin/mpicc
/opt/apps/intel11_1/openmpi/1.4.3/include
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
n
a
n
Y
EOF
./Build install

cd $CWD
cp -R ./bin ./data ./GMOD ./lib ./LICENSE ./MWAS ./perl ./README $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
A portable and easy to configure genome annotation pipeline. MAKER allows smaller eukaryotic genome projects and prokaryotic genome projects to annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab initio gene predictions and automatically synthesizes these data into gene annotations with evidence-based quality values. MAKER is also easily trainable: outputs of preliminary runs can be used to automatically retrain its gene prediction algorithm, producing higher quality gene-models on subsequent runs. MAKER's inputs are minimal. Its outputs are in GFF3 or FASTA format, and can be directly loaded into Chado, GBrowse, JBrowse or Apollo. Documentation can be found at http://gmod.org/wiki/MAKER.

Version %{version}
]])

whatis("Name: maker")
whatis("Version: %{version}")
whatis("Category: Biology, sequencing")
whatis("Keywords:  Genome, Sequencing, Annotation")
whatis("Description: Maker - a portable and easily configurable genome annotation pipeline.") 
whatis("http://www.yandell-lab.org/software/maker.html")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
prepend_path("PATH",              "%{INSTALL_DIR}/pgsql/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
prepend_path("LD_PRELOAD",              "/opt/apps/intel11_1/openmpi/1.4.3/lib/libmpi.so")
setenv ( "OMPI_MCA_mpi_warn_on_fork",    "0")
setenv ( "TACC_MAKER_DATADIR",      "/scratch/projects/tacc/bio/%{name}/2.28b")
prepend_path("PATH",         "%{MAKER_DATADIR}/RepeatMasker")
prepend_path("PATH",         "%{MAKER_DATADIR}/RepeatMasker/rmblast/bin")
prepend_path("PATH",         "%{MAKER_DATADIR}/blast/bin")
setenv ("AUGUSTUS_CONFIG_PATH",     "%{MAKER_DATADIR}/augustus/config")
prepend_path("PATH",         "%{MAKER_DATADIR}/augustus/bin")
prepend_path("PATH",         "%{MAKER_DATADIR}/snap")
setenv ("ZOE",        "%{MAKER_DATADIR}/snap")
prepend_path("PATH",         "%{MAKER_DATADIR}/exonerate/bin")
prereq("openmpi")

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

