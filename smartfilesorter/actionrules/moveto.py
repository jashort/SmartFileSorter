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
        self.destination = os.path.expanduser(destination)
        self.continue_processing = False

    def action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: filename: Full path and filename after action completes
        """
        new_filename = target

        if dry_run is False:
            base_name = os.path.basename(target)
            new_filename = os.path.join(self.destination, base_name)
            self.logger.debug("Moving {0} to {1}".format(target, new_filename))

            if not os.path.exists(new_filename):
                try:
                    shutil.move(target, self.destination)
                except IOError:
                    self.logger.error("Error moving file {0} to {1}".format(target, self.destination))
                    raise IOError
            else:
                self.logger.error("Destination file already exists: {0}".format(new_filename))
                raise IOError


        return new_filename