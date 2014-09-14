from smartfilesorter.smartfilesorter import StopProcessingException


class StopProcessing(object):
    """
    Stop processing rules and actions for the given file
    """
    config_name = 'stop-processing'

    def __init__(self, value=None):
        # Nothing to do here - just call the parent __init__ function for logging
        self.continue_processing = False

    @staticmethod
    def do_action(target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: None
        """
        raise StopProcessingException()
