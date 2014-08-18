#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for match rule filenamecontains
"""

import unittest
from smartfilesorter.matchrules.filenamecontains import FilenameContains


class TestFilenameContains(unittest.TestCase):
    def setUp(self):
        self.rule = FilenameContains('st_fi')

    def test_case_sensitive_match(self):
        self.rule.case_sensitive = True
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertFalse(self.rule.matches('/tmp/TEST_FILE.log'))

    def test_case_insensitive_match(self):
        self.rule.case_sensitive = False
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertTrue(self.rule.matches('/tmp/TEST_FILE.log'))


if __name__ == '__main__':
    unittest.main()