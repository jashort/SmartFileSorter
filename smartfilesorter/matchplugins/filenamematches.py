import os
import re


class FilenameMatches(object):
    """
    Tests if a filename matches the given regular expression. File path and extension are ignored.
    """
    config_name = 'filename-matches'

    def __init__(self, match_value):
        """
        :param match_value: A string containing characters to match anywhere in a filename
        """
        super(FilenameMatches, self).__init__()
        self.match_value = match_value

    def test(self, target):
        """
        :param target: Full path and filename
        :return: boolean
        """
        path, filename = os.path.split(target)
        filename, extension = os.path.splitext(filename)

        if re.match(self.match_value, filename) is not None:
            return True
        else:
            return False
