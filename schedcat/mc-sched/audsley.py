import random
import math
from task import task # Abstract representation of task with two crit level.
from taskset import taskset

class audsley:
    """Base class with audsley implementation."""

    def __init__(self, taskset = None):
        self.arg = []
        if taskset:
            self.taskset = random.random(taskset) #Randomize taskset list.
        else:
            self.taskset = None

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

    def is_eligible(self, task, rtb):
        """Check task's success in completion before deadline."""
        task_budget = task.bl_lo
        eligible = False
        if (task.deadline - rtb) >= task_budget:
            eligible = True
        return eligible

    def __default_prio_assign(self):
        """Default priority assigment implementation for Audsley's approach.'"""
        # Iterate for max instances of task in taskset.
        # Priority minimum to maximum.
        taskset_schedulable = True
        total_intf = 0
        taskset_len = len(self.taskset)
        taskset_copy = copy(self.taskset)
        priority_vals = [i for i in range(taskset_len)]
        #Pick each task, check if its eligible for lowest prio. if not push to
        #end of queue, pick a new one. repeat till all tasks are assigned prio
        #-rities or taskset is unschedulable.
        for prio in priority_vals:
            eligible = False
            task_pick = taskset_copy.popfront()
            takset_len = len(taskset_copy)
            for var in range(taskset_len):
                total_intf = self.__default_rtb(taskset_copy)
                if(self.is_eligible(task, total_intf)):
                    eligible = True
                    task.pr_lo = prio
                    break
                else:
                    taskset_copy.push(task_pick)
                    task_pick = taskset_copy.popfront()
            if eligible == False:
                taskset_schedulable = False
                break
        return taskset_schedulable

    def assign_priorities(self, func = self.__default_prio_assign):
        """Audsley's priority assigment.'"""
        prio_taskset = None # Taskset arranged in order of increasing priorities.
        try:
            pass
        except ValueError:
            print("Failed to assign priorities to taskset.\n")
        return prio_taskset

    def sort_by_crit(self):
        """Sort the given taskset according to criticality first deadline
        monotonic order."""
        prev_ind  = 0
        prio_prev = 0
        prio_curr = 0
        tasklen = len(self.taskset)
        prio_indices = []
        new_tskset = copy(self.taskset)
        new_tskset.sort(lambda x: x.crit, reverse=True)
        for i in range(tasklen):
            prio_curr = new_tskset[tasklen].pr_lo
            if(prio_curr != prio_prev):
                prio_indices.append((prev_ind, i))
                prio_prev = prio_curr
                prev_ind = i
        for ind in prio_indices:
            new_tskset[ind[0]:ind[1]] = sorted(new_tskset[ind[0]:ind[1]],key=lambda x: x.dl_lo, reverse=True)
        return new_tskset

    def sort_by_prio(self, mode=0):
        """Sort the given taskset according to priority."""
        new_tskset = []
        if mode == 0:
            # Sort for low criticality.
            new_tskset = copy(self.taskset)
            new_tskset = sorted(new_tskset, lambda x: x.pr_lo, reverse=True)
        else:
            for task in self.taskset:
                if task.crit:
                    new_tskset.append(task)
            new_tskset = sorted(new_tskset, lambda x: x.pr_hi, reverse=True)
        return new_tskset



    

