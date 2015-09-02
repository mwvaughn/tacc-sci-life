#!/bin/bash

module load git

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

usage="Usage: $0 <dir>"

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
    echo "Build directory tree in the current directory? (y/n)[n] "
    read userInput
    if [ "$userInput" == "y" ] || [ "$userInput" == "Y" ]
        baseDir=$DIR
    else
        echo "Exiting..."
        exit 0
    fi
fi

if [ ! -d $baseDir ]; then
    echo "Creating directory: $baseDir"
fi


# if ! [[ "$scriptPath" =~ .*rpmbuild.* ]]; then 
#     echo "The script is running from the path $scriptPath"
#     echo "To setup directories, you need this script to reside somewhere inside an "rpmbuild" directory."
#     echo "We recommend cloning the tacc-sci-life repository into a directory called SPECS like this:"
#     echo "git clone https://github.com/mwvaughn/tacc-sci-life.git SPECS"
#     echo "Please see README.md for more information"
#     exit 1
# fi

rpmbuildPath=$baseDir
# echo $rpmbuildPath

for systemName in ls4 stampede maverick wrangler; do
    if [ ! -d $rpmbuildPath/$systemName ]; then
        echo "creating $systemName directory"
        mkdir -p $rpmbuildPath/$systemName
    fi    
    for subDir in BUILD RPMS SOURCES SRPMS; do
        if [ ! -d $rpmbuildPath/$systemName/$subDir ]; then
            echo "creating $systemName/$subDir directory"
            mkdir -p $rpmbuildPath/$systemName/$subDir
        fi
    done
done
