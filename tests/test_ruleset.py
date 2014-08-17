#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ruleset.py
----------------------------------

Tests for `Ruleset` module.
"""

import unittest

from smartfilesorter.ruleset import RuleSet
from smartfilesorter.matchrules.filenamestartswith import FilenameStartsWith
from smartfilesorter.actionrules.stopprocessing import StopProcessing


class TestRuleSet(unittest.TestCase):
    def setUp(self):
        # Create mock objects for the plugins
        match_plugins = {'filename-starts-with': FilenameStartsWith}
        action_plugins = {'stop-processing': StopProcessing}
        # Represents a single section of the YAML config file
        test_yaml = {'action': 'stop-processing',
                     'match': {'filename-starts-with': 'a', 'file-extension-is': '.jpg .gif .png .jpeg'},
                     'name': 'Just a test'}
        self.ruleset = RuleSet(test_yaml, match_plugins=match_plugins, action_plugins=action_plugins)

    def test_ruleset_name_is_set(self):
        # Name should be set by constructor
        self.assertEqual(str(self.ruleset), 'Ruleset: Just a test')
        self.assertEqual(self.ruleset.name, 'Just a test')

    def test_plugins_available(self):
        # Plugins
        self.assertGreaterEqual(len(self.ruleset.available_match_plugins), 1)
        self.assertGreaterEqual(len(self.ruleset.available_action_plugins), 1)

    def test_add_match_rule(self):
        self.ruleset.add_match_rule(config_name='filename-starts-with', value='abcdef')
        self.assertGreaterEqual(len(self.ruleset.match_rules), 1)

    def test_add_action_rule_without_value(self):
        self.ruleset.add_action_rule(config_name='stop-processing')
        self.assertGreaterEqual(len(self.ruleset.action_rules), 1)

    def test_add_action_rule_with_value(self):
        self.ruleset.add_action_rule(config_name='stop-processing', value='not needed for this rule')
        self.assertGreaterEqual(len(self.ruleset.action_rules), 1)

    def test_add_nonexistent_rule(self):
        # Test that an error is raised when a rule can't be found
        self.assertRaises(IndexError, self.ruleset.add_action_rule, 'i-do-not-exist')


if __name__ == '__main__':
    unittest.main()