# -*-rpm-spec-*-
#
#-----------------------------------------
# Compiler Designations for TACC Clusters
#-----------------------------------------

%define comp_fam error

%if "%{is_intel11}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel11
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel
%endif

%if "%{is_gcc44}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_4
  %define comp_fam_name GNU
  %define comp_module gcc/4.4.5
%endif

%if "%{is_gcc47}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_7
  %define comp_fam_name GNU
  %define comp_module gcc/4.7.1
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  #exit
%endif
