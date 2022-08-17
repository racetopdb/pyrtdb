# -*- coding: utf-8 -*-
import pandas as pd
from Comm.data import *
import os,sys
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *
from Lib.createDB import *
import logging
from Lib.tableOpt import *



# path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
@unittest.skip('执行大批量时，跳过此用例')
class Test_db_sample(unittest.TestCase):

    def test_db_sample(self):

        # sql = 'use DB_TEST_WRITE_100'
        # res = tableOpt.querySql(sql)
        # # self.assertEqual(res, 0, msg='初始化use数据库')
        # sql = "select bound_first(*),count(F_3) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(24hour)"
        # res = tableOpt.querySql(sql, 1)
        data_dict = read_excel(r"" + path + "\TestData\\juhe_003_1.xlsx", header=None,sheet_name='juhe_002')
        for j, row in enumerate(data_dict):
            print(row)
        # i = 0
        # bound = dict()
        # # row = res.get_row_count()
        # while res.cursor_next() == 0:
        #     bound_first = res.get_datetime_ms(0)
        #     countF_1 = res.get_int64(1)
        #     bound[i] = dict()
        #     bound[i].update({
        #                     'bound_first': bound_first,
        #                     'countF_1':countF_1
        #                     })
        #     i +=1
        # for j, row in enumerate(data_dict):
        #     self.assertEqual(bound[j]['bound_first'],int(row[0][25:38]),msg='验证bound_first的值')
        #     self.assertEqual(bound[j]['countF_1'], int(row[1]), msg='验证countF_1的值')






