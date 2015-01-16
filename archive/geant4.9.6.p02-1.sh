#!/bin/bash
#This script moves the data directories of geant4 to the datadir on scratch.
#newgrp G-800657
GEANT4_DATADIR="/scratch/projects/tacc/bio/geant4/9.6.p02"

if [ ! -d "$GEANT4_DATADIR" ];
then
    echo "Directory $GEANT4_DATADIR does not exist. Creating directory.."
    mkdir -p $GEANT4_DATADIR
    echo "Directory $GEANT4_DATADIR created"
else
    rm -fr ${GEANT4_DATADIR}/*
fi

DATAFILES=("G4NDL.4.2.tar.gz" "G4NDL4.2.TS.tar.gz" "G4EMLOW.6.32.tar.gz" "G4NEUTRONXS.1.2.tar.gz" "G4PII.1.3.tar.gz" "G4PhotonEvaporation.2.3.tar.gz" "G4RadioactiveDecay.3.6.tar.gz" "G4SAIDDATA.1.1.tar.gz" "RealSurface.1.0.tar.gz")
cd ../../SOURCES

for FILE in ${DATAFILES[*]};
do
    if [ -f $FILE ];
    then
        echo "Unzipping source file."
        tar xvf $FILE
    else
        echo "File $FILE does not exist. Quiting.."
        exit 1
    fi
done
echo "Moving data files to  ${GEANT4_DATADIR}"
mv G4NDL4.2 G4EMLOW6.32 G4NEUTRONXS1.2 G4PII1.3 PhotonEvaporation2.3 RadioactiveDecay3.6 G4SAIDDATA1.1 RealSurface1.0 ${GEANT4_DATADIR}/
chmod -R 775 ${GEANT4_DATADIR}
 
