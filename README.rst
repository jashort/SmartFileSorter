===============================
Smart File Sorter
===============================

.. image:: https://badge.fury.io/py/SmartFileSorter.png
    :target: http://badge.fury.io/py/SmartFileSorter

.. image:: https://travis-ci.org/jashort/SmartFileSorter.png?branch=master
        :target: https://travis-ci.org/jashort/SmartFileSorter

.. image:: https://pypip.in/d/SmartFileSorter/badge.png
        :target: https://pypi.python.org/pypi/SmartFileSorter


Rule based file moving and renaming tool

* Free software: BSD license
* Documentation: https://smartfilesorter.readthedocs.org.

Features
--------

* Moves/renames files based on rules defined in a YAML configuration file.
* Automatically renames a file if it already exists in the destination directory by appending a sequence number to the
  filename. (file.txt, file_001.txt, file_002.txt, etc)
* Easy to extend with new match or action rules
