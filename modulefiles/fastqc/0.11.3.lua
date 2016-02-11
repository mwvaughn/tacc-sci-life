help (
[[
This module loads fastqc built with %{comp_fam}.
Documentation for fastqc is available online at http://www.bioinformatics.babraham.ac.uk/projects/fastqc
The executables are added on to path

Version 0.11.3

]])

whatis("Name: fastqc")
whatis("Version: 0.11.3")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Sequencing, FastQ, Quality Control")
whatis("Description: fastqc - A Quality Control application for FastQ files")
whatis("URL: http://www.bioinformatics.babraham.ac.uk/projects/fastqc")

setenv("TACC_FASTQC_DIR","/tmprpm/fastqc/0.11.3/")
prepend_path("PATH"       ,"/tmprpm/fastqc/0.11.3")

