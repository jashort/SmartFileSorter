"""
Classes representing rules that test various aspects of a file's name. Example:
    >>> r = FilenameStartsWith('test')
    >>> r.matches('/tmp/test_file.log')
    True
    >>> r.matches('/tmp/something_else.txt')
    False

"""

import logging
import os


class MatchRule(object):
    """
    Base class for file matching rules. Handles logging. Shouldn't be used directly.
    """
    config_name = None                  # Name as it appears in the rule configuration file
                                        # Must be unique across plugins

    def __init__(self):
        self.match_value = 'Generic'    # String to match - different for each rule
        self.case_sensitive = False     # Case sensitive matches? Default to false, but can be
                                        # set per rule
        self.logger = logging.getLogger('SmartFileSorter.MatchRule')
        self.logger.debug("Created match rule {0}: {1}".format(self.config_name, self.match_value))

    def __str__(self):
        return '{0}: {1}'.format(self.config_name, self.match_value)

    def matches(self, target):
        """
        :param target: Full path and filename to test against this rule
        :return: boolean, True if filename matches this rule
        """
        self.logger.debug("Running test {0}: {1}".format(self.config_name, self.match_value))
        result = self.test(target)
        self.logger.debug("Result: {0}".format(result))
        return result

    def test(self, target):
        raise NotImplementedError


