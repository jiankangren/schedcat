from task import task
import sys

class smc:
    """
    Implementation of static mixed criticality schedulability analysis.
    """
    def __init__(self, taskset):
        self.taskset = taskset
        self.sorted = False
        self.task_rtb_array = {}
        self.task_sorted_by_prio = None
        self.task_sorted_by_crit = None

    def __find_total_interference(taskset, crit):
        """Find the total interference created by given taskset."""
        if crit == "low":
            pass

    def __get_lcm(self, x, y):
        """Get lcm for given two variables."""

    
    def __get_hyperperiod(self):
        """Get the task hyperperiod."""
        for task in self.taskset:
            pass

    def smc_rtb(self):
        taskset_len = len(self.task_sorted_by_prio)
        if not sorted:
            self.task_sorted_by_prio = self.__sort_by_prio(self.taskset)
        for i in range(taskset_len):
            task = self.task_sorted_by_prio[i]
            segment = self.task_sorted_by_prio[i+1:]
            response_time = task.bd_hi +  self.__find_total_interference(segment, task.crit)
            

