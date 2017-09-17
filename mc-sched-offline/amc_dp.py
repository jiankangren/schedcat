import math
from copy import copy

class AmcDP:
    """Implementation of AMC Deffered preemtion."""

    def __int__(self, taskset=None):
        super(AmcDP, self).__init__()
        self.taskset = taskset

    def __get_bi(self, curr_task, mode = "default"):
        """ Get total blocking for given task."""
        Bi = 0
        if mode == "default":
            for task in self.taskset:
                if task.prio_lo < curr_task.prio_lo:
                    Bi = max(Bi, task.fp - 1)
        elif mode == "high":
            filtered_task = []
            for task in self.taskset:
                if task.crit > 1:
                    filtered_task.append(task)
            for task in filtered_task:
                if task.prio_lo < curr_task.prio_lo:
                    Bi = max(Bi, task.fp - 1)
        return Bi

    def __calculate_g_hi(self, task, taskset):
        """Number of high jobs in busy period."""
        Bi = self.__get_bi(task)
        taskset_hi_hi = taskset.get_taskset_high_crit_high_prio(task)
        taskset_hi_lo = taskset.get_taskset_low_crit_high_prio(task)
        Vi_prev = 0
        Vi = Bi + g * task.c_lo
        Vi_const = Vi
        while Vi_prev < Vi:
            Vi_prev = Vi
            Vi = Vi_const
            Vi += max(0, math.ceil(Vi/task.t_lo) - g)*task.c_hi
            interfer_hi_hi = 0
            interfer_lo_hi = 0
            for t in taskset_hi_hi:
                interfer_hi_hi += math.ceil(Vi/t.t_lo)*t.c_hi
            for t in taskset_hi_lo:
                interfer_lo_hi += math.ceil(Vi/t.t_lo)*t.c_lo
            Vi += interfer_hi_hi + interfer_lo_hi
        Gi = math.ceil(Vi/task.t_lo)
        return Gi

    def __calculate_g_lo(self, task, taskset):
        """Number of low jobs in busy period."""
        taskset_hep = []
        for t in taskset:
            if t.prio_lo >= t.prio_lo:
                taskset_hep.append(t)
        Vi = self.__get_bi(task)
        V_i_const = Vi
        Vi_prev = 0
        while Vi > Vi_prev:
            Vi_prev = Vi
            Vi = V_i_const
            for t in taskset_hep:
                Vi += math.ceil(Vi/t.t_lo)*t.c_lo
        Gi = math.ceil(Vi/task.t_lo)
        return Gi

    def __calculate_Ri_lo(self, task, taskset):
        taskset_hp = []
        R_i = 0
        G_lo = self.__calculate_g_lo(task, taskset)
        for t in taskset:
            if t.prio_lo > task.prio_lo:
                taskset_hp.append(t)
        for g in range(int(G_lo)):
            R_i_g = self.__calculate_Ri_lo_g(task, taskset_hp, g)
            R_i = max(R_i, R_i_g)
        return R_i

    def __calculate_Ri_lo_g(self, task, taskset, g):
        R_i_g = self.__get_bi(task)
        R_i_g += (g + 1) * task.c_lo - task.dp_lo
        R_i_const = R_i_g
        R_i_prev = 0
        while (R_i_g > R_i_prev):
            R_i_prev = R_i_g
            R_i_g = R_i_const
            for t in taskset:
                R_i_g += (math.floor(R_i_g / t.t_lo) + 1) * t.c_lo
        return R_i_g

    def __calculate_Ri_g_p(self, task, taskset, p, g):
        task.dp_hi = min((task.c_hi - task.c_lo), task.dp_lo)
        taskset_hp = []
        for t in taskset:
            if t.prio_lo > task.prio_lo:
                taskset_hp.append(t)

        R_i_hi = self.__get_bi(task)
        R_i_hi += g*task.c_lo + (p + 1 - g)*task.c_hi - task.dp_hi
        task_hpl = taskset.get_taskset_low_crit_high_prio(task)
        R_i_g = self.__calculate_Ri_lo_g(task, taskset_hp, g)
        for t in task_hpl:
            R_i_g += math.ceil(R_i_g/t.t_lo) * t.c_lo

        R_i_hi += R_i_g
        R_i_prev = 0
        R_i_const = R_i_hi
        task_hph = taskset.get_taskset_high_crit_high_prio(task)
        while R_i_hi > R_i_prev:
            R_i_prev = R_i_hi
            R_i_hi = R_i_const
            for t in task_hph:
                R_i_hi += (math.floor(R_i_hi/t.t_lo) + 1)*t.c_hi

        R_i_hi = R_i_hi + task.dp_hi - p*task.t_lo
        return R_i_hi

    def __calculate_Ri_hi(self, task, taskset, g):

        R_i_hi = 0
        G_lo = self.__calculate_g_lo(task, taskset)
        G_hi = self.__calculate_g_hi(task, taskset)
        for g in range(int(G_lo)):
            for p in range(g, int(G_hi)):
                R_i_g_p = self.__calculate_Ri_g_p(task, taskset, p, g)
                R_i_hi = max(R_i_hi, R_i_g_p)
        return R_i_hi

    def __search_F_i(self, task, taskset):
        F_i = 0
        f_range = task.c_lo
        if task.crit > 1:
            f_range = task.c_hi
        for f in range(0, f_range):
            r_i_lo = self.__calculate_Ri_lo(task, taskset)

            if task.crit > 1:
                r_i_hi = self.__calculate_g_hi(task, taskset)



    def assign_priorities_and_dp(self):
        """ assign priorities and deferred preemtion.
        1. Start from the lowest priority.
        2. Start with high criticality tasks.
        3. Try to assign dp from 1 to C_hi.
        4. Of the schedulable task found at given priority level
           pick task with lowest F and assign priority.
        """
        taskset_copy = copy(self.taskset)
        tasks = taskset_copy.sorted_by_crit()


