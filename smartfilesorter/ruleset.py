import logging


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

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Ruleset: {0}'.format(self.name)

    def add_match_rule(self, config_name, value):
        self.logger.debug('Adding match rule {0}: {1}'.format(config_name, value))

        self.add_rule(config_name, value, self.available_match_plugins, self.match_rules)

    def add_action_rule(self, config_name, value=None):
        self.logger.debug('Adding action rule {0}: {1}'.format(config_name, value))
        self.add_rule(config_name, value, self.available_action_plugins, self.action_rules)

    def add_rule(self, config_name, value, plugins, destination):
        self.logger.debug('Adding rule {0}: {1}'.format(config_name, value))

        if config_name in plugins:
            destination.append(plugins[config_name](value))
        else:
            self.logger.error("Plugin with config_name {0} not found".format(config_name))
            raise IndexError("Plugin with config_name {0} not found".format(config_name))


