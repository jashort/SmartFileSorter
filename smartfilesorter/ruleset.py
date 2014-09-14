import logging
import os


class RuleSet(object):
    """
    A ruleset is a collection of associated match rules and actions. For example:

    - file-extension-is: .log
    - filename-starts-with: ex
    - move-to: /archive/logs/

    Match rules are a boolean AND operation -- all must match. Actions are all applied in order.
    """
    def __init__(self, yaml_section, match_plugins={}, action_plugins={}):
        self.logger = logging.getLogger('SmartFileSorter.RuleSet')
        self.name = yaml_section['name']
        self.logger.debug("Creating ruleset: {0}".format(self.name))
        self.match_rules = []
        self.action_rules = []
        self.available_match_plugins = match_plugins
        self.available_action_plugins = action_plugins

        self.add_action_rules(yaml_section['action'])
        self.add_match_rules(yaml_section['match'])

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Ruleset: {0}'.format(self.name)

    def add_match_rule(self, rule_config_name):
        """
        Adds the given match rule to this ruleset's match rules
        :param rule_config_name: Plugin's config name
        :return: None
        """
        self.logger.debug('Adding match rule {0}'.format(rule_config_name))
        # Handle rules that are just a string, like 'stop-processing'
        if type(rule_config_name) == str:
            self.add_rule(rule_config_name, None, self.available_match_plugins, self.match_rules)
        # Handle rules built from key-value pairs
        elif type(rule_config_name) == dict:
            for r in rule_config_name:
                self.add_rule(r, rule_config_name[r], self.available_match_plugins, self.match_rules)

    def add_action_rule(self, rule_config_name):
        """
        Adds the given action rule to this ruleset's action rules
        :param rule_config_name:
        :return:
        """
        self.logger.debug('Adding action rule {0}'.format(rule_config_name))
        # Handle rules that are just a string, like 'stop-processing'
        if type(rule_config_name) == str:
            self.add_rule(rule_config_name, None, self.available_action_plugins, self.action_rules)
        # Handle rules built from key-value pairs
        elif type(rule_config_name) == dict:
            for r in rule_config_name:
                self.add_rule(r, rule_config_name[r], self.available_action_plugins, self.action_rules)

    def add_rule(self, config_name, value, plugins, destination):
        """
        Adds a rule. Use add_action_rule or add_match_rule instead
        :param rule_wrapper: Rule wrapper class (ActionRule or MatchRule)
        :param config_name: config_name of the plugin to add
        :param value: configuration information for the rule
        :param plugins: list of all available plugins
        :param destination: list to append plugin to (self.action_rules or self.match_rules)
        :return:
        """
        if config_name in plugins:
            rule = plugins[config_name](value)
            destination.append(rule)
        else:
            self.logger.error("Plugin with config_name {0} not found".format(config_name))
            raise IndexError("Plugin with config_name {0} not found".format(config_name))

    def matches_all_rules(self, target_filename):
        """
        Returns true if the given file matches all the rules in this ruleset.
        :param target_filename:
        :return: boolean
        """

        for rule in self.match_rules:
            if rule.test(target_filename) is False:
                return False

        self.logger.info('{0}: {1} - {2}'.format(self.name,
                                                 os.path.basename(target_filename),
                                                 'Match'))
        return True

    def do_actions(self, target_filename, dry_run=False):
        """
        Runs all the given action rules in this ruleset on target_filename
        :param target_filename:
        :retrn: filename Filename and path after any actions have been completed
\        """
        for rule in self.action_rules:
                target_filename = rule.do_action(target_filename, dry_run)

        return target_filename

    def add_action_rules(self, action_rules):
        """
        Add the given action rules to the ruleset. Handles single rules or a list of rules.
        :param action_rules: Object representing YAML section from config file
        :return:

        Example action_rules object:
            ['print-file-info', {'move-to': '/tmp'}, 'stop-processing']
        """
        if type(action_rules) == list:
            for r in action_rules:
                self.add_action_rule(r)
        else:
            # Handle a single rule being passed in that's not in a list
            self.add_action_rule(action_rules)

    def add_match_rules(self, match_rules):
        """
        Add the given match rules to the ruleset. Handles single rules or a list of rules.
        :param match_rules: Object representing YAML section from config file
        :return:

        Example match_rules object:
            [{'filename-starts-with': 'abc'}, {'filename-ends-with': 'xyz']
        """
        if type(match_rules) == list:
            for r in match_rules:
                self.add_match_rule(r)
        else:
            # Handle a single rule being passed in that's not in a list
            self.add_match_rule(match_rules)
