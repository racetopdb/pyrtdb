# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
import datetime
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import logging
from Comm.convert import *
from time import sleep

# @unittest.skip('执行大批量时，跳过此用例')
class Test_select_last(unittest.TestCase):
    tb = 'select_last'
    db = 'test_select_last' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres =tableOpt.createTb(cls.tb,
                                {
                                    'f1':data_type['int'],
                                    'f2':data_type['bigint'],
                                    'f3':data_type['bool']
                                })
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_select_025(self):
        '''
        使用select last * from t1查询表的最后一条记录
        '''
        res1 = tableOpt.insertTb(self.tb,['time','f1','f2','f3'],['2022-07-11 10:00:00.000',1,222222,1])
        self.assertEqual(res1 , 0 ,msg='第一条写入失败')
        res2 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:01:00.000', 2, 222222, 1])
        self.assertEqual(res2, 0, msg='第二条写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            timekey = lastObj.get_datetime_ms(0)
            # 把时间戳转成日期格式
            dates = convert.get_date_stamp(timekey)
            self.assertEqual(dates, '2022-07-11 10:01:00.000', msg='验证time值')
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 2, msg='验证f1值')
            f2 = lastObj.get_int64(2)
            self.assertEqual(f2, 222222, msg='验证f2值')
            f3 = lastObj.get_bool(3)
            self.assertEqual(f3, True, msg='验证f3值')
    def test_select_026(self):
        '''
        使用select last f1,f2,f3 from t1 查询表的最后一条记录,query ok
        '''
        res1 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:02:00.000', 3, 222222, 1])
        self.assertEqual(res1, 0, msg='第一条写入失败')
        res2 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:03:00.000', 4, 222222, 1])
        self.assertEqual(res2, 0, msg='第二条写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 4, msg='验证f1值')
            f2 = lastObj.get_int64(2)
            self.assertEqual(f2, 222222, msg='验证f2值')
            f3 = lastObj.get_bool(3)
            self.assertEqual(f3, True, msg='验证f3值')
    def test_select_027(self):
        '''
        使用select last f1 f2 f3 from t1 查询表的最后一条记录，字段直接使用空格分隔,query fail
        '''
        res1 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:04:00.000', 5, 222222, 1])
        self.assertEqual(res1, 0, msg='第一条写入失败')
        sql = 'select last f1 f2 f3 from '+self.tb+''
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='查询失败')
    def test_select_028(self):
        '''
        先写入两条时间点小的记录，再写入时间大的记录，再写入时间小的记录，使用select last * 查询最后一条记录
        '''
        res1 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:05:00.000', 6, 222222, 1])
        self.assertEqual(res1, 0, msg='第一条写入失败')
        res2 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:06:00.000', 7, 222222, 1])
        self.assertEqual(res2, 0, msg='第二条写入失败')
        res3 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:10:00.000', 10, 222222, 1])
        self.assertEqual(res3, 0, msg='第三条写入失败')
        res4 = tableOpt.insertTb(self.tb, ['time', 'f1', 'f2', 'f3'], ['2022-07-11 10:08:00.000', 8, 222222, 1])
        self.assertEqual(res4, 0, msg='第四条写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            timekey = lastObj.get_datetime_ms(0)
            # 把时间戳转成日期格式
            dates = convert.get_date_stamp(timekey)
            self.assertEqual(dates, '2022-07-11 10:10:00.000', msg='验证time值')
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 10, msg='验证f1值')
            f2 = lastObj.get_int64(2)
            self.assertEqual(f2, 222222, msg='验证f2值')
            f3 = lastObj.get_bool(3)
            self.assertEqual(f3, True, msg='验证f3值')



