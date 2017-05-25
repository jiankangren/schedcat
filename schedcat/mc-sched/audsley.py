import random
import math
from task import task # Abstract representation of task with two crit level.

class audsley:
    """Base class with audsley implementation."""

    def __init__(self, taskset = None):
        self.arg = []
        if taskset:
            self.taskset = random.random(taskset) #Randomize taskset list.
        else:
            self.taskset = None

    def __pick_next_task(self):
        pass

    def __default_per_task_intf(self, task, hyperperiod, mode="low"):
        budget = None
        period = None
        if mode == "low":
            budget = task.b_lo
            period = task.pd_lo
        else:
            budget = task.b_hi
            period = task.pd_hi
        intf = math.floor(hyperperiod/period) * budget
        return intf

    def __default_rtb(self, taskset, mode = "low"):
        """Calculate response time bound for taskset."""
        rtb = 0
        hyperperiod = self.__find_taskset_lcm(taskset)
        for task in taskset:
            rtb += self.__default_per_task_intf(task, hyperperiod, mode); 
        return rtb

    def __default_prio_assign(self):
        """Default priority assigment implementation for Audsley's approach.'"""
        for i in range(len(self.taskset)):
            # Iterate for max instances of task in taskset.
            # Priority minimum to maximum.
            total_intf = 0
            priority_vals = [i for i in range(len(self.taskset))]
            for task in self.taskset:
                total_intf = self.__default_rtb

    def assign_priorities(self, func = self.__default_prio_assign):
        """Audsley's priority assigment.'"""
        prio_taskset = None # Taskset arranged in order of increasing priorities.
        try:
            pass
        except ValueError:
            print("Failed to assign priorities to taskset.\n")
        return prio_taskset
