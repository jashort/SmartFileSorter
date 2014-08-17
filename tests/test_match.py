#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyfilemover
----------------------------------

Tests for `pyfilemover` module.
"""

import unittest

from smartfilesorter.matchrules.fileextensionis import FileExtensionIs
from smartfilesorter.matchrules.filenamestartswith import FilenameStartsWith
from smartfilesorter.matchrules.filenameendswith import FilenameEndsWith
from smartfilesorter.matchrules.filenamecontains import FilenameContains


class TestFilenameStartsWith(unittest.TestCase):
    def setUp(self):
        self.rule = FilenameStartsWith('test_')

    def test_case_sensitive_match(self):
        self.rule.case_sensitive = True
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertFalse(self.rule.matches('/tmp/TEST_FILE.log'))

    def test_case_insensitive_match(self):
        self.rule.case_sensitive = False
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertTrue(self.rule.matches('/tmp/TEST_FILE.log'))


class TestFilenameEndsWith(unittest.TestCase):
    def setUp(self):
        self.rule = FilenameEndsWith('_file')

    def test_case_sensitive_match(self):
        self.rule.case_sensitive = True
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertFalse(self.rule.matches('/tmp/TEST_FILE.log'))

    def test_case_insensitive_match(self):
        self.rule.case_sensitive = False
        self.assertTrue(self.rule.matches('/tmp/test_file.log'))
        self.assertTrue(self.rule.matches('/tmp/TEST_FILE.log'))


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