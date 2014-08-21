from actionrule import ActionRule
import shutil
import os
import re


class RenameTo(ActionRule):
    """
    Renames a given file. Performs a case sensitive search and replace on the filename, then renames it.
    Also supports regular expressions.
    """
    config_name = 'rename-to'

    def __init__(self, parameters):
        super(RenameTo, self).__init__(parameters)
        if 'match' in parameters:
            self.match = parameters['match']
        else:
            raise ValueError('rename-to rule must have parameter "match"')
        if 'replace-with' in parameters:
            if parameters['replace-with'] is None:
                self.replace_with = ''
            else:
                self.replace_with = parameters['replace-with']
        else:
            raise ValueError('rename-to rule must have "replace-with" parameter')

    def action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: filename: Full path and filename after action completes
        """
        original_path = os.path.dirname(target)
        original_filename, original_extension = os.path.splitext(os.path.basename(target))

        new_filename = re.sub(self.match, self.replace_with, original_filename) + original_extension
        destination = os.path.join(original_path, new_filename)

        if dry_run is True:
            self.logger.debug("Dry run: Skipping rename {0} to {1}".format(target, new_filename))
            return target
        else:
            self.logger.debug("Renaming {0} to {1}".format(original_filename + original_extension,
                                                           new_filename + original_extension))

            if not os.path.exists(destination):
                try:
                    shutil.move(target, destination)
                except IOError:
                    self.logger.error("Error renaming file {0} to {1}".format(target, new_filename))
                    raise IOError
            else:
                self.logger.error("Destination file already exists: {0}".format(new_filename))
                raise IOError

        return destination