*****
F.A.Q
*****

Interface
=========

**How does file name autocompletion work?**

To autocomplete a file name, you need to write out the command you want to use and the beginning of the file name. After the partial file name, you should add the '-c' modifier. Make sure there's a space between the partial filename and '-c'!

For example, if you have the file 'my fly mixtape track 1.mp3', you can download it by typing ``--download 'my fly' -c``. However, this only works if there's only one thing that could possibly match! If you also have the file 'my flying leason.mov' then, because they both begin with 'my fly', they might be confused with each other and you won't know which one will get downloaded. To avoid this, please write out enough of the name that no other file will match with it.

**Can I use autocomplete with uploads?**

Unfortunately, no. CFS_Manager knows the name of every file in your cloud system, but it does *not* know the name of every file on your hard drive. Getting a list of all of those would take a *very* long time. Since you can upload a file from any location on your computer, the app can't possibly guess which one you might mean, so you'll have to write the whole thing out.

**How does the 'verbose' command work?**

If you use the '--help' command, either on its own (to get the system-level help) or after a command (to get the help info for that command), you'll get the a reasonably short response. The default help statement for each command is just one line, and the default help file is half a dozen.

But what happens if that isn't enough information? You know what a command does, but not exactly what information you have to give for that command to do it's job? ("Do I give it a file name? A file path? How many arguments do I feed it?...") Or what if you want the more detailed explain-like-I'm-five help file? In that case, you should follow the '--help' command with the '--verbose' flag. Then you'll get the much wordier version. (If that *still* isn't enough, you can always use '--docs' to get to the documentation.)

Also, if you use '--verbose' after '--commands', you'll get the long-form description of *every* command. Which will probably take up your screen, but at least you'll have *all* the info.

**How do managed directories work?**

The managed directories are all the folders that CFS_Manager has been explicitly told about. If you use '--upload-all', the application will upload all your files from each of those folders.

If you want to add a folder to this list, there are multiple options. One is to navigate to the relevant directory in your shell and then run the ``cfs-watch`` command. A more graphical way to do this would be to drag-and-drop a copy of the cfs-watcher.py file from the cfs_manager directory into the one you want to manage, and then run that file. Finally, you can directly edit the managed.txt file in the cfs_manager directory to add a new folder to the list.

**What is a zipper.ignore file?**

If you use an automatic method to add a managed directory, this will create a 'zipper.ignore' file. What this does is list all the files and directories that cfs_manager shouldn't upload. This tells the 'zipper' module, which compresses all the files for upload, that it should ignore everything in that list. 'zipper.ignore' is a regular text file, so you can add things to it if you want.

If you have a 'zipper.ignore' file in any directory, then cfs_manager will ignore the files it lists, regardless of what upload method you use. Whether you use '--upload-all' or '--upload [directory name]'; whether the folder is in your managed.txt or not. You can create one yourself and put it anywhere and it'll work the same.

**Can I drag files into the CFS_Manager folder to manage them?**

As of 1.2.x, this functionality is unsupported. Please check back here in case we get a chance to add it.

Development
===========

**What versioning system does the project use?**

CFS_Manager follows `Semantic Versioning <http://semver.org/>`_. That means that the version number comes in three parts - Major.Minor.Patch - with each number indicating a different degree of change.

* The patch number is changed when new bug fixes, performance improvements, and other background-level contributions are made.

* The minor version is incremented when new functionality is added that doesn't interfere with existing functionality.

* The major version is incremented when the interface is changed in ways that make things that used to work stop working.

Notably, the interface here refers to the command line interface. Anything that you can do in the CLI today should work just the same in the future, if the major version is the same. However, there is also a plugin architecture in the works which will likely be less stable, so there may be breaking changes to the plugin system in minor version - at least until plugins are out of alpha.

**What should I do if I want to contribute?**

At the moment, your best bets are either creating an issue on GitHub or emailing Alison directly. Then you can share your ideas, suggest new features, and figure out what sub-problems to work on.

If you want to learn more about the general guidelines around contributions, please read the `Contributor Notes <contributor_notes.html>`_. If you want a problem to tackle *right now*, please check out the `Project Direction <direction.html>`_ page. It has a list of open problems and goals for the project, and if you tackle one of them the project will be forever grateful.