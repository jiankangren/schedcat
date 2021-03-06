# AMC Priority assignment based on:
# Response-Time Analysis for Mixed Criticality Systems - S.K. Baruah et.al.
# Link: https://www-users.cs.york.ac.uk/burns/RTSS.pdf

from audsley import Audsley
import math


class AmcRtb(Audsley):
    """amc-rtb based schedulability test and priority assignment."""

    def __init__(self, taskset):
        super(AmcRtb, self).__init__(taskset)

    def __amc_ri_low(self, task, taskset=None):
        """Calculate the response time of low criticality tasks."""
        R_lo = task.b_lo
        for ind in taskset:
            if ind != task:
                R_lo += math.ceil(R_lo / ind.pr_lo) * ind.b_lo
        return R_lo

    def __amc_ri_high(self, task, r_initial, taskset=None):
        """Calculate the response time of the high criticality tasks."""
        R_hi = r_initial
        for ind in taskset:
            if (ind.crit == 1) and (ind != task):
                R_hi += math.ceil(R_hi / ind.pr_hi) * ind.b_hi
        return R_hi

    def dbf_amc_rtb(self, task, taskset=None):
        """Demand bound function for amc-rtb."""
        rtb = task.b_hi
        rtb += self.__amc_ri_low(task, taskset)
        if task.crit == 1:
            rtb += self.__amc_ri_high(task, rtb, taskset)
        return rtb

    def amc_rtb_rta(self, task, taskset=None, debug=False):
        """Check schedulability based on amc-rtb """
        Ri = self.dbf_amc_rtb(task, taskset)
        if debug:
            print("Response time for task :", Ri)
        return Ri

    def assign_priority(self):
        """Priority assignment based on Audsley's approach."""
        try:
            prio_assigned = self.assign_priorities(self.amc_rtb_rta)
        except ValueError as vs:
            print("Failed to assign priorities: Taskset not schedulable.: \n", vs)
            raise ValueError("schedulability test failed: Value error.\n")  # Throw for test.
        return prio_assigned
