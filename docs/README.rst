*******
Read Me
*******

CFS_Manager aims to make cloud storage easy to manage, even when you're dealing with multiple providers. It creates a unified API for upload/download/modification of files on multiple platforms. The unified API is mostly internal to the script, as the main user interface is the console script (cli.py).

The most recent release supports simultaneous integration with up to four storage providers: Google, Dropbox, Box, and pCloud. In addition, there is a clear and documented process for adding support for new providers, so a rapid expansion in supported platforms should be expected. Once setup, you should be able to treat all your storage providers as if they were a unified whole, with more space than any one would have individually.

Setup And Installation
======================

To use CFS_Manager, you need to have Python 3 and pip installed. Then run: ``pip install cfs_manager``. The installation and dependencies will then be handled automatically. (Note: As CFS_Manager interacts with the SDKs of multiple cloud storage providers, these will also be installed as dependencies.)
	
**Warning:** The Dropbox SDK claims to be incompatible with Python <3.4.
While problems haven't been reproduced, managing Dropbox using CFS_Manager is not recommended unless you have Python 3.4 or higher.

After installation, you'll have new system-level commands you can use to control CFS_Manager. To enable the CLI to interact with your cloud accounts, run ``cfs-config`` in the shell to set up your system. The console dialogue should walk you through providing settings. If you ever want to change your settings, just run ``cfs-config`` again with different inputs. After that, running ``cfs-manager`` or ``cfsm`` will allow you to interact with the file manager directly.

If you want to add a folder to your list of managed directories, you can just drag cfs_watcher.py into that folder and run it. Alternatively, you can navigate to a directory and then run ``cfs-watch``. If you do either of these, it will also create a zipper.ignore file in the directory. This is a regular text file you can use to list any files or directories that shouldn't be uploaded. As a last resort, you can manually add the file path to a 'managed.txt' file in CFS_Manager's installed directory.

This utility aims for OS-independence and should work on Windows, Mac, and Linux (at least). (In case you encounter OS-specific issues, please note your OS in bug reports so attempts to reproduce it go smoothly.)
	
About
=====

CFS_Manager uses the Apache 2.0 license and is `publicly hosted on github <https://github.com/alisonstreete/cfs-manager/>`_.
It is developed by Alison Streete, but welcomes anyone interested in contributing. (You could see your name on this line!)

Questions? Bugs? Kudos? Confusion? Want to buy the developer a drink? Email her at alison.streete {@} gmail.com.
*(If it's a bug, pull requests work too.)*

See the *About CFS_Manager* page for more details.