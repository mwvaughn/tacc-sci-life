#!/bin/bash

module load git

scriptPath=$( cd "$( dirname $0 )" && pwd )
if ! [[ "$scriptPath" =~ .*rpmbuild.* ]]; then 
    echo "The script is running from the path $scriptPath"
    echo "To setup directories, you need this script to reside somewhere inside an "rpmbuild" directory."
    echo "We recommend cloning the tacc-sci-life repository into a directory called SPECS like this:"
    echo "git clone https://github.com/mwvaughn/tacc-sci-life.git SPECS"
    echo "Please see README.md for more information"
    exit 1
fi

rpmbuildPath="${scriptPath%rpmbuild*}rpmbuild"
# echo $rpmbuildPath

for systemName in ls4 stampede maverick; do
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
