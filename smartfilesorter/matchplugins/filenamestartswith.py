import os


class FilenameStartsWith(object):
    """
    Tests if a filename starts with these characters. File path and extension are ignored.
    """
    config_name = 'filename-starts-with'

    def __init__(self, match_value, case_sensitive=False):
        """
        :param match_value: A string containing characters to match at the start of a filename
        """
        self.match_value = match_value
        self.case_sensitive = case_sensitive

    def test(self, target):
        """
        :param target: Full path and filename
        :return: boolean
        """
        path, filename = os.path.split(target)
        if self.case_sensitive:
            return filename.startswith(self.match_value)
        else:
            return filename.lower().startswith(self.match_value.lower())
