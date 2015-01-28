Overview
========
The Life Sciences Computing group at the Texas Advanced Computing Center (TACC) uses this repository to build modules for TACC's supercomputing systems

Older modules are in the "archive" directory.  The "scripts" directory contains helpful utility scripts.  The "include" directory contains system specific information that gets loaded during the RPM build process. SPEC files follow a specific naming convention to keep track of the version and revision information.  In general, new revisions are made because the previous version of the SPEC file contained an error (or in the case of Amber, the app updates itself with bugfixes as part of the build process).  The naming convention follows this pattern:

<application name>-<major version>.<minor version>.<patch>-<spec revision number>.spec

