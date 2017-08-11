%define debug_package		%{nil}
%define dbg                     %{nil}
%define system			linux
%define PLATFORM		%( echo $TACC_SYSTEM )

%define MODULE_VAR_PREFIX	TACC_
%define MODULE_VAR		%{MODULE_VAR_PREFIX}%(echo "%{pkg_base_name}" | tr [:lower:] [:upper:] | head -c 8 )
