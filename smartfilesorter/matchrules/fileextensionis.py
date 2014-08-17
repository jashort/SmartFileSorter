from matchrule import MatchRule
import os


class FileExtensionIs(MatchRule):
    """
    Tests if a given file has one of the defined extensions.
    """
    config_name = 'file-extension-is'

    def __init__(self, match_value):
        """
        :param match_value: A string containing one or more file extensions separated by spaces. Ex: ".log .txt"
        """
        super(FileExtensionIs, self).__init__()
        self.config_name = 'file-extension-is'
        self.extensions = match_value.split(' ')
        self.match_value = match_value

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
