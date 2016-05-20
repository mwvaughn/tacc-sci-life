%define debug_package %{nil}
%define system linux
%define PLATFORM %(hostname -f | awk -F. '{if (substr($1,0,3) == "nid") print "ls5"; else print $2}')

%define MODULE_VAR_PREFIX TACC_

Prefix: /opt/apps
