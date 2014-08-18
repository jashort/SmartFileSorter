#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_printfileinfo.py
----------------------------------

Tests for action rule printfileinfo
"""

import unittest
from smartfilesorter.actionrules.printfileinfo import PrintFileInfo


class TestPrintFileInfo(unittest.TestCase):
    def setUp(self):
        self.action = PrintFileInfo()

    def test_file_does_not_exist(self):
        # Should continue processing, even if it tries to perform action and can't.
        self.assertEqual(self.action.action('this_file_does_not_exist.txt'), True)

if __name__ == '__main__':
    unittest.main()