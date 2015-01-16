Several folders consists of big files are moved out to TACC_FREESURFER_DATADIR (/scratch/projects/tacc/bio/freesurfer/1

1. average 
2. subjects
3. trctrain

Symlinks are created inside the module directory. 

Bash script freesurfer-5.3.0-1.sh needs to run before rpmbuild which moves all the data files to scratch and change the ownship to compbio group (G-800657) 
