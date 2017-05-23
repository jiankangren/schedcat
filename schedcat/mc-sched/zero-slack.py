import sys
import pprint
import json
import matplotlib.pyplot as plt

class zero_slack:
    def __init__(self, task_file):
        """Load the taskset from the json file.
        Taskset: [task, task, ...]
        task : [crit, prio]
        """
        self.task_file = task_file
        self.taskset =  None
        self.zero_slack_array = []
        # Initialize the zero slack array to the size of the taskset.
        for i in range(len(self.taskset)):
            self.zero_slack_array.append(0)

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
        for task in self.taskset:
            task_union = self.get_task_union(task)

    def get_zero_slack_instant():
        """Calculates instant of slack 0 before the task deadline."""
        pass

    def __iter__(self):
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
