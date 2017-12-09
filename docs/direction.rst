*****************
Project Direction
*****************

There are many areas of the CFS_Manager project that are in need of development. If you'd like to tackle one of these areas, go ahead and make a pull request. If you'd like to add to this list, you can open an issue on GitHub. You can also contact Alison directly with any feedback or suggestions.


Open Issues
===========

*Bugs*
------

* Inability to store files of the same name

* Autocomplete occasionally returns names that are missing their first letter(s)


*Performance Drains*
--------------------

* Cloud systems must be accessed sequentially

* Zipping files is slow. (According to cProfile, the slowest part of the package that isn't network-access.)


Goals
=====

*Recurring*
-----------

* Writing/editing documentation

* Writing new unit tests *(please help!)*

* Integrating more storage providers

* Test on new operating systems


*Near-term Enhancements*
------------------------

* Open cloud files on local machine

* Migrating to a database using SQLAlchemy

* When multiple files share a name, return list for user confirmation

* Allow users to choose storage order

* Make files that are dropped into a CFS_Manager folder managable


*Medium-term Enhancements*
--------------------------

* Allow file encryption

* Create architecture for plugins

* Enable users to sign up for new storage providers

* Enable multi-user shared folder access


*Stretch Goals*
---------------

* Have network connections to each cloud run as concurrent processes

* Programmatically determine the best deal on buying extra storage

* Create a GUI for file management

* Make the cloud filesystem locally mountable