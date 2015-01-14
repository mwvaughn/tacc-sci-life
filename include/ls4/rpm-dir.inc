# -*-rpm-spec-*-
#
#-------------------------------------------------------------------
# Define local build root and top level dir for rpm builds
#-------------------------------------------------------------------
# if you don't have a SPECS directory, this won't work

Buildroot: %(echo ${PWD%SPECS*})/tmp/%{name}-%{version}-buildroot
%define _topdir %(echo ${PWD%SPECS*})

%define defined()      %{expand:%%{?%{1}:1}%%{!?%{1}:0}}
%define undefined()    %{expand:%%{?%{1}:0}%%{!?%{1}:1}}

