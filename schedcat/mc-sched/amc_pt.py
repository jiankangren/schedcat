import amc_rtb as AmcRtb
from taskset import Taskset
from copy import copy
import math


class ptamc(AmcRtb):
    
    def __init__(self, folder, file):
        self.taskset = Taskset()
        self.processed_taskset = Taskset()
        self.file = folder + '/' + file
        self.pt_array = []

    def __load_from_json(self, file = None):
        """Load taskset from json save."""
        try:
            if file is None:
                file = self.file
            taskset.generate_taskset_from_json(file)
        except IOError:
            print("Error opening file {0}.\n".format(file))
    
    def __assign_priorities(self):
        """Use amc-rtb approach to assign priority."""
        self.taskset = self.assign_priorities(self.taskset)

    def __get_lo_crit_response_time(self, task):
        """get worst case response time in low crit mode."""
        R_i_lo = task.c_lo
        high_prio_tasks = self.taskset.get_high_prio(task)
        for t in high_prio_tasks:
            R_i_lo += math.ceil(R_i_lo/t.t_lo) * t.c_lo
        return R_i_lo

    def __get_max_blocking(self, task, mode='normal'):
        """Determine the maximum blocking encountered by task in mode."""
        B_i = 0
        if mode == 'normal':
            interfer_tasks = self.taskset.get_taskset_low_crit_low_prio(task)
            for t in interfer_tasks:
                if self.pt_array[task.index] < self.pt_array[t.index]:
                    B_i = max(B_i, t.c_lo)
        elif mode == 'high':
            interfer_tasks = self.taskset.get_taskset_high_crit_low_prio(task)
            for t in interfer_tasks:
                if self.pt_array[task.index] < self.pt_array[t.index]:
                    B_i = max(B_i, t.c_hi)
        return B_i

    def __get_hi_crit_response_time(self, task):
        """Get worst case response time in high crit mode."""
        R_i_hi = task.c_hi
        high_prio_tasks = self.taskset.get_taskset_low_crit_high_prio(task)
        for t in high_prio_tasks:
            R_i_hi += math.ceil(R_i_hi/t.t_hi) * t.c_lo
        return R_i_hi
    
    def __get_transition_response_time(self, task):
        """Get the worst case response time for task in crit transition."""

        # First find the level i Busy Period in low crit mode.

        # tasks with priority greater than or equal to task.
        taskset_hep = self.taskset.get_high_equal_prio_tasks(task)
        LBP_i_lo = B_i_lo
        for t in taskset_hep:
            LBP_i_lo += math.ceil(LBP_i_lo/t.t_lo) * t.c_lo
        
        R_i_tran = 0
        for q in range(int(math.floor(LBP_i_lo/task.t_lo))):
            R_i_trans = max(R_i_trans, self.__get_transition_response_time(task, q))
        return R_i_trans

    def __get_transition_response_time(self, task, q = 0):
        """Response time for transition from low to high crit."""
        # Determine worst case starting point of task while in low criticality
        # mode.
        S_i_q_lo = B_i_lo + q * task.c_lo
        high_prio_tasks = self.taskset.get_prio_tasks(task)
        for task in high_prio_tasks:
            S_i_q_lo += (1 + math.floor(S_i_q_lo/task.pr_lo)) * task.c_lo
        # Determine worst case stopping time.
        F_i_q_lo = S_i_q_lo + C_i_lo
        for t in high_prio_tasks:
            F_i_q_lo += ( math.ceil(F_i_q_lo/t.t_lo) - 
                    (1 + math.floor(S_i_q_lo/t.t_lo)) * t.c_lo)

        # Determine the worst case blocking while in transition to high crit.
        # Assuming no offset release of the task.
        if q == 0:
            B_i_q_tran = max(B_i_hi, B_i_lo)
        else:
            B_i_q_tran = B_i_lo
        # Determine Worst case starting point while in criticality transition.
        high_prio_lo_crit_tasks = self.taskset.get_taskset_low_crit_high_prio(task)
        high_prio_hi_crit_tasks = self.taskset.get_taskset_high_crit_high_prio(task)
        
        S_i_q_trans = B_i_q_tran + q * task.c_lo
        
        for t in high_prio_lo_crit_tasks:
            S_i_q_trans += math.ceil(S_i_q_lo/t.t_lo) * t.c_lo

        for t in high_prio_hi_crit_tasks:
            S_i_q_trans += (1 + math.floor(S_i_q_trans/t.t_lo)) * t.c_hi

        # Worst case completion time during criticality transition when transition
        # occurs before S_i_q_lo.
        F_i_q_trans_bf = S_i_q_trans + task.c_hi
        for t in high_prio_hi_crit_tasks:
            F_i_q_trans_bf += ((math.ceil(F_i_q_trans_bf/t.t_lo) - (1 + 
                math.floor(S_i_q_trans/t.t_lo))) * task.c_hi)
        
        # Worst case completion time during criticality transition, when transition
        # occurs after S_i_q_lo
        F_i_q_trans_af = S_i_q_lo + task.c_hi
        for t in high_prio_lo_crit_tasks:
            F_i_q_trans_af += ((math.ceil(F_i_q_lo/t.t_lo) - 
                (1 + math.floor(S_i_q_lo/t.t_lo))) * task.c_lo)

        for t in high_prio_hi_crit_tasks:
            F_i_q_trans_af += ((math.ceil(F_i_q_trans_af/t.t_lo) -
                    (1 + math.floor(S_i_q_lo/t.t_lo))) * t.c_hi)
        
        R_i_q = max(F_i_q_trans_bf, F_i_q_trans_af) - q*t.t_lo
        return R_i_q

    def __is_task_schedulable(self):
        """Sufficient schedulability test for pt-amc.
        Two necessary conditions are checked:
        1. Schedulability in low criticality.
        2. Schedulability in high crit in transition.
        """
        Lo_schedulable = True
        Hi_schedulable = True
        for task in self.taskset:
            if self.__get_lo_crit_response_time(task) < task.d_lo:
                continue
            else:
                Lo_schedulable = False
                break
        if Lo_schedulable:
            hi_tasks = self.taskset.get_tasks_by_crit('high')
            for task in hi_tasks:
                trans_rta = self.__get_transition_response_time(task)
                hi_rta = self.__get_hi_crit_response_time(task)
                if max(trans_rta, hi_rta) < task.d_lo:
                    continue
                else:
                    Hi_schedulable = False
                    break
        return Lo_schedulable and Hi_schedulable
        

    def __generate_preemption_threshold(self):
        """Maximal Preemption Threshold Assignment Algorithm(MPTAA) implementation.
        pt_array set with task preemption values, index corresponds to task index in 
        taskset object.
        """
        no_tasks = len(self.taskset) 
        self.pt_array = [self.taskset[i].prio for i in range(no_tasks)]
        for i in reversed(range(no_tasks)):
            schedulable = True
            j = i + 1
            while schedulable and pt_array[i] < no_tasks:
                self.pt_array[i] += 1
                schedulable = self.__is_task_schedulable(self.taskset[j])
                if not schedulable:
                    if self.pt_array[i]:
                        self.pt_array[i] -= 1
                    else:
                        ValueError("Negative preemption threshold assignment.\n")
                j = j + 1
                if j >= no_tasks:
                    break

    def get_processed_taskset(self):
        return self.processed_taskset

    def generate_ptamc(self, file):
        """Generate ptamc schedule for taskset given in json file."""
        self.__load_from_json(file)
