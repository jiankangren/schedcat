import json
from copy import copy
from task import Task


class Taskset:
    """Abstract representation of a taskset."""

    def __init__(self, sched_type, folder=None):
        self.folder = folder
        self.sched_type = sched_type
        self.tasks = []
        self.active_index = 0
        self.task_properties = {}
        self.iterindex = 0

    def __getattr__(self, name=None):
        if name == "scheduler":
            return self.sched_type

    def __append_task(self, task):
        """Append task and increment tracking index."""
        task.index = self.active_index
        self.tasks.append(task)
        self.active_index += 1

    def append(self, task):
        if task.sched_type == self.sched_type:
            self.tasks.append(task)

    def pop(self):
        return self.tasks.pop()

    def __iter__(self):
        self.iterindex = 0
        return self

    def __next__(self):
        slot = self.tasks[self.iterindex]
        self.iterindex += 1
        return slot

    def sort_by_crit(self):
        tasks = copy(self.tasks)
        tasks.sort(key=lambda x:x.crit, reverse=True)
        return tasks

    def generate_taskset_from_json(self, json_file):
        """Convert json representation to taskset."""
        self.tasks = []  # Clear the saved taskset.
        with open(json_file, 'r') as f:
            taskset_package = json.load(f)
            self.task_properties = taskset_package['properties']
            for index, json_task in enumerate(taskset_package['tasks']):
                new_task = Task()
                self.__append_task(new_task.load_from_json(json_task))
                print("Loaded {0} tasks from taskset file {1}".format(
                    len(self.tasks), json_file.tokenize("//")[-1]))

    def __len__(self):
        """Return number of tasks present in given taskset."""
        return len(self.tasks)

    def save_taskset_to_json(self, filename=None):
        """Dump a given taskset to json representation."""
        json_taskset = []
        taskset_package = {}
        for task in self.tasks:
            json_taskset.append(task.get_json_representation())

        taskset_package['properties'] = self.task_properties
        taskset_package['tasks'] = json_taskset

        with open(filename, 'w') as f:
            json.dump(taskset_package, f)

    def __calculate_total_utilization(self, flag='norm'):
        """Get taskset utilization."""
        total_util = 0
        if not len(self.tasks):
            raise ValueError("Taskset is empty.")
        else:
            for task in self.tasks:
                total_util += task.util(flag)
        if flag == 'norm':
            self.task_properties["total_util"] = total_util
        elif flag == 'high':
            self.task_properties["high_util"] = total_util
        else:
            self.task_properties["low_util"] = total_util
        return total_util

    def get_high_util(self):
        """Total utilization of only high crit tasks."""
        high_util = 0
        if self.task_properties["high_util"] is None:
            high_util = self.__calculate_total_utilization('high')
        else:
            high_util = self.task_properties["high_util"]
            return high_util

    def __get_conditional_taskset(self, task, comparison_op):
        conditional_taskset = []
        for t in self.tasks:
            if comparison_op(t, task):
                conditional_taskset.append(t)
        return conditional_taskset

    def get_taskset_high_crit_low_prio(self, task):
        """get tasks of higher criticality, lower priority"""
        def comparison_op(x, y):
            return (x.crit > y.crit) and (x.prio < y.prio)
        return self.__get_conditional_taskset(task, comparison_op)

    def get_taskset_high_crit_high_prio(self, task):
        """get tasks of higher criticality, higher priority"""
        def comparison_op(x, y):
            return (x.crit > y.crit) and (x.prio > y.prio)
        return self.__get_conditional_taskset(task, comparison_op)

    def get_taskset_low_crit_high_prio(self, task):
        """get tasks of lower criticality, higher priority"""
        def comparison_op(x, y):
            return (x.crit < y.crit) and (x.prio > y.prio)
        return self.__get_conditional_taskset(task, comparison_op)

    def get_taskset_high_crit_same_prio(self, task):
        """get tasks of higher criticality, same priority"""
        def comparison_op(x, y):
            return (x.crit > y.crit) and (x.prio == y.prio)
        return self.__get_conditional_taskset(task, comparison_op)

    def get_tasks_by_crit(self, flag='high'):
        """Retrieve all high or low crit tasks from the given taskset."""
        high_taskset = []
        condition = None
        if flag == 'high':
            def condition(x):
                return x.crit == 1
        elif flag == 'low':
            def condition(x):
                return x.crit == 0
        else:
            print("Value error.")

        for task in self.tasks:
            if condition(task):
                high_taskset.append(task)
        return high_taskset

    def calculate_rta(self, task):
        """Do response time analysis for given taskset, override"""
        pass

    def get_low_util(self):
        """Total utilization of only low crit tasks."""
        low_util = 0
        if self.task_properties["low_util"] is None:
            low_util = self.__calculate_total_utilization('low')
        else:
            low_util = self.task_properties["low_util"]
        return low_util

    def get_high_crit_high_util(self):
        pass

    def get_low_crit_low_util(self):
        pass

    def get_high_crit_low_util(self):
        pass

    def total_util(self):
        """Total taskset utilization in normal mode."""
        total_util = 0
        if self.task_properties["low_util"] is None:
            total_util = self.__calculate_total_utilization('low')
        else:
            total_util = self.task_properties["low_util"]
        return total_util
