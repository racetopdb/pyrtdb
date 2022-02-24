from pyrtdb.connection import Connection
import unittest

import sys
from pathlib import Path
from python.pyrtdb.pyrtdb.constant import RTDB_HOST, RTDB_PASSWORD, RTDB_PORT, RTDB_USER_NAME
sys.path.append(str(Path.cwd().parent))


class TestConnectionV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = Connection(RTDB_HOST, RTDB_PORT, RTDB_USER_NAME,
                            RTDB_PASSWORD, timeout=10, charset='utf-8')
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self) -> None:
        self.db.connect()
        return super().setUp()

    def tearDown(self) -> None:
        self.db.close()
        return super().tearDown()

    def test_query(self):
        self.db.query("show databases;")


if __name__ == '__main__':
    unittest.main()
