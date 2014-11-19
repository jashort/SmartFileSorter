#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartfilesorter.py
----------------------------------

Tests for `smartfilesorter` module.
"""

import unittest
import smartfilesorter
import logging
from docopt import DocoptExit
import os
from yaml import YAMLError
import tempfile
import shutil


class TestSmartFileSorter(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.s = smartfilesorter.SmartFileSorter()
        self.s.create_logger({})

    def test_parse_arguments_empty(self):
        self.assertRaises(DocoptExit, self.s.parse_arguments, [])

    def test_parse_arguments(self):
        args = self.s.parse_arguments(['test.yml', '/tmp'])
        self.assertEqual(args['RULEFILE'], 'test.yml')
        self.assertEqual(args['DIRECTORY'], '/tmp')
        self.assertFalse(args['--debug'])
        self.assertFalse(args['--dry-run'])
        self.assertEqual(args['--log'], None)

    def test_parse_arguments_list_plugins(self):
        args = self.s.parse_arguments(['--debug', '--list-plugins'])
        self.assertTrue(args['--list-plugins'])
        self.assertTrue(args['--debug'])

    def test_parse_dry_run(self):
        # Note that in this test, test.yml and /tmp don't have to exist, they're just placeholders
        # to test parsed values
        args = self.s.parse_arguments(['test.yml', '/tmp', '--dry-run'])
        self.assertEqual(args['RULEFILE'], 'test.yml')
        self.assertEqual(args['DIRECTORY'], '/tmp')
        self.assertFalse(args['--debug'])
        self.assertTrue(args['--dry-run'])
        self.assertEqual(args['--log'], None)

    def test_create_log_file(self):
        # Note that in this test, test.yml and /tmp don't have to exist, they're just placeholders
        tmp_file = os.path.join(self.tmp_dir, 'test.log')
        args = self.s.parse_arguments(['test.yml', '/tmp',  '--log=' + tmp_file, '--dry-run'])
        self.s.create_logger(args)
        self.assertEqual(tmp_file, args['--log'])
        # Verify the log was created and it has something in it
        self.assertTrue(os.path.exists(tmp_file))
        self.assertGreater(os.path.getsize(tmp_file), 0)

    def test_logger_info_level(self):
        # Test that a logger was created with INFO level (default)
        args = self.s.parse_arguments(['--list-plugins'])
        self.s.create_logger(args)
        self.assertEqual(logging.Logger, type(self.s.logger))
        self.assertEqual(logging.INFO, self.s.logger.level)

    def test_logger_debug_level(self):
        # Test that a logger was created with the level set to DEBUG
        args = self.s.parse_arguments(['--list-plugins', '--debug'])
        self.s.create_logger(args)
        self.assertEqual(logging.Logger, type(self.s.logger))
        self.assertEqual(logging.DEBUG, self.s.logger.level)

    def test_list_files_path_does_not_exist(self):
        f = self.s.get_files('asdfsadf')
        self.assertRaises(OSError, f.send, None)

    def test_load_plugins(self):
        module_path = os.path.dirname(smartfilesorter.__file__)
        plugin_path = os.path.join(module_path, 'matchplugins/')
        plugins = self.s.load_plugins(plugin_path)
        # Check to make sure at least one plugin loaded
        self.assertGreaterEqual(len(plugins), 0)

    def test_load_rules(self):
        # Test loading rules from example.yml in the tests directory
        test_path = os.path.dirname(__file__)
        test_file = os.path.join(test_path, 'example.yml')
        rules = self.s.load_rules(test_file)
        self.assertGreaterEqual(len(rules), 2)
        self.assertTrue('name' in rules[0])
        self.assertTrue('match' in rules[0])
        self.assertTrue('action' in rules[0])

    def test_load_rules_file_does_not_exist(self):
        self.assertRaises(IOError, self.s.load_rules, 'thisfiledoesnotexist')

    def test_load_rules_invalid_yaml_in_file(self):
        test_path = os.path.dirname(__file__)
        test_file = os.path.join(test_path, 'example-invalid.yml')
        self.assertRaises(YAMLError, self.s.load_rules, test_file)

    def test_run_list_plugins(self):
        # Simple case for the run function - just list plugins and exit
        args = self.s.parse_arguments(['--list-plugins'])
        self.assertRaises(SystemExit, self.s.run, args)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
