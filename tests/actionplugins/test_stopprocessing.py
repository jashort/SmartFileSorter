"""
test_stopprocessing.py
----------------------------------

Tests for action rule stopprocessing
"""

import unittest
from smartfilesorter.actionplugins.stopprocessing import StopProcessing
from smartfilesorter.smartfilesorter import StopProcessingException


class TestStopProcessing(unittest.TestCase):
    def setUp(self):
        self.action = StopProcessing(None)

    def test_stop(self):
        self.assertRaises(StopProcessingException, self.action.do_action, '/tmp/TEST_FILE.log')

if __name__ == '__main__':
    unittest.main()
