"""
Classes representing rules that do various things to files. Example:
    >>> r = MoveTo('/tmp')

"""

import logging
import os


class StopProcessingException(Exception):
    """
    Exception indicates processing should stop for the current file in the current ruleset
    """
    pass


class ActionRule(object):
    """
    Base class for file matching rules. Handles logging. Shouldn't be used directly.
    """
    config_name = None                       # Name as it appears in the rule configuration file
                                             # Must be unique across plugins

    def __init__(self, value):
        self.value = value                   # Where to copy/move file to (if applicable)
        self.logger = logging.getLogger('SmartFileSorter.ActionRule')
        self.logger.debug("Created action rule {0}: {1}".format(self.config_name, self.value))

    def __str__(self):
        return '{0}: {1}'.format(self.config_name, self.value)

    def do_action(self, target, dry_run=False):
        """
        :param target: Full path and filename to test against this rule
        :param dry_run: Actually perform the action if False, just log messages if True
        :return: filename: Full path and filename after action (e.g., if the file was moved)
        """
        if dry_run is False:
            self.logger.debug("Performing action {0} on {1}".format(self.config_name, target))
        else:
            self.logger.debug("Dry-run: Skipping action {0} on {1}".format(self.config_name, target))

        new_filename = self.action(target, dry_run)
        self.logger.debug("Continue processing? {0}".format(new_filename))
        return new_filename

    def action(self, target):
        raise NotImplementedError


