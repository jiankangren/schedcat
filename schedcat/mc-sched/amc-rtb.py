#AMC Priority assignment based on: 
#Response-Time Analysis for Mixed Criticality Systems - S.K. Baruah et.al.
#Link: https://www-users.cs.york.ac.uk/burns/RTSS.pdf

from task import task # Abstract representation of task.
from audsley import audsley
import sys

class amc_rtb(audsley):
    """amc-rtb based schedulability test and priority assignment."""
    def __init__(self, taskset):
        super(amc_rtb, self).__init__(taskset)
    
    def __amc_rtb_low(self, task):
        """Calculate the response time of low criticality tasks."""
        R_lo = task.b_lo
        for ind in self.taskset:
            if ind != task:
                R_lo += math.ceil(R_lo/ind.pr_lo) * ind.b_lo
        return R_lo
    
    def __amc_rtb_high(self, R_initial):
        """Calculate the response time of the high criticality tasks."""
        R_hi = R_initial
        for ind in self.taskset:
            if (ind.prio == 1) and (ind != task):
                R_hi += math.ceil(R_hi/ind.pr_hi) * ind.b_hi
        return R_hi

    def dbf_amc_rtb(self, task):
        """Demand bound function for amc-rtb."""
        rtb = task.b_hi
        rtb += self.__amc_rtb_low(task)
        if task.crit == 1:
            rtb += self.__amc_rtb_high(task)
        return rtb
            

    def check_schedulability(self, task):
        """Check schedulability based on amc-rtb """
        

    def assign_priority(self):
        """Priority assignment based on Audsley's approach."""
        pass
