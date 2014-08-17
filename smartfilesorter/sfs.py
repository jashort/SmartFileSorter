#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import logging
import os
import yaml
import inspect
from ruleset import RuleSet


class SmartFileSorter(object):
    def __init__(self):
        self.logger = logging.getLogger('SmartFileSorter')
        self.args = None

    def parse_arguments(self):
        """
        Process command line arguments
        :return: object
        """
        # Define and parse command line arguments
        parser = argparse.ArgumentParser(description='Rule based file mover/renamer')
        parser.add_argument('filename', type=argparse.FileType('r'), help='Rules to process')
        parser.add_argument('source_directory_or_file', type=str, help='Source directory or filename')
        parser.add_argument('--log', type=argparse.FileType('w'), default=None, help='Output Log Filename')
        parser.add_argument('--debug',
                            action='store_true',
                            default=False,
                            help='Enable extra log information')
        parser.add_argument('--dry-run',
                            action='store_true',
                            default=False,
                            help='Log actions that would be executed but does not execute them')
        self.args = parser.parse_args()
        return self.args

    def create_logger(self, args):
        """
        Configure the program's logger object.

        Log levels:
        INFO - information only, hidden unless --debug is used
        ERROR - Critical error
        :param args: Object containing program's parsed command line arguments
        :return: logger
        """
        # Set up logging
        file_log_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s',
                                               '%Y-%m-%d %H:%M:%S')
        console_log_formatter = logging.Formatter('%(name)s %(message)s')

        # Log to stdout
        stdout_stream = logging.StreamHandler(stream=sys.stdout)
        stdout_stream.setFormatter(console_log_formatter)
        self.logger.addHandler(stdout_stream)

        # Log to file if the option is chosen
        if args.log is not None:
            logfile_stream = logging.StreamHandler(stream=args.log)
            logfile_stream.setFormatter(file_log_formatter)
            self.logger.addHandler(logfile_stream)

        if args.debug is True:
            self.logger.setLevel(logging.DEBUG)

        if args.dry_run is True:
            self.logger.info('Running with --dry-run parameter. Actions will not be executed.')

    def get_files(self, path):
        """
        Yields full path and filename for each file that exists in the given directory. Will
        ignore hidden files (that start with a ".") and directories
        :param path: Directory or filename
        :return:
        """

        if os.path.isfile(path):
            self.logger.debug('Called with single file as target: {0}'.format(path))
            yield path
            return

        self.logger.info('Getting list of files in {0}'.format(path))

        try:
            for f in os.listdir(path):
                cur_file = os.path.join(path, f)
                if f[0] != '.' and os.path.isfile(cur_file):
                    yield cur_file
        except OSError:
            self.logger.error('Could not read files from {0}'.format(path))
            sys.exit(1)

    def load_rules(self, in_file):
        """
        Load rules from YAML configuration in the given stream object
        :param in_file: stream object containing rules YAML
        :return: rules object
        """
        self.logger.info('Reading rules from %s', in_file.name)
        try:
            y = yaml.load(in_file)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                self.logger.error('Error parsing rules{0}'.format(exc.problem_mark))
            else:
                self.logger.error('Error parsing rules in {0}'.format(in_file.name))
            sys.exit(1)
        return y

    def load_plugins(self, plugin_path):
        """
        Loads plugins from modules in plugin_path. Looks for the config_name property
        in each object that's found. If so, adds that to the dictionary with the
        config_name as the key. config_name should be unique between different plugins.

        :param plugin_path: Path to load plugins from
        :return: dictionary of plugins by config_name
        """
        self.logger.debug('Loading plugins from {0}'.format(plugin_path))
        plugins = {}
        plugin_dir = os.path.realpath(plugin_path)
        sys.path.append(plugin_dir)

        for f in os.listdir(plugin_dir):
            if f.endswith(".py"):
                name = f[:-3]
            elif f.endswith(".pyc"):
                name = f[:-4]
            # Possible support for plugins inside directories - worth doing?
            # elif os.path.isdir(os.path.join(plugin_dir, f)):
            #    name = f
            else:
                continue

            try:
                self.logger.debug('Adding plugin from: {0}'.format(f))
                mod = __import__(name, globals(), locals(), [], 0)

                for piece in inspect.getmembers(mod):
                    if piece[0][0:2] == '__':            # Skip dunder members - builtins, etc
                        continue
                    if hasattr(piece[1], 'config_name'):
                        if piece[1].config_name is not None:
                            # Skip plugins where config_name is None, like the base classes
                            plugins[piece[1].config_name] = piece[1]
                            self.logger.debug('Added plugin: {0}'.format(piece[1].config_name))

                            # Todo: Add error checking here. If a plugin with that name already exists,
                            # log an error. Quit or continue?

            except ImportError as e:
                self.logger.error(e)
                pass            # problem importing

        self.logger.debug('Done loading plugins')
        return plugins

    def build_rules(self, rule_yaml, match_plugins, action_plugins):
        """
        Convert parsed rule YAML in to a list of ruleset objects
        :param rule_yaml: Dictionary parsed from YAML rule file
        :param match_plugins: Dictionary of match plugins (key=config_name, value=plugin object)
        :param action_plugins: Dictionary of action plugins (key=config_name, value=plugin object)
        :return: list of rules
        """
        rule_sets = []

        for yaml_section in rule_yaml:
            rule_sets.append(RuleSet(yaml_section, match_plugins=match_plugins, action_plugins=action_plugins))
        return rule_sets


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    m = SmartFileSorter()
    args = m.parse_arguments()
    m.create_logger(args)
    rule_yaml = m.load_rules(args.filename)

    match_plugins = m.load_plugins(os.path.join(script_dir, 'matchrules/'))
    action_plugins = m.load_plugins(os.path.join(script_dir, 'actionrules/'))

    rules = m.build_rules(rule_yaml, match_plugins, action_plugins)

    for cur_file in m.get_files(args.source_directory_or_file):
        m.logger.debug("Processing {0}".format(cur_file))

        for ruleset in rules:
            if ruleset.matches_all_rules(cur_file):
                # If the file matches all rules in the ruleset, do whatever
                # actions the ruleset specifies. Stop processing if the
                # ruleset says stop.
                keep_processing = ruleset.do_actions(cur_file, args.dry_run)
                if keep_processing is not True:
                    m.logger.debug("Stopping processing for this file")
                    break

