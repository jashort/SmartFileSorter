#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for match rule filenamematches
"""

import unittest
from smartfilesorter.matchrules.filenamematches import FilenameMatches


class TestFilenameMatches(unittest.TestCase):
    def setUp(self):
        self.rule = FilenameMatches('^ex\d\d\d\d')

    def test_regex_match(self):
        self.assertTrue(self.rule.matches('ex20140801.log'))
        self.assertFalse(self.rule.matches('EX20140801.log'))


if __name__ == '__main__':
    unittest.main()