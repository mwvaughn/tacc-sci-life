#!/bin/bash
#This script moves the data directories of freesurfer to the datadir on scratch.
#newgrp G-800657
FREESURFER_DATADIR="/scratch/projects/tacc/bio/freesurfer/5.3.0"
UNZIP="freesurfer"
echo ${FREESURFER_DATADIR}

if [ ! -d "$FREESURFER_DATADIR" ];
then
    echo "Directory $FREESURFER_DATADIR does not exist. Creating directory.."
    mkdir -p $FREESURFER_DATADIR
    echo "Directory $FREESURFER_DATADIR created"
else
    rm -fr ${FREESURFER_DATADIR}/*
fi

FILE="../../SOURCES/freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0.tar.gz"
if [ -f $FILE ];
then
    rm $UNZIP
    echo "Unzipping source file."
    tar xvf ../../SOURCES/$UNZIP-Linux-centos6_x86_64-stable-pub-v5.3.0.tar.gz
    echo "Copying data directories to  ${FREESURFER_DATADIR}"
    cd $UNZIP
    cp -r average subjects trctrain ${FREESURFER_DATADIR}/
    chgrp -R G-800657 ${FREESURFER_DATADIR}
    chmod -R 775 ${FREESURFER_DATADIR}
    echo "Permission changed."
    cd ..
    echo "Deleting unzipped files"
    rm -fr $UNZIP
    echo "Done!"
else
    echo "File $FILE does not exist. Quiting.."
    exit 1
fi
 
