import shutil
import os
import logging


class MoveTo(object):
    """
    Moves a given file to a new directory
    """
    config_name = 'move-to'

    def __init__(self, destination):
        self.destination = os.path.expanduser(destination)
        self.continue_processing = False
        self.logger = logging.getLogger(__name__)

    def do_action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action.
        :return: filename: Full path and filename after action completes
        """
        # Get full path to the file in the destination directory
        new_filename = os.path.join(self.destination, os.path.basename(target))

        # If the file exists in the destination directory, append _NNN to the name where NNN is
        # a zero padded number. Starts at _001
        while os.path.exists(new_filename):
            # if filename ends in _NNN, start at that number
            filename, extension = os.path.splitext(os.path.basename(new_filename))
            if filename[-4] == '_' and filename[-3:].isdigit():
                # Split the number off the filename and increment it, handle suffixes longer than 3 numbers
                current = filename.split('_')[-1]
                filename_root = filename[0:-len(current)-1]
                current = int(current) + 1
                new_filename = os.path.join(self.destination,
                                            (filename_root +
                                             "_{0:03d}".format(current) +
                                             extension))
            else:
                # No number suffix found in the filename, just start at _001
                new_filename = os.path.join(self.destination,
                                            (filename + "_001" + extension))

        if dry_run is False:
            self.logger.debug("Moving {0} to {1}".format(target, new_filename))

            if not os.path.exists(new_filename):
                try:
                    shutil.move(target, new_filename)
                except IOError:
                    self.logger.error("Error moving file {0} to {1}".format(target, self.destination))
                    raise IOError
            else:
                self.logger.error("Destination file already exists: {0}".format(new_filename))
                raise IOError

            return new_filename

        else:
            self.logger.debug("Dry run. Skipping move {0} to {1}".format(target, new_filename))
            return target
