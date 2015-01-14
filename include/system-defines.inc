%define APPS    /opt/apps
%define MODULES  modulefiles
%define debug_package %{nil}
%define system linux
%define PLATFORM %(hostname | awk -F. '{print $2}')
%define MODULE_VAR_PREFIX TACC_
