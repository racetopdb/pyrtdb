from pyrtdb.log import rtdb_logger_singleton
from pyrtdb.cursor import INSERT_VALUES_PATTERN
from pyrtdb.cursor import Cursor, DictCursor
from pyrtdb.connection import Connection
from pyrtdb.constant import RTDB_HOST, RTDB_PASSWORD, RTDB_PORT, RTDB_USER_NAME
import unittest
from datetime import datetime, timedelta

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent))


class TestCursor(unittest.TestCase):
    """
    sql pattern:
        insert into abc values(1),(2), efg values(3),(4)
        insert into abc values(1)(2) efg values(3)(4)
        insert into abc(d) values(1),(2), efg(h) values(3),(4)
        insert into abc(d) values(1)(2) efg(h) values(3)(4)
        insert into abc(d) values(1), (2)
        insert into abc(d) values(1), (2)
        insert into abc(a,b,c) values(1,2,'abc'), (3,4,'def')
        insert into abc(a,b,c) values(1,2,'abc')(3,4,'def')
        insert into abc value( 'abc' ), ( 'def' )
        insert into abc value( 'abc' )
        insert into abc(c) value( 'abc' )
        insert into abc(a,b,c) values(1,2,'abc')
    """
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = Connection(RTDB_HOST, RTDB_PORT, RTDB_USER_NAME,
                            RTDB_PASSWORD, timeout=10, charset='utf-8')
        cls.cursor = Cursor(cls.db)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def test_re_insert_values_pattern1(self):
        # sqls = [
        #     "insert into abc values(1), (2), efg values(3), (4)",
        #     "insert into abc values(1)(2) efg values(3)(4)",
        #     "insert into abc(d) values(1), (2), efg(h) values(3), (4)",
        #     "insert into abc(d) values(1)(2) efg(h) values(3)(4)",
        #     "insert into abc(d) values(1), (2)",
        #     "insert into abc(d) values(1), (2)",
        #     "insert into abc(a, b, c) values(1, 2, 3), (1, 2, 3)",
        #     "insert into abc(a, b, c) values(1, 2, 'abc')(3, 4, 'def')",
        #     "insert into abc value('abc'), ('def')",
        #     "insert into abc value('abc')",
        #     "insert into abc(c) value('abc')",
        #     "insert into abc(a, b, c) values(1, 2, 'abc')",
        # ]
        sqls = [
            "insert into abc(a, b, c) values(%s,%s,%s);",
            "insert into abc values(%s, %s, %s);"
        ]
        for i, sql in enumerate(sqls):
            m = INSERT_VALUES_PATTERN.match(sql)
            if m:
                q_prefix = m.group(1) % ()
                q_values = m.group(2).rstrip()
                assert q_values[0] == "(" and q_values[-1] == ")"

                if i == 0:
                    self.assertEqual(
                        q_prefix, "insert into abc(a, b, c) values")
                    self.assertEqual(q_values, "(%s,%s,%s)")
                if i == 1:
                    self.assertEqual(q_prefix, "insert into abc values")
                    self.assertEqual(q_values, "(%s, %s, %s)")

    def test_fetch(self):

        self.cursor.execute("create database test_db if not exists;")
        self.cursor.execute("show databases;")
        rows = self.cursor.fetchall()
        self.assertIsNotNone(rows)
        self.assertIsInstance(rows[0], tuple)

        rtdb_logger_singleton().debug(
            "Fetch all rows from rtdb, rows: {}, sql: {}".format(rows, "show databases"))

        # test for dict rows
        dict_cursor = DictCursor(self.db)
        dict_cursor.execute("show databases;")
        rows = dict_cursor.fetchall()
        self.assertIsNotNone(rows)
        self.assertIsInstance(rows[0], dict)

        rtdb_logger_singleton().debug(
            "Fetch dict rows from rtdb, rows: {}, sql: {}".format(rows, "show databases;"))

        self.assertEqual(self.cursor.execute("use test_db;"), -1)
        self.cursor.execute(
            "create table if not exists test_table(is_working boolean, age int, name char(100));")
        self.cursor.execute(
            "insert into test_table(is_working, age, name) values(false, 12, 'Michael');")
        self.cursor.execute("select last * from test_table")
        rows = self.cursor.fetchall()
        self.assertIsNotNone(rows)
        self.assertIsInstance(rows[0], tuple)
        rtdb_logger_singleton().debug(
            "Fetch all rows from rtdb, rows: {}, sql: {}".format(rows, "select last * from test_table;"))

        # "select * from test_table where time between '2022-02-09 00:00:00.000' and '2022-02-12 00:00:00.000'"
        self.cursor.execute(
            "select * from test_table where time between %s and %s", (datetime.now() - timedelta(days=2), datetime.now() + timedelta(days=2), ))
        rows = self.cursor.fetchall()
        self.assertIsNotNone(rows)
        self.assertIsInstance(rows[0], tuple)
        rtdb_logger_singleton().debug(
            "Fetch all rows from rtdb, rows: {}, not formatted sql: {}".format(rows, "select * from test_table where time between %s and %s"))


if __name__ == '__main__':
    unittest.main()
