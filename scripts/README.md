# Module support scripts

These scripts are designed to support LMOD module development and useage.

## moveRpm

Copies RPMs to standard admin directories and presents you with rpm install commands for use on TACC Collab.

```
Usage: moveRpm RPM [RPM ...]
```

## buildAll

Get your tokens ready, because the `buildAll` accepts spec files as arguments and hops to each machine in the `systemList` array to natively build the software package. After the rpm is sucessfully built, `buildAll` will copy it to the standard RPM directory on that system. After iterating through each system and spec file, a list of installation commands will also be printed, which can then be pasted into the "Software Install" requests on collab.

```
Usage: buildAll A.spec [B.spec] [...]
```

## buildDirectories.sh

Builds or updates `rpmbuild` directory in the specified path. These directories need to be created before any RPMs can be built.

```
Usage: buildDirectories.sh PATH
```

## myRpmInstall

Installs a TACC RPM into a local directory, changes all original paths to reflect the local path, and sets up an LMOD directory structure.

```
Usage: myRpmInstall <prefix> <file.rpm>

$ rpmbuild -bb test.spec
$ scripts/myRpmInstall $HOME/apps test.rpm
$ module use $HOME/apps/modulefiles
$ module load test
```

## queryBioModules.py

Tabulates all modules with the "biology" keyword across all TACC systems. The results can be printed as either a

* tab - easy to read and importable
* csv - importable
* pretty - easy to read

```
usage: queryBioModules.py [-h] [-S LIST] [-O TYPE]

optional arguments:
  -h, --help  show this help message and exit
  -S LIST     Systems to query [stampede,ls5,wrangler,login-
              knl1.stampede,hikari]
  -O TYPE     Output format ([csv], tab, pretty)
```
