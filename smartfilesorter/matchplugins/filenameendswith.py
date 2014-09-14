import os


class FilenameEndsWith(object):
    """
    Tests if a filename ends with these characters. File path and extension are ignored.
    """
    config_name = 'filename-ends-with'

    def __init__(self, match_value, case_sensitive=False):
        """
        :param match_value: A string containing characters to match at the end of a filename
        """
        self.match_value = match_value
        self.case_sensitive = case_sensitive

    def test(self, target):
        """
        :param target: Full path and filename
        :return: boolean
        """
        path, filename = os.path.split(target)
        filename, extension = os.path.splitext(filename)
        if self.case_sensitive:
            return filename.endswith(self.match_value)
        else:
            return filename.lower().endswith(self.match_value.lower())
