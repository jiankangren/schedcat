import math
import os
import errno
from taskset import Taskset


class Zss:
    def __init__(self, folder = None, file = None):
        self.folder = folder
        self.file = folder + '/' + file
        self.taskset = Taskset()
        self.processed_taskset = None
        self.slack_vectors = []
    
    @staticmethod
    def __create_slack_instance(start, duration):
        """Create a new slack tuple: (start time, duratiom)"""
        slack_instance = {
                "budget": duration,
                "start": start,
                "deadline": start + duration
                }
        return slack_instance

    @staticmethod
    def __sort_slack(slacklist):
        """Sort slack by start time."""
        return sorted(slacklist, key=lambda x: x[0])

    def __retrieve_taskset(self):
        """Load tasksets from json file."""
        json_taskset = []
        self.taskset.generate_taskset_from_json(self.file)
        print("loaded {0} tasksets from files".format(len(self.taskset)))

    def __save_zero_slack_taskset(self):
        """Create output folder and save the calculated taskset."""
        output_dir = self.folder + 'output'
        try:
            os.makedirs(self.folder + 'output')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise FileExistsError(errno)
        file_name = output_dir + str("zss") + '_taskset_processed.json'
        self.taskset.save_taskset_to_json(file_name)
        print("wrote {0} tasksets to {1} directory.\n", len(self.taskset), output_dir)

    @staticmethod
    def __get_conditional_taskset(task, taskset, condition_check):
        """Filter given taskset as per the given condition check function."""
        filtered_taskset = []
        for t in taskset:
            if condition_check(task, t):
                filtered_taskset.append(task)
        return filtered_taskset

    @staticmethod
    def __start_of_trailing_slack(t_i, slack_vec):
        """Get instance of trailing slack to given task."""
        b_i = t_i.budget # Task budget.
        d_i = t_i.deadline # Task deadline.
        trailing_slack_start = -1
        status = True
        index = 0
        rev_slack_vec = sorted(slack_vec, key=lambda x: x["deadline"], reverse=True)
        for i, slack in enumerate(rev_slack_vec):
            # Slack needs to be searched for deadline upto the deadline of 
            # task being tested.
            if slack.deadline <= d_i:
                index = i
                break
        if(index):
            slack_accumulated = 0
            for slack in rev_slack_vec[index:]:
                # Search for slack instance able to meet budget in c mode.
                slack_accumulated += slack["budget"]
                if slack_accumulated >= b_i:
                    trailing_slack_start = slack["start"] # Coarse starting time of slack.
                    break
            if slack_accumulated <= b_i: # Couldn't find enough slack for t_i.
                status = False
        else:
            status = False
        return (status, trailing_slack_start)

    @staticmethod
    def __get_slack_upto_instance(slack_vec, slack_instance, t_i):
        """Total available slack upto slack_instance."""
        avail_slack = 0
        slack_index = 0
        for index, slack in enumerate(slack_vec):
            if slack_instance <= slack["start"]:
                slack_index = index
                break

        if slack_index:
            for slack in slack_vec:
                if t_i.budget <= avail_slack:
                    break
                else:
                    avail_slack += slack["budget"]
        return avail_slack

    @staticmethod
    def __get_zero_slack_instant(task, norm_slack, high_slack):
        """Calculate the maximum available slack."""
        pass

    @staticmethod
    def __get_effective_budget(task, prio, mode):
        """Get the effective execution budget for task."""
        effective_budget = 0
        if task.prio > prio:
            if task.crit == 'normal':
                effective_budget = task.b_lo
            else:
                effective_budget = task.b_hi
        else:
            if task.crit == 'high':
                effective_budget = task.b_lo - task.slack

        return effective_budget

    def __get_slack_vector(self, task, taskset, mode='normal'):
        """An ordered list of slacks available in the given given taskset.
           Implementation for a rate-monotonic approach.
           implementation and notations as per Algorithm-3 in paper.
        """
        C_i_v = 0
        R_current = C_i_v
        interfering_tasks_c = self.taskset.__get_taskset_high_crit_high_prio(task)
        interfering_tasks_n = self.taskset.__get_taskset_normal_crit_high_prio(task)
        while(R_current >= t.period):
            R_previous = R_current
            b = 0
            while R_previous == R_current or R_current <= t:
                R_prevous = R_current
                R_current = C_i_v + self.__get_effective_budget(R_previous)
                b = t
                for task in taskset:
                    A = math.ceil(R_previous/task.period) * task.budget
                    if A < b:
                        A = b
                        I_m = task
                if R_previous == R_current:
                    R_current = R_current + self.__get_effective_budget(I_m, mode)


    @staticmethod
    def __are_vectors_equal(vec1, vec2):
        """Vector element wise comparator"""
        status = True
        if len(vec1) != len(vec2):
            raise ValueError("List should be of same size.\n")
        len_vec = len(vec1)
        comparator_list = [vec1[n].budget == vec2[n].budget for n in range(len_vec)]
        for flag in comparator_list:
            if not flag:
                status = False
        return status

    def __compute_final_slack_instant(self, taskset):
        """Calculate the zero slack instance of taskset."""
        slack_instant = None
        slack_before_cycle = []
        slack_after_cycle = []
        taskset_high_crit = taskset.__get_tasks_by_crit(taskset, 'high')

        while slack_before_cycle != slack_after_cycle:
            slack_before_cycle = slack_after_cycle
            for index, task in enumerate(taskset):
                normal_slack_vec = self.__get_slack_vector(task, taskset)
                high_slack_vec   = self.__get_slack_vector(task, taskset_high_crit)
                slack_after_cycle = self.__get_zero_slack_instant(
                        task, normal_slack_vec, high_slack_vec)
                # Stop when no more slack movement can be made between normal and
                # critical mode.
                if self.__are_vectors_equal(slack_before_cycle, slack_after_cycle):
                    break

    def do_zero_slack_assignment(self):
        """public function to invoke zero slack calculation."""
        for taskset in self.tasksets:
            zss_taskset = self.__computer_final_slack_instant(taskset)
