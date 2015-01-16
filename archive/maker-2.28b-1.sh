#!/bin/bash
#This script installs the external softwares required by Maker-2.28b to datadir on scratch

MAKER_DATADIR="/scratch/projects/tacc/bio/maker/2.28b"
if [ ! -d "$MAKER_DATADIR" ];
then
    echo "Directory $MAKER_DATADIR does not exist. Creating directory.."
    mkdir -p $MAKER_DATADIR
    echo "Directory $MAKER_DATADIR created"
else
    rm -fr ${MAKER_DATADIR}/*
fi
cd ${MAKER_DATADIR}
echo "Downloading RepeatMasker..."
wget http://www.repeatmasker.org/RepeatMasker-open-3-3-0-p1.tar.gz
echo "RepeatMasker downloaded."
echo "Unpacking RepeatMasker..."
tar xvf RepeatMasker-open-3-3-0-p1.tar.gz
cd RepeatMasker
echo "Downloading RepBase..."
wget --user=nasridine --password="ylt993" http://www.girinst.org/server/RepBase/protected/repeatmaskerlibraries/repeatmaskerlibraries-20130422.tar.gz
echo "Unpacking RepBase..."
tar xvf repeatmaskerlibraries-20130422.tar.gz
echo "Downloading trf..."
wget http://tandem.bu.edu/trf/downloads/trf404.linux64
mv trf404.linux64 trf
chmod 755 trf
echo "Downloading rmblast..."
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/rmblast/2.2.27/rmblast-2.2.27-x64-linux.tar.gz
echo "Unpacking rmblast..."
tar xvf rmblast-2.2.27-x64-linux.tar.gz
mv rmblast-2.2.27 rmblast
cd ..
echo "Downloading blast..."
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.27/ncbi-blast-2.2.27+-x64-linux.tar.gz
echo "Unpacking blast..."
tar xvf ncbi-blast-2.2.27+-x64-linux.tar.gz
mv ncbi-blast-2.2.27+ blast
cp -r blast/* RepeatMasker/rmblast/
echo "Configuring RepeatMasker..."
cd RepeatMasker
perl ./configure << EOF



/scratch/projects/tacc/bio/maker/2.28b/RepeatMasker/
2
/scratch/projects/tacc/bio/maker/2.28b/RepeatMasker/rmblast/bin/
Y
5
EOF

cd ..
echo "Downloading Augustus..."
wget http://bioinf.uni-greifswald.de/augustus/binaries/augustus.2.6.1.tar.gz
echo "Unpacking Augustus..."
mkdir augustus
tar xvf augustus.2.6.1.tar.gz -C augustus
cd augustus/src
echo "Configuring Augustus..."
make

cd ../../
echo "Downloading Snap..."
wget http://korflab.ucdavis.edu/Software/snap-2012-05-17.tar.gz
echo "Unpacking Snap..."
tar xvf snap-2012-05-17.tar.gz
cd snap
echo "Configuring Snap..."
make

cd ../
echo "Downloading Exonerate..."
wget http://www.ebi.ac.uk/~guy/exonerate/exonerate-2.2.0-x86_64.tar.gz
echo "Unpacking Exonerate..."
tar xvf exonerate-2.2.0-x86_64.tar.gz
mv exonerate-2.2.0-x86_64 exonerate

echo "Deleting download files..."
rm *.tar.gz
echo "Changing folder permissions (755)..."
echo "Ownership(root) and group(G-800657) will be changed manually as root"
