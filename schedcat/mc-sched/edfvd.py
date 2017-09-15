from taskset import Taskset


class EdfVD:
    """Implementation of edfvd schedulability test."""
    def __init__(self, file=None, taskset=None):
        self.file = file
        self.taskset = taskset

    def schedulability_check(self):

        schedulable = True
        U_h_h = self.taskset.get_high_crit_high_util()
        U_l_l = self.taskset.get_low_crit_low_util()
        U_h_l = self.taskset.get_high_crit_low_util()

        x = U_h_l/(1 - U_l_l)

        if x*U_l_l + U_h_h <= 1:
            for task in self.taskset:
                task.t_lo = x * task.t_hi
        else:
            schedulable = False
        return schedulable

    def get_taskset(self):
        return self.taskset
