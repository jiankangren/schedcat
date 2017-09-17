"""Improved schedulability analysis for EDF-VD by Ekberg and Yi."""
from taskset import taskset
from edfvd import edfvd

class edfey(edfvd):
    def __init__(self, taskset):
        self.taskset = taskset

    
