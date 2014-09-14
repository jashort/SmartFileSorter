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
every file in the /tmp directory, without actually performing any actions. If there are no
files with the .log extension in /tmp, the output would look like this::

    $ sfs ~/sortdl.yml /tmp --dry-run
    Running with --dry-run parameter. Actions will not be performed.
    Files matched: 0/4

