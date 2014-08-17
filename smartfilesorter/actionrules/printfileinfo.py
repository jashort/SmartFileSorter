from actionrule import ActionRule
import os


class PrintFileInfo(ActionRule):
    """
    Prints the filename and size to stdout. Mostly used for testing.
    """
    config_name = 'print-file-info'

    def __init__(self, value=None):
        # Nothing to do here - just call the parent __init__ function for logging
        super(PrintFileInfo, self).__init__(value)
        self.continue_processing = True

    def action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: boolean - Continue processing rules for this file?
        """
        if dry_run is False:
            try:
                filename = os.path.basename(target)
                size = os.path.getsize(target)
                print("{0}\t{1}".format(filename, size))
            except IOError:
                self.logger.error("Error getting size for file: {0}".format(target))

        return self.continue_processing