========
Match Plugins
========

Match Plugins indicate if a given file matches the rule it defines. For example, if the file has a certain
extension, or if the file name starts with a certain character. The available match plugins are:

- file-extension-is_
- filename-contains_
- filename-ends-with_
- filename-matches_
- filename-starts-with_

file-extension-is
-----------------
Matches if the file's extension is equal to the given extension. Not case sensitive. More than one extension
may be given, space separated.

.. code:: yaml

      match:
        - file-extension-is: .log .txt

Would match:
  - test.log
  - test.txt
  - a.file.with.multiple.periods.txt
But not:
  - test.jpg


filename-contains
-----------------
Matches if the filename (without extension) contains the given string. Not case sensitive.

.. code:: yaml

      match:
        - filename-contains: foo

Would match:
  - this_file_has_foo.log
  - foo_and_more_foo.log
But not:
  - test.jpg
  - test.foo


filename-ends-with
------------------
Matches if the filename (without extension) ends with the given string. Not case sensitive.

.. code:: yaml

      match:
        - filename-ends-with: bar

Would match:
  - foo_and_bar.log
  - bar.log
But not:
  - bar_test.jpg
  - test.bar


filename-matches
----------------
Matches if the filename (without extension) matches the given regular expression. Is case sensitive unless the regex
says otherwise. See https://docs.python.org/3/howto/regex.html for more information on regular expressions.

.. code:: yaml

      match:
        - filename-matches: ^\d\d\d\d.

Would match:
  - 1234.log
  - 7890_and_other_things.log
But not:
  - abc1234.jpg
  - 12.log


filename-starts-with
--------------------
Matches if the filename (without extension) starts with the given string. Not case sensitive.

.. code:: yaml

      match:
        - filename-starts-with: abc

Would match:
  - abcdefg.log
  - abc.log
  - AbCdEf.txt
But not:
  - bcdef.jpg
