#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_stopprocessing.py
----------------------------------

Tests for action rule stopprocessing
"""

import unittest
from smartfilesorter.actionrules.stopprocessing import StopProcessing


class TestStopProcessing(unittest.TestCase):
    def setUp(self):
        self.action = StopProcessing()

    def test_stop(self):
        self.assertFalse(self.action.do_action('/tmp/TEST_FILE.log'))


if __name__ == '__main__':
    unittest.main()