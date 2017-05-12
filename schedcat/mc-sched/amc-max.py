from audsley import audsley
import sys

class amc_max(audsley):
    """AMC-max based priority assignment."""

    def __init__(self, taskset):
        self.taskset = taskset

    def dbf_max(self):
        """Demand bound function for amc max."""
        pass

    def check_schedulability(self):
        """Check schedulability for the given taskset."""
        pass

    def priority_assignment(self):
        """Uses audsley's approach to priority assignment and returns priority
        values or an empty set in case of failure."""
        pass



