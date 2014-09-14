import os


class FilenameContains(object):
    """
    Tests if a filename contains these characters. File path and extension are ignored.
    """
    config_name = 'filename-contains'

    def __init__(self, match_value, case_sensitive=False):
        """
        :param match_value: A string containing characters to match anywhere in a filename
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
            return self.match_value in filename
        else:
            return self.match_value.lower() in filename.lower()
