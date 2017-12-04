*******
Read Me
*******

The *Cloud File System Manager* (CFS_Manager) aims to make cloud storage easy to manage, even when you're dealing with multiple providers. It creates a unified API for upload/download/modification of files on multiple platforms. The unified API is mostly internal to the script, as the main user interface is the console script (cli.py).

This initial release supports simultaneous integration with up to three storage providers: Google, Dropbox, and pCloud. In addition, there is a clear and documented process for adding support for new providers, so a rapid expansion in supported platforms should be expected. Once setup, you should be able to treat all your storage providers as if they were a unified whole, with more space than any one would have individually.

Setup And Installation
======================

To use CFS_Manager, you need to have Python 3 and pip installed. Then run:
``pip install cfs_manager``
The installation and dependencies will then be handled automatically.
(Note: As CFS_Manager interacts with the SDKs of multiple cloud storage providers, these will also be installed as dependencies.)
	
**Warning:** The Dropbox SDK claims to be incompatible with Python <3.4.
While problems haven't been reproduced, managing Dropbox using CFS_Manager is not recommended unless you have Python 3.4 or higher.

To enable the CLI to interact with your cloud accounts, run configuration.py to set up your system.
The console dialogue should walk you through providing settings. If you ever want to change your settings, just run configuration.py again with different inputs.

If you want to add a folder to your list of managed directories, you can just drag cfs_watcher.py into that folder and run it. 
If you do this, it will create a zipper.ignore file in the directory. This is a regular text file you can use to list any files or directories that shouldn't be uploaded.
Alternatively, you can manually add the file path to a 'managed.txt' file in CFS_Manager's installed directory.

This utility aims at OS-independence and should work on Windows, Mac, and Linux (at least). (In case you encounter OS-specific issues, please note your OS in bug reports so attempts to reproduce it go smoothly.)
	
About
=====

CFS_Manager uses the Apache 2.0 license and is `publicly hosted on github <http://https://github.com/alisonstreete/cfs-manager/>`_.
It is developed by Alison Streete, but welcomes anyone interested in contributing. (You could see your name on this line!)

Questions? Bugs? Kudos? Confusion? Want to buy the developer a drink? Email her at alison.streete {@} gmail.com.
*(If it's a bug, pull requests work too.)*

See the *About CFS_Manager* page for more details.
