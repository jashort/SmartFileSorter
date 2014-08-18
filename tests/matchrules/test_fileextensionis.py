#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for match rule fileextensionis
"""

import unittest
from smartfilesorter.matchrules.fileextensionis import FileExtensionIs


class TestFileExtensionIs(unittest.TestCase):
    def setUp(self):
        self.rule = FileExtensionIs('.log .txt')

    def test_extensions_are_split(self):
        self.assertEqual(self.rule.extensions, ['.log', '.txt'])

    def test_case_sensitive_match(self):
        self.rule.case_sensitive = True
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertTrue(self.rule.matches('/tmp/test_file.txt'))
        self.assertFalse(self.rule.matches('/tmp/TEST_FILE.LOG'))
        self.assertFalse(self.rule.matches('/tmp/TEST_FILE.TxT'))

    def test_case_insensitive_match(self):
        self.rule.case_sensitive = False
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertTrue(self.rule.matches('/tmp/test_file.txt'))
        self.assertTrue(self.rule.matches('/tmp/TEST_FILE.LOG'))
        self.assertTrue(self.rule.matches('/tmp/TEST_FILE.TXT'))


if __name__ == '__main__':
    unittest.main()