from actionrule import ActionRule


class ContinueProcessing(ActionRule):
    """
    Continue processing rules and actions for the given file
    """
    config_name = 'continue-processing'

    def __init__(self, value=None):
        # Nothing to do here - just call the parent __init__ function for logging
        super(ContinueProcessing, self).__init__(value)
        self.continue_processing = True

    def action(self, target, dry_run=False):
        """
        :param target: Full path and filename
        :param dry_run: True - don't actually perform action. False: perform action. No effect for this rule.
        :return: boolean - Continue processing rules for this file?
        """
        return self.continue_processing