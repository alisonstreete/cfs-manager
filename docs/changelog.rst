**********
Change Log
**********

This is where all inter-version changes in the CFS_Manager project will be noted. All changes noted here will be in summary form. If you're reading this on *readthedocs*, you can do a full-text search to get more details.

1.x Series
==========

1.1.0.1
-------

*Bugfixes:*

* Setuptools incorrectly packaged the files which were uploaded to PyPI, so they had to be re-uploaded. This should really not be considered a distinct version from 1.1.0, and is only a thing because of an upload error.

1.1.0
-----

*Bugfixes:*

* The documentation correctly ships with the PyPI package.

* GDrive no longer breaks when CFS_Manager is installed from PyPI.

* Large Dropbox uploads no longer cause crashes.

*New Functionality:*

* Added filename autocompletion option.

* Enabled the 'cfs-config' system command for the configuration flow.

* Enabled the 'cfs-watch' system command to add the current directory to the set of managed directories.

*User Interface Improvements:*

* Added a list of command options to the CLI command listing.

1.0.1
-----

*Bugfixes:*

* CLI tools are functional even if there's no managed.txt yet.

1.0.0
-----

(Nothing - initial release)