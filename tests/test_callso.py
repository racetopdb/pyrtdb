from pyrtdb.log import rtdb_logger_singleton
from pyrtdb.callso import *
from pyrtdb.constant import *
import unittest
from unittest import TestCase
from datetime import datetime

import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent))


class TestRawTsdbClient(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = RawTsdbClientV2(
            RTDB_HOST, RTDB_PORT, RTDB_USER_NAME, RTDB_PASSWORD)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self) -> None:
        self.client.connect()
        return super().setUp()

    def tearDown(self) -> None:
        errno = self.client.disconnect()
        self.assertEqual(errno, 0)
        return super().tearDown()

    def test_disconnect(self):
        errno = self.client.disconnect()
        self.assertEqual(errno, 0)

    # @unittest.skip("return value will be invalid, now skip it")
    def test_get_charset(self):
        charset = self.client.get_charset()
        self.assertEqual(charset, CHARSET_ISO1)

    def test_set_charset(self):
        charset_reverse = {v: k for k, v in CHARSET_DICT.items()}
        charset_id = charset_reverse.get(CHARSET_UTF8, None)
        assert charset_id

        errno = self.client.set_charset(charset_id)
        self.assertEqual(errno, 0)

        charset = self.client.get_charset()
        self.assertEqual(charset, CHARSET_UTF8)

    def test_user_name(self):
        self.assertEqual(self.client.user_name, "test")
        print(self.client.user_name)

    def test_query(self):
        sql = "show databases;"
        errno = self.client.query(sql)
        self.assertEqual(errno, 0)

    def test_store_result(self):
        sql = "create database test_my_db if not exists;"
        errno = self.client.query(sql)
        self.assertEqual(errno, 0)
        self.client.store_result()
        self.assertIsNone(self.client.result)
        rtdb_logger_singleton().debug("result: {}".format(self.client.result))

        if self.client.result:
            self.client.free_result()

    # def test_free_result(self):
    #     sql = "show databases;"
    #     errno = self.client.query(sql)
    #     self.assertEqual(errno, 0)

    #     self.client.store_result()
    #     if getattr(self.client, "_result"):
    #         self.client.free_result()

    @unittest.skip("skip it")
    def test_fetch_rows(self):
        create_db_sql = "create database test_db if not exists;"
        errno = self.client.query(create_db_sql)
        self.assertEqual(errno, 0)

        sql = "show databases;"
        errno = self.client.query(sql)
        self.assertEqual(errno, 0)

        self.client.store_result()

        rows = self.client.fetch_rows()
        rtdb_logger_singleton().debug("Fetch rows: {}, query: {}".format(rows, sql))

        if self.client.result:
            self.client.free_result()

    def test_dml(self):
        create_db_sql = "create database test_db if not exists;"
        errno = self.client.query(create_db_sql)
        self.assertEqual(errno, 0)

        errno = self.client.query("use test_db;")
        self.assertEqual(errno, 0)

        errno = self.client.query(
            "create table if not exists test_table(is_working boolean, age int, name char(100));", database="test_db")
        self.assertEqual(errno, 0)

        errno = self.client.query(
            "insert into test_table(is_working, age, name) values(false, 12, 'Michael');")
        self.assertEqual(errno, 0)

        errno = self.client.query("select last * from test_table")
        self.assertEqual(errno, 0)
        self.client.store_result()
        rows = self.client.fetch_rows()
        rtdb_logger_singleton().debug("Fetch rows: {}, query: {}".format(
            rows, "select last * from test_table"))
        rtdb_logger_singleton().debug("Last time: {}".format(rows[0][0]))
        if self.client.result:
            self.client.free_result()

        errno = self.client.query(
            "select * from test_table where time between '2022-02-09 00:00:00.000' and '2022-02-12 00:00:00.000'")
        self.assertEqual(errno, 0)
        self.client.store_result()
        rows = self.client.fetch_rows()
        rtdb_logger_singleton().debug("Fetch rows: {}, query: {}".format(
            rows, "select * from test_table where time between '2022-02-09 00:00:00.000' and '2022-02-12 00:00:00.000'"))
        if self.client.result:
            self.client.free_result()


if __name__ == '__main__':
    unittest.main()
