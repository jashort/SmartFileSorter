
"""
test_ruleset.py
----------------------------------

Tests for `Ruleset` module.
"""

import unittest
from smartfilesorter.ruleset import RuleSet


# Dummy objects
class FilenameStartsWith(object):
    def __init__(self, value):
        self.config_name = 'filename-starts-with'


class FileExtensionIs(object):
    def __init__(self, value):
        self.config_name = 'file-extension-is'


class StopProcessing(object):
    def __init__(self, value):
        self.config_name = 'stop-processing'


class TestRuleSet(unittest.TestCase):
    def setUp(self):
        # Create mock objects for the plugins
        match_plugins = {'filename-starts-with': FilenameStartsWith, 'file-extension-is': FileExtensionIs}
        action_plugins = {'stop-processing': StopProcessing}
        # Represents a single section of the YAML config file
        test_yaml = {'action': 'stop-processing',
                     'match': {'filename-starts-with': 'a'},
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
        self.ruleset.add_match_rule({'filename-starts-with': 'abcdef'})
        self.assertGreaterEqual(len(self.ruleset.match_rules), 1)

    def test_add_action_rule_without_value(self):
        self.ruleset.add_action_rule('stop-processing')
        self.assertGreaterEqual(len(self.ruleset.action_rules), 1)

    def test_add_action_rule_with_value(self):
        self.ruleset.add_action_rule({'stop-processing': 'not needed for this rule'})
        self.assertGreaterEqual(len(self.ruleset.action_rules), 1)

    def test_add_nonexistent_rule(self):
        # Test that an error is raised when a rule can't be found
        self.assertRaises(IndexError, self.ruleset.add_action_rule, 'i-do-not-exist')


class TestRuleSetInList(unittest.TestCase):
    """
    Plugins in the config file can either be individual strings, or a list of objects. This is testing
    when the rules are in lists.
    """
    def setUp(self):
        # Create mock objects for the plugins
        match_plugins = {'filename-starts-with': FilenameStartsWith, 'file-extension-is': FileExtensionIs}
        action_plugins = {'stop-processing': StopProcessing}
        # Represents a single section of the YAML config file
        test_yaml = {'action': ['stop-processing'],
                     'match': [{'filename-starts-with': 'a'}, {'file-extension-is': '.jpg .gif .png .jpeg'}],
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
        self.ruleset.add_match_rule({'filename-starts-with': 'abcdef'})
        self.assertGreaterEqual(len(self.ruleset.match_rules), 1)

    def test_add_action_rule_without_value(self):
        self.ruleset.add_action_rule('stop-processing')
        self.assertGreaterEqual(len(self.ruleset.action_rules), 1)

    def test_add_action_rule_with_value(self):
        self.ruleset.add_action_rule({'stop-processing': 'not needed for this rule'})
        self.assertGreaterEqual(len(self.ruleset.action_rules), 1)

    def test_add_nonexistent_rule(self):
        # Test that an error is raised when a rule can't be found
        self.assertRaises(IndexError, self.ruleset.add_action_rule, 'i-do-not-exist')


if __name__ == '__main__':
    unittest.main()
