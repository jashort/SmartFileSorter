import os


class FileExtensionIs(object):
    """
    Tests if a given file has one of the defined extensions.
    """
    config_name = 'file-extension-is'

    def __init__(self, match_value, case_sensitive=False):
        """
        :param match_value: A string containing one or more file extensions separated by spaces. Ex: ".log .txt"
        """
        self.config_name = 'file-extension-is'
        self.extensions = match_value.split(' ')
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
            return extension in self.extensions
        else:
            return extension.lower() in [e.lower() for e in self.extensions]
