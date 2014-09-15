========
Action Plugins
========

Action Plugins tell Smart File Sorter what to do with a file if it matches all the rules in that ruleset. For exmaple,
rename or move the file. The available action plugins are:

- move-to_
- print-file-inf_
- rename-to_
- stop-processing_


move-to
-----------------
Moves the file to the given directory. If a file with the same name already exists, the current file with have a
numbered suffix appended. For example, abc.log would be renamed to abc_001.log.

.. code:: yaml

      action:
        - move-to: /archive/

Would move the file to the /archive/ directory.


print-file-info
-----------------
Prints information on the file. Mostly used for testing.

.. code:: yaml

      action:
        - print-file-info


rename-to
------------------
In the filename, replaces the match value (a regular expression) with the replace-with value. Is case sensitive

.. code:: yaml

    action:
      - rename-to:
          match: ^\d\d\d\d
          replace-with: abcd

Would change:
  - 1234_and_things.txt to abcd_and_things
  - 7980.txt to abcd.txt

.. code:: yaml

    action:
      - rename-to:
          match: XYZ
          replace-with: 123

Would change:
  - XYZ.txt to 123.txt
  - xyz_and_XYZ.txt to xyz_and_XYZ.txt


stop-processing
----------------
This rule stops all further processing on the current file.

.. code:: yaml

      action:
        - stop-processing
