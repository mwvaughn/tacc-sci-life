%define debug_package %{nil}
%define system linux
%define PLATFORM %( echo $TACC_SYSTEM )

%define MODULE_VAR_PREFIX TACC_

Prefix: /opt/apps
