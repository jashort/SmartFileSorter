#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_action_moveto.py
----------------------------------

Tests for moveto action rule
"""

import unittest
import tempfile
import os
import shutil

from smartfilesorter.actionrules.moveto import MoveTo


class TestMoveTo(unittest.TestCase):
    def setUp(self):
        # Make a temp directory and test file
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = os.path.join(self.source_dir, 'dest/')
        os.mkdir(self.dest_dir)

        self.test_filename = "test.txt"
        self.source_file = os.path.join(self.source_dir, self.test_filename)
        self.dest_file = os.path.join(self.dest_dir, self.test_filename)

        with open(self.source_file, 'w') as output:
            output.write("This is a test file.")

        self.action = MoveTo(self.dest_dir)

    def test_moveto(self):
        # Test that moveto works with the simple case - source file exists, dest file does not exist,
        # and source file gets moved successfully
        new_filename = self.action.do_action(self.source_file)
        self.assertEqual(new_filename, self.dest_file)
        self.assertTrue(os.path.isfile(self.dest_file), "Destination file does not exist")
        self.assertFalse(os.path.isfile(self.source_file), "Source file still exists")

    def test_moveto_dry_run(self):
        # Test that file is NOT moved when dryrun=True
        new_filename = self.action.do_action(self.source_file, dry_run=True)
        self.assertEqual(new_filename, self.source_file)
        self.assertFalse(os.path.isfile(self.dest_file), "Destination file does not exist")
        self.assertTrue(os.path.isfile(self.source_file), "Source file still exists")

    def test_moveto_destination_exists(self):
        # Test that if the file already exists in the destination directory, add _001
        # to the filename and try again.
        shutil.copy(self.source_file, self.dest_dir)
        new_filename = self.action.do_action(self.source_file)
        self.assertFalse(os.path.isfile(self.source_file), "Source file exists and should have been moved")
        self.assertTrue(os.path.isfile(new_filename), "Destination file does not exist and should")
        self.assertTrue(new_filename[-8:-4] == '_001', 'New file does not end in "_001"')

    def test_moveto_destination_exists_twice(self):
        # Test that if the file already exists in the destination directory, and a file with the _001 suffix
        # in the filename exists, that the file will be renamed to <filename>_002.extension
        shutil.copy(self.source_file, self.dest_dir)
        filename, extension = os.path.splitext(self.dest_file)
        file1 = os.path.join(self.dest_dir, (filename + '_001' + extension))
        shutil.copy(self.source_file, file1)

        new_filename = self.action.do_action(self.source_file)
        self.assertFalse(os.path.isfile(self.source_file), "Source file exists and should have been moved")
        self.assertTrue(os.path.isfile(new_filename), "Destination file does not exist and should")
        self.assertTrue(new_filename[-8:-4] == '_002', 'New file does not end in "_002"')



    def tearDown(self):
        # Clean up temp files
        shutil.rmtree(self.source_dir)


if __name__ == '__main__':
    unittest.main()