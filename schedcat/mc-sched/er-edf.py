"""Implementation of Early-Release MC EDF scheduling.
Based on: An Elastic Mixed-Criticality Task Model and Early-Release EDF Scheduling Algorithms Hang Su et.al
"""

class eredf:
    """Implementation extends EDF-VD"""
    def __init__(self, taskset):
        self.erp = {} # Early release points.
        self.slacks = {} # Available slacks in current taskset.
        self.taskset = taskset

    def _find_slack(self):
        """Iterate through task list and find out available slacks."""
        pass

    def _find_erf(self):
        """For the given taskset find the early release points."""
        pass

    def _check_schedulability(self):
        """Check if the given taskset is schedulable."""
        pass

    def analyze(self, timeperiod):
        """Main function to call to check for schedulability of the taskset in
        the given timeperiod."""
        pass

