from actionrule import ActionRule
import shutil
import os


class RenameTo(ActionRule):
    """
    Renames a given file. Performs a case sensitive search and replace on the filename, then renames it.
    """
    config_name = 'rename-to'

    def __init__(self, value):
        super(RenameTo, self).__init__(value)
        match, replace_with = value.strip().split('>>')
        self.match = match.strip()
        self.replace_with = replace_with.strip()

    def action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: filename: Full path and filename after action completes
        """
        new_filename = target

        if dry_run is False:
            original_path = os.path.dirname(target)
            original_filename, original_extension = os.path.splitext(os.path.basename(target))

            new_filename = os.path.join(original_path,
                                        original_filename.replace(self.match, self.replace_with) +
                                        original_extension)
            self.logger.debug("Moving {0} to {1}".format(target, new_filename))

            if not os.path.exists(new_filename):
                try:
                    shutil.move(target, new_filename)
                except IOError:
                    self.logger.error("Error renaming file {0} to {1}".format(target, new_filename))
                    raise IOError
            else:
                self.logger.error("Destination file already exists: {0}".format(new_filename))
                raise IOError

        return new_filename