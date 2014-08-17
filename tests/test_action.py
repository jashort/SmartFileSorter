#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_action
----------------------------------

Tests for action rules
"""

import unittest

from smartfilesorter.actionrules.continueprocessing import ContinueProcessing
from smartfilesorter.actionrules.stopprocessing import StopProcessing
from smartfilesorter.actionrules.printfileinfo import PrintFileInfo


class TestContinueProcessing(unittest.TestCase):
    def setUp(self):
        self.action = ContinueProcessing()

    def test_continue(self):
        # Not much to test here - this action should return True without
        # actually doing anything
        self.assertTrue(self.action.do_action('/tmp/test_file.log'))


class TestStopProcessing(unittest.TestCase):
    def setUp(self):
        self.action = StopProcessing()

    def test_stop(self):
        self.assertFalse(self.action.do_action('/tmp/TEST_FILE.log'))


class TestPrintFileInfo(unittest.TestCase):
    def setUp(self):
        self.action = PrintFileInfo()

    def test_file_does_not_exist(self):
        # Should continue processing, even if it tries to perform action and can't.
        self.assertEqual(self.action.action('this_file_does_not_exist.txt'), True)

if __name__ == '__main__':
    unittest.main()