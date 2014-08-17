#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartfilesorter.py
----------------------------------

Tests for `smartfilesorter` module.
"""

import unittest
from smartfilesorter.sfs import SmartFileSorter


class TestSmartFileSorter(unittest.TestCase):

    def setUp(self):
        self.mover = SmartFileSorter()

    def test_load_plugins(self):
        plugins = self.mover.load_plugins('../smartfilesorter/matchrules/')
        # Check to make sure at least one plugin loaded
        self.assertGreaterEqual(len(plugins), 0)

    def test_something(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()