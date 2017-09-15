import sys
from edfvd import EdfVD


class service_adaptation(EdfVD):
    """Service adaptation for EDF VD"""
    def __init__(self, taskset):
        super(service_adaptation, self).__init__()
        self.taskset = taskset

    def schedulability_check_sa(self):
        self.schedulability_check()

    def calculate_recovery_time(self):
        """Calculate recovery period to transition back to low criticality."""
        pass
