from taskset import taskset
from task import task
from amc_rtb import amc_rtb
import math

class bailout(amc_rtb):
    """Offline support for bailout algorithm to recover budget from high crit tasks."""
    self.__init__(self, taskset):
        self.taskset = taskset
        self.alpha = 1 # Value to multiple all high crit task low budget.
        self.c_bu_array = {} # save augmented budget for each high crit task.

    self.__binary_search_alpha(self):
        """Do a binary search to determine optimal alpha value."""
        alpha_start = 1
        alpha_end = 1
        high_taskset = self.taskset.get_task_by_crit("high")
        for task in high_taskset:
            alpha_end = max(task.c_hi/task.c_lo, alpha_end)
        
        for alpha in range(alpha_start, alpha_end, 0.2):
            # Do a binary search on the alpha indexes available.
            pass


    self.__is_task_schedulable(self):
        """Check if the task is schedulable under audsley approach."""
        return self.check_taskset_schedulability()


