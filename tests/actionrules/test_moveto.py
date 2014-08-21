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

    def test_moveto_dryrun(self):
        # Test that file is NOT moved when dryrun=True
        new_filename = self.action.do_action(self.source_file, dry_run=True)
        self.assertEqual(new_filename, self.source_file)
        self.assertFalse(os.path.isfile(self.dest_file), "Destination file does not exist")
        self.assertTrue(os.path.isfile(self.source_file), "Source file still exists")

    def test_moveto_dest_exists(self):
        # Test that error is raised when destination file exists
        shutil.copy(self.source_file, self.dest_dir)
        self.assertRaises(IOError, self.action.do_action, self.source_file)
        self.assertTrue(os.path.isfile(self.source_file), "Source file does not exist")
        self.assertTrue(os.path.isfile(self.dest_file), "Destination file does not exist and should")

    def tearDown(self):
        # Clean up temp files
        shutil.rmtree(self.source_dir)



if __name__ == '__main__':
    unittest.main()