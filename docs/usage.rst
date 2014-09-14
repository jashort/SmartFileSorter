========
Usage Example
========

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
    Move Logs: test1.log - Match
    Move Logs: test2.log - Match
    Files matched: 2/10

And to actually move the files, run without the --dry-run parameter::

    $ sfs test.yml /tmp
    Move Logs: test1.log - Match
    Move Logs: test2.log - Match
    Files matched: 2/10

The two files would be moved to the directory /archive.
