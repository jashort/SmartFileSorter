import os
import logging


class PrintFileInfo(object):
    """
    Prints the filename and size to stdout. Mostly used for testing.
    """
    config_name = 'print-file-info'

    def __init__(self, value=None):
        self.value = value
        self.logger = logging.getLogger(__name__)

    def do_action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: filename: Full path and filename after action completes
        """
        if dry_run is False:
            try:
                filename = os.path.basename(target)
                size = os.path.getsize(target)
                print("{0}\t{1}".format(filename, size))
            except OSError:
                self.logger.error("Error getting size for file: {0}".format(target))

        return target
