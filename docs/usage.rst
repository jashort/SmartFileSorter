========
Usage Example
========

- Basic Example
- Advanced Example


Basic Example
=============

To use SmartFileSorter, create a rule file. For example:

.. code:: yaml

    # test.yml
    - name: Move Logs
      match:
        - file-extension-is: .log
      action:
        - move-to: /archive


Then run the sfp command. In this case, it will process the rules in the test.yml file against
every file in the /tmp directory, without actually performing any actions. Assuming there are
two files with the .log extension in /tmp (test1.log and test2.log), the output would look like
this::

    $ sfs test.yml /tmp --dry-run
    Running with --dry-run parameter. Actions will not be performed.
    Files matched: 2/10
    Move Logs: 2 files

And to actually move the files, run without the --dry-run parameter::

    $ sfs test.yml /tmp
    Files matched: 2/10
    Move Logs: 2 files

The two files would be moved to the directory /archive.


Advanced Example
================

In this example, we'll move and rename log files in the /tmp/ directory in to the /archive/ directory by year.
Assume that the log files are named test-YY-MM-DD.log and we want them to be named YYYY-MM-DD.log

.. code:: yaml

    # test2.yml
    - name: Move and Rename 2014 Logs
      match:
        - filename-starts-with: test-14
        - file-extension-is: .log
      action:
        - rename-to:
          match: ^test-14
          replace-with: 2014
        - move-to: /archive/2014/

    - name: Move and Rename 2013 Logs
      match:
        - filename-starts-with: test-13
        - file-extension-is: .log
      action:
        - rename-to:
          match: ^test-13
          replace-with: 2013
        - move-to: /archive/2013/

    - name: Move and Rename 2012 data
      match:
        - filename-starts-with: test-12
        - file-extension-is: .log
      action:
        - rename-to:
          match: ^test-12
          replace-with: 2012
        - move-to: /archive/2012/


Use --dry-run to see what files would be affected::

    $ ls /tmp
    test-13-05-01.log
    test-14-01-01.log
    test-14-01-02.log

    $ sfs test2.yml /tmp --dry-run
    Running with --dry-run parameter. Actions will not be performed.
    Files matched: 3/3
    Move and Rename 2013 data: 1 file(s)
    Move and Rename 2014 data: 2 file(s)

And to actually move the files, run without the --dry-run parameter::

    $ sfs test2.yml /tmp
    Files matched: 3/3
    Move and Rename 2013 data: 1 file(s)
    Move and Rename 2014 data: 2 file(s)

Here are the results::

    $ ls -R /archive
    /archive/2012:

    /archive/2013:
    test-2013-05-01.log

    /archive/2014:
    test-2014-01-01.log
    test-2014-01-02.log

