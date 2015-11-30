# Support for the lmod system
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  clearMT
  export MODULEPATH=/opt/apps/modulefiles:/opt/cray/modulefiles:/opt/cray/ari/modulefiles:/opt/cray/craype/default/modulefiles:/opt/modulefiles:$WORK/rpmbuild/SPECS/modulefiles/ls5
  module load TACC_lsc
  module purge
  module load TACC_lsc
fi
