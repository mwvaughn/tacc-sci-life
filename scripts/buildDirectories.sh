#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

usage="Usage: $0 <dir> \n Builds an \"rpmbuild\" directory in the path you specify and a set of system subdirectories below that."

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo $usage
    exit 0
fi

if [ $# -gt 1 ]; then
    echo "Error: Too many arguments."
    echo $usage
    exit 1
fi

if [ $# -eq 1 ]; then
    baseDir=$1
else
    baseDir=$PWD
fi

if [[ "$baseDir" =~ .*rpmbuild.* ]]; then
    echo "An rpmbuild directory already exists here:"
    rpmbuildPath="${baseDir%rpmbuild*}rpmbuild"
    echo "$rpmbuildPath"
    echo
    echo "Would you like to have the directory tree under this existing directory? (y/n) [n]"
    read userInput
    if [ "$userInput" == "y" ] || [ "$userInput" == "Y" ]; then
        baseDir=${baseDir%rpmbuild*}
    fi
else
    echo "Build directory tree in the current directory? (y/n)[n] "
    read userInput
    if [ "$userInput" != "y" ] && [ "$userInput" != "Y" ]; then
        echo "Exiting..."
        echo
        echo $usage
        exit 0
    fi
fi

if [ ! -d $baseDir ]; then
    echo "Creating directory: $baseDir"
    mkdir -p $baseDir
    if [ $? -ne 0 ] ; then
        echo "It looks like the directory $baseDir could not be created. Exiting..."
        exit 1
    fi
fi

# if ! [[ "$scriptPath" =~ .*rpmbuild.* ]]; then
#     echo "The script is running from the path $scriptPath"
#     echo "To setup directories, you need this script to reside somewhere inside an "rpmbuild" directory."
#     echo "We recommend cloning the tacc-sci-life repository into a directory called SPECS like this:"
#     echo "git clone https://github.com/mwvaughn/tacc-sci-life.git SPECS"
#     echo "Please see README.md for more information"
#     exit 1
# fi

if [ ! -d "${baseDir}/rpmbuild" ]; then
    mkdir -p ${baseDir}/rpmbuild
fi
baseDir=${baseDir}/rpmbuild

# Use a shared source direcotry and
# link it to each system directory
[ -d $baseDir/SOURCES ] || mkdir -p $baseDir/SOURCES

echo "Creating rpmbuild heirarchy in the ${baseDir} directory."
for systemName in hikari ls5 stampede2 stampede maverick wrangler; do
    # Make system folder
    if [ ! -d $baseDir/$systemName ]; then
        echo "creating $systemName directory"
        mkdir -p $baseDir/$systemName
    fi
    # Link SOURCES
    if [ ! -d $baseDir/$systemName/SOURCES ]
    then
        echo "Linking $baseDir/SOURCES to $baseDIR/$systemName"
        ln -s $baseDir/SOURCES $baseDir/$systemName/SOURCES
    fi
    # Create build directories
    for subDir in BUILD RPMS SRPMS; do
        if [ ! -d $baseDir/$systemName/$subDir ]; then
            echo "creating $systemName/$subDir directory"
            mkdir -p $baseDir/$systemName/$subDir
        fi
    done
done

echo
echo "----------------------------------------------------------------------------"
echo "Finished creating directory heirarchy."
echo "To import TACC's Life Sciences Modules git repository, use this command:"
echo
echo "cd $baseDir && git clone https://github.com/mwvaughn/tacc-sci-life.git SPECS"
echo
echo "----------------------------------------------------------------------------"
echo

