#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for match rule FilenameStartsWith
"""

import unittest
from smartfilesorter.matchplugins.filenamestartswith import FilenameStartsWith


class TestFilenameStartsWith(unittest.TestCase):
    def setUp(self):
        self.rule = FilenameStartsWith('test_')

    def test_case_sensitive_match(self):
        self.rule.case_sensitive = True
        self.assertTrue(self.rule.test('/tmp/test_file.log'))
        self.assertFalse(self.rule.test('/tmp/TEST_FILE.log'))

    def test_case_insensitive_match(self):
        self.rule.case_sensitive = False
        self.assertTrue(self.rule.test('/tmp/test_file.log'))
        self.assertTrue(self.rule.test('/tmp/TEST_FILE.log'))


if __name__ == '__main__':
    unittest.main()
