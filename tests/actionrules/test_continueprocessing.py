#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_continueprocessing.py
----------------------------------

Tests for action rule continueprocessing
"""

import unittest
from smartfilesorter.actionrules.continueprocessing import ContinueProcessing


class TestContinueProcessing(unittest.TestCase):
    def setUp(self):
        self.action = ContinueProcessing()

    def test_continue(self):
        # Not much to test here - this action should return True without
        # actually doing anything
        self.assertTrue(self.action.do_action('/tmp/test_file.log'))


if __name__ == '__main__':
    unittest.main()