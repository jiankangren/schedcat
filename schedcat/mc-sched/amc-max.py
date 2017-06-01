from task import task # Abstract representation of task.
from audsley import audsley
import sys

class amc_max(audsley):
    """AMC-max based priority assignment."""

    def __init__(self, taskset):
        self.taskset = taskset
        super(amc_max, self).__init__(taskset)

    def __amc_max_low(self, task, taskset=None):
        """Response time for low criticality tasks."""
        R_lo = task.b_lo
        for ind in self.taskset:
            if ind != task:
                R_lo += math.ceil(R_lo/ind.pr_lo) * ind.b_lo
        return R_lo

    def __amc_max_high(self, task,R_initial, taskset=None):
        """Response time for high criticality tasks."""
        R_hi = R_initial
        if taskset == None:
            taskset_cp = copy(self.taskset)
        else:
            taskset_cp = taskset
        for ind in taskset_cp:
            if (ind.crit == 1) and (ind != task):
                
        

    def dbf_amc_max(self, task, taskset):
        """Demand bound function for amc max."""
        rtb = task.b_hi
        rtb += self.__amc_max_low(task, taskset)
        if task.crit > 0:
            rtb += self.__amc_rtb_high(task, rtb, taskset)
        return rtb

    def check_schedulability(self, task, taskset=None):
        """Check schedulability for the given taskset."""
        rtb = 0.0
        status = False
        rtb = self.dbf_amc_max(task, taskset)
        if task.crit > 0:
            rtb += self.dfb_amc_max(task, taskset)
        return status

    def priority_assignment(self):
        """Uses audsley's approach to priority assignment and returns priority
        values or an empty set in case of failure."""
        pass



