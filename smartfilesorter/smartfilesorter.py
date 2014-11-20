# -*- coding: utf-8 -*-

import sys
import logging
import os
import yaml
import inspect
from .ruleset import RuleSet
from .exceptions import StopProcessingException
import docopt


class SmartFileSorter(object):
    def __init__(self):
        self.args = None
        self.logger = None
        self.match_plugins = []
        self.action_plugins = []

    @staticmethod
    def parse_arguments(arguments=sys.argv[1:]):
        """
        Process command line arguments
        :param: List of strings containing command line arguments, defaults to sys.argv[1:]
        :return: docopt args object
        """
        args = docopt.docopt(doc="""
Smart File Sorter

Usage:
  sfp RULEFILE DIRECTORY [--debug] [--dry-run] [--log LOGFILE]
  sfp [--debug] --list-plugins

Options:
    RULEFILE        Rule configuration file to execute
    DIRECTORY       Directory of files to process
    --debug         Log extra information during processing
    --dry-run       Log actions but do not make any changes
    --log LOGFILE   Specify log output file
    --list-plugins  Print match and action plugin information
        """, argv=arguments)
        return args

    def create_logger(self, args={}):
        """
        Create and configure the program's logger object.

        Log levels:
        DEBUG - Log everything. Hidden unless --debug is used.
        INFO - information only
        ERROR - Critical error
        :param args: Object containing program's parsed command line arguments
        :return: None
        """
        # Set up logging
        logger = logging.getLogger("SmartFileSorter")
        logger.level = logging.INFO

        if '--debug' in args and args['--debug'] is True:
            logger.setLevel(logging.DEBUG)

        file_log_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s',
                                               '%Y-%m-%d %H:%M:%S')
        console_log_formatter = logging.Formatter('%(message)s')

        # Log to stdout
        stdout_stream = logging.StreamHandler(stream=sys.stdout)
        stdout_stream.setFormatter(console_log_formatter)
        logger.addHandler(stdout_stream)

        # Log to file if the option is chosen
        if '--log' in args and args['--log'] is not None:
            logfile = open(args['--log'], 'w')
            logfile_stream = logging.StreamHandler(stream=logfile)
            logfile_stream.setFormatter(file_log_formatter)
            logger.addHandler(logfile_stream)

        if '--dry-run' in args and args['--dry-run'] is True:
            logger.info('Running with --dry-run parameter. Actions will not be performed.')
        self.logger = logger

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

        self.logger.debug('Getting list of files in {0}'.format(path))

        try:
            for f in os.listdir(path):
                cur_file = os.path.join(path, f)
                if f[0] != '.' and os.path.isfile(cur_file):
                    yield cur_file
        except OSError:
            self.logger.error('Could not read files from {0}'.format(path))
            raise

    def load_rules(self, filename):
        """
        Load rules from YAML configuration in the given stream object
        :param filename: Filename of rule YAML file
        :return: rules object
        """
        self.logger.debug('Reading rules from %s', filename)
        try:
            in_file = open(filename)
        except IOError:
            self.logger.error('Error opening {0}'.format(filename))
            raise

        y = None
        try:
            y = yaml.load(in_file)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                self.logger.error('Error parsing rules{0}'.format(exc.problem_mark))

            else:
                self.logger.error('Error parsing rules in {0}'.format(in_file.name))
            raise
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

                for plugin_class in inspect.getmembers(mod):
                    if plugin_class[0][0:2] == '__':            # Skip dunder members - builtins, etc
                        continue
                    if hasattr(plugin_class[1], 'config_name'):
                        if plugin_class[1].config_name is not None:
                            # Skip plugins where config_name is None, like the base classes
                            plugins[plugin_class[1].config_name] = plugin_class[1]
                            self.logger.debug('Added plugin: {0}'.format(plugin_class[1].config_name))

                            # Todo: Add error checking here. If a plugin with that name already exists,
                            # log an error. Quit or continue?

            except ImportError as e:
                self.logger.error(e)
                pass            # problem importing

        self.logger.debug('Done loading plugins')
        return plugins

    @staticmethod
    def build_rules(rule_yaml, match_plugins, action_plugins):
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

    def run(self, args):
        """
        Load plugins and run with the configuration given in args
        :param args: Object containing program's parsed command line arguments
        :return: None
        """
        module_dir = os.path.dirname(__file__)
        self.match_plugins = self.load_plugins(os.path.join(module_dir, 'matchplugins/'))
        self.action_plugins = self.load_plugins(os.path.join(module_dir, 'actionplugins/'))

        if args['--list-plugins'] is True:
            print("\nAvailable Match Plugins:")
            for m in sorted(self.match_plugins):
                print(m)
            print("\nAvailable Action Plugins:")
            for a in sorted(self.action_plugins):
                print(a)
            sys.exit()

        rule_yaml = self.load_rules(args['RULEFILE'])
        rules = self.build_rules(rule_yaml, self.match_plugins, self.action_plugins)

        files_analyzed = 0
        files_matched = 0

        for cur_file in self.get_files(args['DIRECTORY']):
            self.logger.debug("Processing {0}".format(cur_file))
            files_analyzed += 1

            for ruleset in rules:
                if ruleset.matches_all_rules(cur_file):
                    files_matched += 1
                    # If the file matches all rules in the ruleset, do whatever
                    # actions the ruleset specifies. Stop processing if the
                    # ruleset says stop.
                    try:
                        ruleset.do_actions(cur_file, args['--dry-run'])
                    except StopProcessingException:
                        break

        self.logger.info("Files matched: {0}/{1}".format(files_matched, files_analyzed))
