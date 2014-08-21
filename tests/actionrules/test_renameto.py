#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for renameto action rule
"""

import unittest
import tempfile
import os
import shutil
from smartfilesorter.actionrules.renameto import RenameTo


class TestContinueProcessing(unittest.TestCase):
    def setUp(self):
        # Make a temp directory and test file
        self.source_dir = tempfile.mkdtemp()

        self.test_filename = "abc_test.txt"
        self.destination_filename = "test.txt"
        self.source_file = os.path.join(self.source_dir, self.test_filename)
        self.destination_file = os.path.join(self.source_dir, self.destination_filename)

        with open(self.source_file, 'w') as output:
            output.write("This is a test file.")

        self.action = RenameTo('abc_ >> ')

    def test_renameto(self):
        # Test that renameto works with the simple case - source file exists, dest file does not exist,
        # and source file gets renamed successfully
        new_filename = self.action.do_action(self.source_file)
        self.assertEqual(self.destination_file, new_filename)
        self.assertTrue(os.path.isfile(self.destination_file), "Destination file does not exist")
        self.assertFalse(os.path.isfile(self.source_file), "Source file still exists")

    def test_renameto_dryrun(self):
        # Test that file is NOT renamed when dryrun=True
        new_filename = self.action.do_action(self.source_file, dry_run=True)
        self.assertEqual(self.source_file, new_filename)
        self.assertFalse(os.path.isfile(self.destination_file), "Destination file does not exist")
        self.assertTrue(os.path.isfile(self.source_file), "Source file still exists")

    # def test_moveto_dest_exists(self):
    #     # Test that error is raised when destination file exists
    #     shutil.copy(self.source_file, self.dest_dir)
    #     self.assertRaises(IOError, self.action.do_action, self.source_file)
    #     self.assertTrue(os.path.isfile(self.source_file), "Source file still exists")
    #     self.assertTrue(os.path.isfile(self.source_file), "Source file still exists")

    def tearDown(self):
        # Clean up temp files
        shutil.rmtree(self.source_dir)



if __name__ == '__main__':
    unittest.main()