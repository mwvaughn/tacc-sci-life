LS5 Workflow
============

Lonestar5 does not at present export WORK or SCRATCH environment variables. Include the following at the end of your .bashrc file

```
export WORK="/work/$(echo $HOME | awk -F '/' '{print $3}')/$USER"
export SCRATCH="/scratch/$(echo $HOME | awk -F '/' '{print $3}')/$USER"
```

Now, the workflow. You may already have the beginning of this in place, but it's OK to re-run just to be sure.

```
$ cd $WORK
$ mkdir -p rpmbuild && cd rpmbuild
$ git clone https://github.com/mwvaughn/tacc-sci-life.git SPECS
Cloning into 'SPECS'...

$ cd SPECS

# now build the directory structure
$ ./scripts/buildDirectories.sh
```

