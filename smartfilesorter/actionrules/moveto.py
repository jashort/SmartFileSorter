from actionrule import ActionRule
import shutil
import os


class MoveTo(ActionRule):
    """
    Moves a given file to a new directory
    """
    config_name = 'move-to'

    def __init__(self, destination):
        super(MoveTo, self).__init__(destination)
        self.destination = destination
        self.continue_processing = False

    def action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: boolean - Continue processing rules for this file?
        """
        if dry_run is False:
            base_name = os.path.basename(target)
            new_name = os.path.join(self.destination, base_name)

            if not os.path.exists(new_name):
                try:
                    shutil.move(target, self.destination)
                except IOError:
                    self.logger.error("Error moving file {0} to {1}".format(target, self.destination))
                    raise IOError
            else:
                self.logger.error("Destination file already exists: {0}".format(new_name))
                raise IOError


        return self.continue_processing