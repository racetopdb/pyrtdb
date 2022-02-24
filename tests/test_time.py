import unittest
try:
    from pyrtdb.time import *
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path.cwd().parent))

    from pyrtdb.time import *


class TestTime(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def test_DateFromTicks(self):
        ticks = 24 * 60 * 60
        d = DateFromTicks(ticks)
        self.assertEqual(d, date(1970, 1, 2))

        # add ten days
        ticks = 24 * 60 * 60 * 10
        d = DateFromTicks(ticks)
        self.assertEqual(d, date(1970, 1, 11))

    def test_TimeFromTicks(self):
        ticks = 24 * 60 * 60
        t = TimeFromTicks(ticks)
        self.assertEqual(t, time(hour=8))


if __name__ == '__main__':
    unittest.main()
