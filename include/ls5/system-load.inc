# Support for the lmod system
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
fi

if [ -n "$MODULEPATH" ]; then
  module purge
  clearMT
  #  export MODULEPATH=/opt/apps/modulefiles:/opt/cray/modulefiles:/opt/cray/ari/modulefiles:/opt/cray/craype/default/modulefiles:/opt/modulefiles
  export MODULEPATH=/opt/apps/modulefiles:/opt/apps/tools/modulefiles
fi

module load TACC
