from amc_dp import AmcDP
import unittest


class AmcDpTest(unittest.TestCase):

    def setUp(self):
        self.a = 1
        self.b = 1

    def test_schedulability(self):
        self.assertEqual(self.a, self.b)

    def test_priority_assignment(self):
        self.assertNotEqual(self.a, 2*self.b)

    def test_dp_assignment(self):
        self.assertEqual(2*self.a, 2*self.b)


if __name__ == '__main__':
    unittest.main()
