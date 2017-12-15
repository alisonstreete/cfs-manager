*************
Features List
*************

This page is for cataloguing all the exciting features of CFS_Manager.

`Planned future features are discussed here <direction.html>`_

System Commands
===============

*After installing CFS_Manager, you should be able to run any of these in your shell/terminal/command-prompt*

* ``cfs-config``

Starts the configuration flow for CFS_Manager, allowing the user to choose defaults and allow access to their preferred storage providers.

* ``cfsm`` or ``cfs-manager``

Starts the CFS_Manager command line interface in the terminal window that is currently open.

* ``cfs-do [command]``

Initialises the virtual file system, performs the specified command, and then terminates. Allows the execution of one-off commands (such as downloading a specific file) without entering the embedded command line interface.

* ``cfs-watch``

Adds the current directory to the list of managed directories. Thus, its contents will be included any time a command to upload all managed files is given.

User Interface
==============

*For the specific commands behind each of these options, open the CFS_Manager command line and use '--commands' for a full list*

* Upload and download files and folders.

* List all the files in your virtual file system.

* Display the metadata associated with any given file, such as which storage provider it's hosted by and the date of last modification.

* Optional autocompletion of filenames, to avoid having to write out really long titles.

* Delete individual files or wipe all files from your virtual file system (with confirmation dialogue).

* Display the amount of cloud space currently occupied by CFS_Manager, and the amount of free space available across platforms.

* Detailed help page, about page, and list of CLI commands and flags.

* Launch the project's license, documentation, or github repository from the command line.