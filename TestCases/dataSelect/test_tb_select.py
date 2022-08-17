# -*- coding: utf-8 -*-
import unittest,datetime

from Comm.pyrtdb import conn
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import os,sys
from Comm.convert import *
from Comm.data import *

#当前路径的上上级目录
path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
# @unittest.skip('执行大批量时，跳过此用例')
class Test_tb_select(unittest.TestCase):
    tb = 'test_tb_001'
    db = 'test_tb_select' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres = tableOpt.createTb(cls.tb,
                                 {
                                     'f1': data_type['int'],
                                     'f2':data_type['varchar']+'(32)',
                                     'f3':data_type['bigint'],
                                     'f4':data_type['int']
                                 }
                                 )
        cls().assertEqual(tres, 0, msg='初始化创建表')
        data_dict = read_excel(r"" + path + "\TestData\\test_001.xlsx", header=None)
        for sql in data_dict:
            tableOpt.querySql(sql[0])  # 写入表

    @classmethod
    def tearDownClass(cls) -> None:

        #删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')
    # !!!当前用例，所有有行数返回的均需要做值的正确性验证，未完成...
    def test_select_029(self):
        '''
        日期格式年-月-日，开始时间<结束时间
        验证行数和验证每行的格式是否是正确的字段类型
        '''
        sql = "select * from "+self.tb+" where time between '2022-03-28' and '2022-03-29'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row ,39 , msg='验证查询到的行数')
        # #
        # while res.cursor_next() == 0:
        #     timekey = res.get_datetime_ms(0)
        #     f1 = res.get_int(1)
        #     f2 = res.get_string(2)
        #     f3 = res.get_int64(3)
        #     f4 = res.get_int(4)
        #     print(f1)
    def test_select_030(self):
        '''
        日期格式年-月-日 时:分:秒，开始时间<结束时间, query ok ,11行返回
        '''
        sql = "select * from "+self.tb+" where time between '2022-03-28 10:20:00' and '2022-03-28 10:30:00'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row , 11,msg='验证行数')
    def test_select_031(self):
        '''
        日期格式时间戳，开始时间<结束时间,query ok ,11行返回
        '''
        sql = "select * from "+self.tb+" where time between 1648434000000 and 1648434600000"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row , 11,msg='验证行数')
    def test_select_032(self):
        '''
        日期格式年-月-日 开始时间> 结束时间，查询成功,39条返回
        '''
        sql = "select * from "+self.tb+" where time between '2022-03-29' and '2022-03-28'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 39, msg='验证行数')
    def test_select_033(self):
        '''
        SELECT 字段1，字段2…from查时间范围，日期格式 年/月/日，开始时间<结束时间,89条返回
        '''
        sql = "select * from " + self.tb + " where time between '2022/03/28' and '2022/03/30'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 89, msg='验证行数')
    def test_select_034(self):
        '''
        SELECT 字段1，字段3…from查时间范围，日期格式 年/月/日，开始时间>结束时间,89行返回
        '''
        sql = "select time,f1,f2,f3,f4 from " + self.tb + " where time between '2022/03/30' and '2022/03/28'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 89, msg='验证行数')
    def test_select_035(self):
        '''
        time = '年/月/日', 0行返回
        '''
        sql = "select * from "+self.tb+" where time = '2022/03/28'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 0, msg='验证行数')
    def test_select_036(self):
        '''
        time == '年/月/日', 0行返回
        '''
        sql = "select * from " + self.tb + " where time == '2022/03/28'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 0, msg='验证行数')
    def test_select_037(self):
        '''
        time == '年/月/日 时:分:秒.毫秒',1行返回
        '''
        sql = "select * from " + self.tb + " where time== '2022/03/28 10:20:00.000'"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row,1, msg='验证行数')
    def test_select_038(self):
        '''
        '年/月/日' == time,0行返回
        '''
        sql = "select * from " + self.tb + " where '2022/03/28' == time"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 0, msg='验证行数')
    def test_select_039(self):
        '''
            ‘年/月/日' = time,0行返回
        '''
        sql = "select * from " + self.tb + " where '2022/03/28' = time"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 0, msg='验证行数')
    def test_select_040(self):
        '''
        ''年/月/日 时:分:秒.毫秒' = time,1行返回
        '''
        sql = "select * from " + self.tb + " where  '2022/03/28 10:20:00.000' = time"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 1, msg='验证行数')
    def test_select_041(self):
        '''
        time = 时间戳,1行返回
        '''
        sql = "select * from " + self.tb + " where  time = 1648434600000"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 1, msg='验证行数')
    def test_select_042(self):
        '''
        time ==时间戳, 1行返回
        '''
        sql = "select * from " + self.tb + " where  time == 1648434600000"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row, 1, msg='验证行数')
    def test_select_044(self):
        '''
        and多条件查询 字段1=值1 and 字段2=值2, query fail
        '''
        sql = "select * from "+self.tb+" where f1=40 and f2='29号'"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_045(self):
        '''
        and多条件查询 字段1==值1 and 字段2==值2,query fail
        '''
        sql = "select * from "+self.tb+" where f1==40 and f2=='29号'"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_046(self):
        '''
        and多条件查询 字段1>值1 and 字段2>值2,query fail
        select * from test_tb_001 where f3>140 and f4>700
        '''
        sql = "select * from "+self.tb+" where f3>140 and f4>700"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_047(self):
        '''
        and多条件查询 字段1<值1 and 字段2<值2,query fail
        '''
        sql = "select * from "+self.tb+" where f3<150 and f4<750"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_048(self):
        '''
        and多条件查询 字段1>=值1 and 字段2>=值2,query fail
        '''
        sql = "select * from "+self.tb+" where f3>=140 and f4<=525"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_049(self):
        '''
        and多条件查询 字段1<=值1 and 字段2 <=值2,query fail
        '''
        sql = "select * from "+self.tb+" where f3<=140 and f4<=740"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_050(self):
        '''
        and多条件查询 字段1<=值1 and 字段2 <=值2,query fail
        '''
        sql = "select count * from "+self.tb+""
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_051(self):
        '''
        count(*),一共145条数据，1行返回
        '''
        sql = "select count(*) from "+self.tb+""
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertTrue(row == 1, msg='1行返回')
        # 需要验证具体的值是否是145 ......
    def test_select_052(self):
        '''
        count(*)和and 多条件连查,query fail
        '''
        sql = "select count(*) from "+self.tb+" where f1=1 and f2='29号'"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_053(self):
        '''
        count(*) as 别名使用关键字 , query fail
        '''
        sql = "select count(*)  as count from "+self.tb+" where f1=1 and f2='28号'"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_054(self):
        '''
        count(*) as 别名使用中文 , query fail
        '''
        sql = "select count(*)  as 数量 from "+self.tb+"  where f1=1 and f2='28号'"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_055(self):
        '''
        count(*) as 别名使用_字母组合,query fail
        '''
        sql = "select count(*) as _test from "+self.tb+" where f1=1 and f2='28号'"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')
    def test_select_056(self):
        '''
        count（*）中文小括号,query fail
        '''
        sql = "select count（*）from "+self.tb+"  where f3=140 and f4=740"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='query fail')