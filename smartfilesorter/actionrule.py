"""
Classes representing rules that do various things to files. Example:
    >>> r = MoveTo('/tmp')

"""

import logging
import os


class ActionRule(object):
    """
    Base class for file matching rules. Handles logging. Shouldn't be used directly.
    """
    config_name = None                       # Name as it appears in the rule configuration file
                                             # Must be unique across plugins

    def __init__(self, value):
        self.value = value                   # Where to copy/move file to (if applicable)
        self.continue_processing = False     # Continue processing rules after performing
                                             # this action?
        self.logger = logging.getLogger('SmartFileSorter.ActionRule')
        self.logger.debug("Created action rule {0}: {1}".format(self.config_name, self.value))

    def __str__(self):
        return '{0}: {1}'.format(self.config_name, self.value)

    def do_action(self, target, dry_run=False):
        """
        :param target: Full path and filename to test against this rule
        :param dry_run: Actually perform the action if False, just log messages if True
        :return: boolean, True if processing should continue
        """
        self.logger.debug("Performing action {0}: {1} on {2}".format(self.config_name, self.value, target))
        result = self.action(target, dry_run)
        self.logger.debug("Result: {0}".format(result))
        return result

    def action(self, target):
        raise NotImplementedError


