from audsley import Audsley
import math
from copy import copy


class AmcMax(Audsley):
    """AMC-max based priority assignment."""

    def __init__(self, taskset):
        self.taskset = taskset
        super(AmcMax, self).__init__(taskset)

    @staticmethod
    def __m_k_s_t(t, s, tk, dk):
        return min(math.ceil((t - s - (tk - dk))/tk) + 1, math.ceil(t/tk))

    @staticmethod
    def __i_l_s(task, taskset, s, hyp_period):
        i_l_s = 0
        if s < hyp_period:
            tsks_lo = taskset.get_taskset_low_crit_high_prio(task)
            for t in tsks_lo:
                i_l_s += ((math.floor(s / t.pd_l) + 1) * t.b_l)
        return i_l_s

    def __i_h_s(self, task, taskset, s, hyp_period):
        i_h_s = 0
        if s < hyp_period:
            tsks_hi = taskset.get_taskset_high_crit_high_prio(task)
            for t in tsks_hi:
                tk = t.pd_l
                dk = t.dl_l
                ch = t.b_h
                cl = t.b_l
                mkst = self.__m_k_s_t(hyp_period, s, tk, dk)
                i_h_s += (mkst * ch) + (math.ceil(t/tk) - mkst*cl)
        return i_h_s

    def __get_hyper_period(self, taskset=None):
        if taskset is not None:
            pass
        return 0

    def __ri_amc_max(self, task, taskset, hyper_period):
        """Demand bound function for amc max."""
        Ri = task.b_hi
        for s in range(1, hyper_period):
            ils = self.__i_l_s(task, taskset, s, hyper_period)
            ihs = self.__i_h_s(task, taskset, s, hyper_period)
            Ri = max(Ri, task.b_hi + ils + ihs)
        return Ri

    def amc_max_rta(self, taskset=None):
        """Check schedulability for the given taskset."""
        rt = 0.0
        hyper_period = self.__get_hyper_period(taskset)
        for task in taskset:
            rt += self.__ri_amc_max(task, taskset, hyper_period)
        return rt

    def priority_assignment(self):
        """Uses audsley's approach to priority assignment and returns priority
        values or an empty set in case of failure."""
        self.assign_priorities(self.amc_max_rta)
