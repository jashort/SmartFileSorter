===============================
SmartFileSorter
===============================

Rule-based file mover/renamer

* Free software: BSD license


Features
--------

SmartFileSorter is used to move files from one or more directories, to one or more
directories, based on user-defined rules. For example:

- Move uploaded files in to archive directories based on name and file modified date
  without overwriting files that already exist
- Move and rename server log files

It also supports "safe" moves. For example, if a file with the same name already exists
in the destination directory but is a different file (by size and md5 hash), it will 
append a suffix to the file before moving it.
