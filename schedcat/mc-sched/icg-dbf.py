import sys


class icg_dbf(amc):
    """Speed up bound and schedulability check for ICG"""
    
    def __init__(self, taskset):
        self.taskset = taskset

    def critical_speedup(self):
        """Calculate critical speed up factor."""
        sched_points = self.get_schedule_points()
        for i in sched_points:
        pass

    def interference_minimization(self):
        """Iteratively minimize the interference in the task graph."""
        pass

    def dbf_icg(self):
        """Calculate the demand bound for the task."""
        pass

    def check_schedulability(self):
        """Check schedulability of the given task set."""
        pass






