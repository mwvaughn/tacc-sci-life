# Support for the lmod system
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi
