import unittest
from task import Task
from taskset import Taskset


class TasksetTest(unittest.TestCase):

    def setUp(self):
        self.filename = ""

    def tearDown(self):
        pass

    def test_create_taskset(self):
        A = Taskset("default")
        self.assertEqual(A.scheduler, "default")

    def test_add_remove_task_from_taskset(self):
        a = Taskset("default")
        b = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        a.append(b)
        c = a.pop()
        self.assertEqual(b.crit, c.crit)

    def test_load_taskset_from_json(self):
        pass

    def test_write_taskset_to_json(self):
        pass

    def test_get_hi_crit_utilization_of_taskset(self):
        tsk = Taskset("default")
        a = Task(1, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        b = Task(2, 5000, 10000, 2, 1, 50000, 50000, 50000, 50000)
        c = Task(1, 5000, 10000, 2, 1, 50000, 50000, 50000, 50000)
        d = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        tsk.append(a)
        tsk.append(b)
        tsk.append(c)
        tsk.append(d)
        util = tsk.get_high_util()
        self.assertEqual(util, 0.2)

    def test_get_lo_crit_utilization_of_taskset(self):
        tsk = Taskset("default")
        a = Task(1, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        b = Task(2, 5000, 10000, 2, 1, 50000, 50000, 50000, 50000)
        c = Task(1, 5000, 10000, 2, 1, 50000, 50000, 50000, 50000)
        d = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        tsk.append(a)
        tsk.append(b)
        tsk.append(c)
        tsk.append(d)
        util = tsk.get_high_util()
        self.assertEqual(util, 0.2)

    def test_get_rta_of_taskset(self):
        tsk = Taskset("default")
        a = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        b = Task(2, 5000, 10000, 2, 1, 50000, 50000, 50000, 50000)
        c = Task(2, 5000, 10000, 2, 1, 50000, 50000, 50000, 50000)
        d = Task(2, 5000, 10000, 1, 1, 50000, 50000, 50000, 50000)
        tsk.append(a)
        tsk.append(b)
        tsk.append(c)
        tsk.append(d)
        rta = tsk.get_high_util()
        self.assertEqual(rta, 0.2)
