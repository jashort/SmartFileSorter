#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for match rule filenamematches
"""

import unittest
from smartfilesorter.matchplugins.filenamematches import FilenameMatches


class TestFilenameMatches(unittest.TestCase):
    def setUp(self):
        self.rule = FilenameMatches('^ex\d\d\d\d')

    def test_regex_match(self):
        # Regex is case sensitive
        self.assertTrue(self.rule.test('ex20140801.log'))
        self.assertFalse(self.rule.test('EX20140801.log'))

    def test_regex_doesnt_match(self):
        self.assertFalse(self.rule.test('tta3.log'))


if __name__ == '__main__':
    unittest.main()
