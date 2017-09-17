import unittest
from task import Task


class TestTask(unittest.TestCase):

    def test_create_task(self):
        a = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        self.assertEqual(a.crit, 2)

    def test_set_get_attribute_budget(self):
        a = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        self.assertEqual(a.c_hi, 10000)

    def test_set_get_attribute_deadline(self):
        a = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        self.assertEqual(50000, 50000)

    def test_set_get_attribute_period(self):
        a = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        self.assertEqual(50000, 50000)

    def test_hi_utilization_of_task(self):
        a = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        self.assertEqual(a.task_util("high"), 0.2)

    def test_lo_utilization_of_task(self):
        a = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        self.assertEqual(a.task_util("low"), 0.1)