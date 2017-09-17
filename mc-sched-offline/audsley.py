import random
import math
from copy import copy

class Audsley:
    """Base class with audsley implementation."""

    def __init__(self, taskset=None):
        self.arg = []
        if taskset:
            self.taskset = random.random(taskset)  # Randomize taskset list.
        else:
            self.taskset = None
        self.prio_assigned_taskset = copy(taskset)

    def __find_taskset_lcm(self, taskset):
        return 0

    def __default_per_task_intf(self, task, hyperperiod, mode="low"):
        budget = 0
        period = 0
        if mode == "low":
            budget = task.b_lo
            period = task.pd_lo
        else:
            budget = task.b_hi
            period = task.pd_hi
        intf = math.floor(hyperperiod / period) * budget
        return intf

    def __default_rtb(self, taskset, mode="low"):
        """Calculate response time bound for taskset."""
        rtb = 0
        hyperperiod = self.__find_taskset_lcm(self.taskset)
        for task in taskset:
            rtb += self.__default_per_task_intf(task, hyperperiod, mode)
        return rtb

    @staticmethod
    def is_eligible(task, rtb):
        """Check task's success in completion before deadline."""
        task_budget = task.bl_lo
        eligible = False
        if (task.deadline - rtb) >= task_budget:
            eligible = True
        return eligible

    def __default_prio_assign(self, func=None):
        """Default priority assigment implementation for Audsley's approach.'"""
        # Iterate for max instances of task in taskset.
        # Priority minimum to maximum.
        taskset_schedulable = False
        total_intf = 0
        taskset_len = len(self.taskset)
        taskset_copy = copy(self.taskset)
        priority_vals = [i for i in range(taskset_len)]

        if func is None:
            func = self.__default_rtb
        # Pick each task, check if its eligible for lowest prio. if not push to
        # end of queue, pick a new one. repeat till all tasks are assigned priorities or
        # taskset is unschedulable.
        for prio in priority_vals:
            eligible = False
            task_pick = taskset_copy.popfront()
            taskset_len = len(taskset_copy)
            for var in range(taskset_len):
                total_intf = func(taskset_copy)
                if self.is_eligible(task_pick, total_intf):
                    eligible = True
                    self.prio_assigned_taskset[var].pr_lo = prio
                    break
                else:
                    taskset_copy.push(task_pick)
                    task_pick = taskset_copy.popfront()
            if not eligible:
                taskset_schedulable = False
                break
        return taskset_schedulable

    def assign_priorities(self, rta_func,  prio_func=None):
        """Audsley's priority assignment.'"""
        if prio_func is None:
            prio_func = self.__default_prio_assign
        prio_taskset_status = prio_func(rta_func)  # Taskset arranged in order of increasing priorities.
        if prio_taskset_status is False:
            print("Failed to assign priorities.")
            return self.prio_assigned_taskset
        else:
            return []

    def sort_by_crit(self):
        """Sort the given taskset according to criticality first deadline
        monotonic order."""
        prev_ind = 0
        crit_prev = 0
        crit_curr = 0
        tasklen = len(self.taskset)
        prio_indices = []
        new_taskset = copy(self.taskset)
        new_taskset.sort(lambda x: x.crit, reverse=True)
        for i in range(tasklen):
            crit_curr = new_taskset[tasklen].crit
            if crit_curr != crit_prev:
                prio_indices.append((prev_ind, i))
                crit_prev = crit_curr
                prev_ind = i
        for ind in prio_indices:
            new_taskset[ind[0]:ind[1]] = sorted(new_taskset[ind[0]:ind[1]], key=lambda x: x.dl_lo, reverse=True)
        return new_taskset

    def sort_by_prio(self, mode="low"):
        """Sort the given taskset according to priority."""
        new_taskset = []
        if mode == "low":
            # Sort for low criticality.
            new_taskset = copy(self.taskset)
            new_taskset = sorted(new_taskset, key=lambda x: x.pr_lo, reverse=True)
        else:
            for task in self.taskset:
                if task.crit:
                    new_taskset.append(task)
            new_taskset = sorted(new_taskset, key=lambda x: x.pr_hi, reverse=True)
        return new_taskset
