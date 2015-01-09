#!/bin/bash
DATAFILES=("G4NDL.4.2.tar.gz" "G4NDL4.2.TS.tar.gz" "G4EMLOW.6.32.tar.gz" "G4NEUTRONXS.1.2.tar.gz" "G4PII.1.3.tar.gz" "G4PhotonEvaporation.2.3.tar.gz" "G4RadioactiveDecay.3.6.tar.gz" "G4SAIDDATA.1.1.tar.gz" "RealSurface.1.0.tar.gz")
cd ../../SOURCES

for FILE in ${DATAFILES[*]};
do
  echo $FILE
done
