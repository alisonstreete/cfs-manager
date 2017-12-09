*****************
Contributor Notes
*****************

Project General
===============

This project follows `Semantic Versioning <http://semver.org/>`_.
As it is currently in 1.x, you can be confident that console commands that work now will keep working in other 1.x versions. As the internal API is not currently intended for out-of-app use, there may be breaking changes in minor versions. However, the internal API should remain stable through patch versions, and future releases that expose this API should fully stabilise it.
    
Comment Policy
==============

The general approach taken is to err on the side of too much commentary.
The goal is to make it easy to know exactly what's happening upon skimming a plain-English description.
Hopefully, one should not have to read the entire codebase to know what they need to change to improve their workflow or make a pull request. If you benefit from the current level of descriptiveness, please pass it on by including comments in your commits!

Direct contributions to the documentation or the UI text are considered as valuable as code contribution.
If there was anything you had to figure out on your own that you wish had been in the standard docs, please write it up!
The world will thank you (or, at least, Alison will).

Adding Support For Storage Providers
====================================

While all current support is built on top of externally sourced wrappers, this is not a requirement for contribution.
If you'd like to build integration for the bare REST API into this project, please go ahead! In fact, the use of a more minimal wrapper that only supports the operations CFS_Manager requires would make the whole project lighter-weight.

When adding an externally-sourced SDK to the dependency tree, check the license! It has to be compatible with imports from an Apache 2.0 project.
Preferred licenses for linked SDKs include the Apache, MIT, BSD, and ISC. (The LGPL is also compatible, but full GPL is not.)
    
If you'd like to suggest another storage provider to integrate, but don't want to write the code, go ahead.
However, if Alison is the one writing the code, she'll prioritise providers based on how simple the integration seems.
Providers with up-to-date SDKs and readable documentation go to the top of the stack.
If you're a fan/user/developer of a provider and really want support for it, and you want to speed it up, the best way is to write a wrapper yourself.
(The second best way is to improve their documentation and be on call for CFS_Manager developers to question you.)

Storage Provider Integration Process
-------------------------------------
If you add a new provider, there are a few places where updates will need to happen to fully integrate them:

#. You'll need to write the in-project wrapper. The current style of the project involves writing an internal wrapper to talk to external ones. Any new wrappers written should losely comply with the conventions of the other ones in terms of function names and what results they achieve.

#. You'll need to write a new class in file_systems.py. This class must inherit from CloudFileSystem and include the same methods. What those methods do is stated in their doc strings in the CloudFileSystem class definition. The consistency is necessary, as it's part of the internal API. Those methods will be called, by name, by manager.py, which is a high-level abstraction over all the cloud accounts and must treat them interchangeably.

#. You'll need to import this class to manager.py, and add it to the list 'fs_classes'. This will be how the manager instantiates these filesystems.

#. Create a function to convert the file metadata returned by the specific API to the general metadata format used by the manager.

#. Depending on what the access credentials needed by the file system are, you should add a setup step to the configuration.py. Ideally, users should save as much reusable info as possible (passwords excepted). Configuration imports fs_classes from manager.py, so your addition will automatically show up in the list of file systems for users to approve. However, you'll still need a step to write its name to the system_configuration.txt file.
    
Once you've completed those five steps, the newly-added filesystem should work just as well as all the others.