from actionrule import ActionRule
from actionrule import StopProcessingException


class StopProcessing(ActionRule):
    """
    Stop processing rules and actions for the given file
    """
    config_name = 'stop-processing'

    def __init__(self, value=None):
        # Nothing to do here - just call the parent __init__ function for logging
        super(StopProcessing, self).__init__(value)
        self.continue_processing = False

    def action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: None
        """
        raise StopProcessingException()
