**********
Change Log
**********

This is where all inter-version changes in the CFS_Manager project will be noted. All changes noted here will be in summary form. If you're reading this on *readthedocs*, you can do a full-text search to get more details. This project follows `Semantic Versioning <http://semver.org/>`_.

1.x Series
==========

[Unreleased]
------------

*Performance Improvements*

* Added rudimentary support for caching downloaded files to speed up repeated downloads

*UI Improvements*

* Support for calling one-off commands from the shell

* Improved error messages for file downloads

*1.2.0* - *2017-12-8*
---------------------

*New Functionality*

* Added support for the (confusingly named) Box cloud storage system.

**1.1.1** - *2017-12-7*
-----------------------

*Bugfixes*

* Google Drive stops making a bunch of incorrectly named folders that it can't find.

*UI Improvements*

* More useful error message when cfs-config hasn't been run.

*Added*

* A unit testing module.

1.1.0.1
-------

*Bugfixes*

* Setuptools incorrectly packaged the files which were uploaded to PyPI, so they had to be re-uploaded immediately. This should really not be considered a distinct version from 1.1.0, and is only a thing because of an upload error.

**1.1.0** - *2017-12-5*
-----------------------

*Bugfixes*

* The documentation correctly ships with the PyPI package.

* GDrive no longer breaks when CFS_Manager is installed from PyPI.

* Large Dropbox uploads no longer cause crashes.

*New Functionality*

* Added filename autocompletion option.

* Enabled the 'cfs-config' system command for the configuration flow.

* Enabled the 'cfs-watch' system command to add the current directory to the set of managed directories.

*UI Improvements*

* Added a list of command options to the CLI command listing.

**1.0.1** - *2017-12-4*
-----------------------

*Bugfixes*

* CLI tools are functional even if there's no managed.txt yet.

**1.0.0** - *2017-12-3*
-----------------------

(Nothing - initial release)