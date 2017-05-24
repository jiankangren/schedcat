import sys
import pprint
import json
import matplotlib.pyplot as plt

class zero_slack:
    
    """
    Task abstraction class.
    TODO: Move to schedule agnostic level.
    """
    class task:
        """Task attribute initialization.
        *_n = Normal mode or low criticality mode.
        *_c = Critical mode or high criticality mode.
        """
        def __init__(self, task_properties = None):
            self.__budget_n = task_properties["budget_lo"]
            self.__budget_c = task_properties["budget_hi"]
            self.__prio_n   = task_properties["prio_low"]
            self.__prio_c   = task_properties["prio_high"]
            self.__crit     = task_properties["crit"]
            self.__dl_n     = task_properties["deadline_low"]
            self.__dl_c     = task_properties["deadline_high"]
            self.__period_n = task_properties["period_low"]
            self.__period_c = task_properties["period_high"]
        
        """Task properties high crit mode."""
        def get_hi_attrib(self):
            return (self.__budget_c, self.__prio_c, self.__dl_c, self.__period_c)

        """Task properties low crit mode."""
        def get_low_attrib(self):
            return (self.__budget_n, self.__prio_n, self.__dl_n, self.__period_n)

        """Task utilization."""
        def get_util(self, mode="low"):
            util = None
            if mode == "low":
                util = self.__budget_n/self.__period_n
            elif mode == "high":
                util = self.__budget_c/self.__period_c
            else:
                raise AttributeError("Input mode attribute is invalid.\n")
            return util

    def __init__(self, task_file):
        """Load the taskset from the json file.
        Taskset: [task, task, ...]
        task : [crit, prio]
        """
        self.__task_file = task_file
        self.__taskset =  None
        self.__zero_slack_array = []
        self.__task_by_crit = [] # Task sorted by criticality.
        self.__task_by_prio = [] # Task sorted by priority.
        # Initialize the zero slack array to the size of the taskset.
        for i in range(len(self.taskset)):
            self.__zero_slack_array.append(0)

    def sort_task_by_function(self, sort_handler = None):
        """Sort task based on the lambda handler passed on."""
        sorted_array = []
        if sort_handler:
            sorted_array = sorted(self.__taskset, key=lambda x: x.__prio_n, reverse=True)
        else:
            raise AttributeError("Input mode attribute is invalid.\n")
        return sorted_array

    def get_task_union(self, current):
        """
        Create the task union consisting of tasks ofHigh crit && high priority,
        Low crit && high Priority, Same Crit && high priority.
        """
        task_union = []
        c_crit = current[0]
        c_prio = current[1]
        for t in self.taskset:
            if ((c_crit < t[0]) and (c_prio < t[1])):
                """Condition-1: """
                pass
            elif ((c_crit < t[0]) and (c_prio > t[1])):
                """Condtion-2: """
                pass
            elif ((c_crit == t[0]) and (c_prio < t[1])):
                """Condition-3: """
                pass
            else:
                pass
        return task_union

    def calc_zero_slack(self):
        """Calculates the zero slack instances for the given taskset."""
        self.zero_slack_instances = self.compute_final_zero_slack_instance()
        return self.zero_slack_instances

    def compute_final_zero_slack_instance(self):
        """Computes the slack instances to switch to higher criticality."""
        for task in self.__taskset:
            task_union = self.get_task_union(task)

    def get_zero_slack_instant():
        """Calculates instant of slack 0 before the task deadline."""
        pass

    def __iter__(self):
        """Iterate over zero slack instances."""
        for val in self.zero_slack_instances:
            yield val

    def get_slack_vector(self):
        """Calculates RM specific slack vector slots."""
        pass

    def plot_slack_gantt_chart(self):
        """Plot a gantt chart representation of the slacks with respect
        to the given taskset."""
        pass

def main():
    # Test scenarios.
    zero_slack object()


if __name__ == '__main__':
    main()
