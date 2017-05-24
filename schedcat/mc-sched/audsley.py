import random
from task import task # Abstract representation of task with two crit level.

class audsley:
    """Base class with audsley implementation."""

    def __init__(self, taskset = None):
        self.arg = []
        if taskset:
            self.taskset = random.random(taskset) #Randomize taskset list.
        else:
            self.taskset = None

    def __pick_next_task(self):
        pass

    def __default_prio_assign(self):
        """Default priority assigment implementation for Audsley's approach.'"""
        for task in 

    def assign_priorities(self, func = self.__default_prio_assign):
        """Audsley's priority assigment.'"""
        prio_taskset = None # Taskset arranged in order of increasing priorities.
        try:
            pass
        except ValueError:
            print("Failed to assign priorities to taskset.\n")
        return prio_taskset
