if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
fi

if [ -n "$MODULEPATH" ]; then
  module --quiet purge
  clearMT
  module load TACC
fi

export MODULEPATH=/opt/apps/xsede/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
