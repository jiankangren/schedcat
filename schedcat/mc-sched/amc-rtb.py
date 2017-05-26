#AMC Priority assignment based on: 
#Response-Time Analysis for Mixed Criticality Systems - S.K. Baruah et.al.
#Link: https://www-users.cs.york.ac.uk/burns/RTSS.pdf

from task import task # Abstract representation of task.
from audsley import audsley
import sys

class amc_rtb(audsley):
    """amc-rtb based schedulability test and priority assignment."""
    def __init__(self, taskset):
        self.taskset = taskset


    def dbf_amc_rtb(self):
        """Demand bound function for amc-rtb."""
        pass

    def check_schedulability(self, task):
        """Check schedulability based on amc-rtb """
        pass

    def assign_priority(self):
        """Priority assignment based on Audsley's approach."""
        pass
