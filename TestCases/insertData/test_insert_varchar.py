# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
import datetime
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import logging
from Comm.convert import *


class Test_insert_varchar(unittest.TestCase):
    tb = 't_varchar'
    db = 'test_insert_varchar' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres = tableOpt.createTb(cls.tb, {'f1': data_type['varchar']+'(254)'})
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        # 删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')
       
    def test_insert_052(self):
        '''
        写入varchar类型，数据加单引号‘’,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['顺实科技'])
        self.assertEqual(res, 0, msg='insert_052写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, '顺实科技', msg='验证f1值')
    def test_insert_053(self):
        '''
        写入varchar类型，数据加双引号"",query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ["顺实科技RTDB"])
        self.assertEqual(res, 0, msg='insert_053写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, "顺实科技RTDB", msg='验证f1值')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_insert_054_win(self):
        '''
        写入varchar类型，数据不加引号，直接输入汉字[手动执行fail，自动ok],query fail
        '''
        sql ="insert into "+self.tb+"(f1) values(时序数据库)"
        res = tableOpt.insertTb(None,[],[],sql)
        self.assertTrue(res == 0, msg='insert_054写入失败')

    @unittest.skipIf(platform['system'] == 'Windows', 'windows平台跳过此用例')
    def test_insert_054_linux(self):
        '''
        写入varchar类型，数据不加引号，直接输入汉字,queryok
        '''
        sql = "insert into "+self.tb+"(f1) values(时序数据库)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_054写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, "时序数据库", msg='验证f1值')
    def test_insert_055(self):
        '''
        写入varchar类型，数据不填,query ok
        '''
        sql = "insert into "+self.tb+"(f1) values('')"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_055写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, "", msg='验证f1值')
    def test_insert_058(self):
        '''
        写入varchar类型，数据填入255个溢出字符,query fail
        '''
        val ='abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrsA8'
        res = tableOpt.insertTb(self.tb, ['f1'], [val])
        self.assertTrue(res != 0, msg='insert_058写入失败')
    def test_insert_059(self):
        '''
        写入varchar类型，数据填入1个字符,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['顺'])
        self.assertTrue(res == 0, msg='insert_059写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, "顺", msg='验证f1值')
    def test_insert_060(self):
        '''
        写入varchar类型，数据填入15个字符,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['顺实科技6顺实科技6顺实科技6'])
        self.assertTrue(res == 0, msg='insert_060写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, "顺实科技6顺实科技6顺实科技6", msg='验证f1值')
    def test_insert_061(self):
        '''
        写入varchar类型，数据填入254个字符，临界值,query ok
        '''
        val = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrsA"
        res = tableOpt.insertTb(self.tb, ['f1'], [val])
        self.assertTrue(res == 0, msg='insert_061写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, val, msg='验证f1值')
    def test_insert_062(self):
        '''
        varchar类型写入路径信息的值,使用系统根目录路径,query ok
        '''
        val = "c:\\windows\\a.txt"
        res = tableOpt.insertTb(self.tb, ['f1'], [val])
        self.assertTrue(res == 0, msg='insert_062写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, val, msg='验证f1值')
    def test_insert_063(self):
        '''
        varchar类型写入路径信息的值,使用/路径, query ok
        '''
        val = "/user/bin/rtdb.txt"
        res = tableOpt.insertTb(self.tb, ['f1'], [val])
        self.assertTrue(res == 0, msg='insert_063写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, val, msg='验证f1值')
    def test_insert_064(self):
        '''
        varchar类型写入路径信息的值,使用@转义路径,query ok
        '''
        sql = "insert into "+self.tb+"(f1) values(@'d:\\a.txt')"
        res = tableOpt.insertTb(None, [], [] , sql)
        self.assertTrue(res == 0, msg='insert_063写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, 'd:\\a.txt', msg='验证f1值')
    def test_insert_065(self):
        '''
        varchar类型写入路径信息的值,使用\转义路径
        '''
        sql = "insert into "+self.tb+"(f1) values('d:\\a.txt')"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_063写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, 'd:\\a.txt', msg='验证f1值')




class Test_insert_varchar2(unittest.TestCase):
    tb2 = 't_varchar2'
    db = 'test_insert_varchar2' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres = tableOpt.createTb(cls.tb2, {'f1': data_type['varchar'] + '(254)  not null'})
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        # 删除数据库
        dropTb = tableOpt.dropTb(cls.tb2)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_insert_056(self):
        '''
        写入varchar类型，字段设置为notnull ，数据不填,【！！！应失败，现ok】
        '''
        sql = "insert into "+self.tb2+"(f1) values('')"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_054写入失败')
        lastObj = tableOpt.selectLast(self.tb2)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, "", msg='验证f1值')
    def test_insert_057(self):
        '''
        写入varchar类型，字段设置为notnull ，数据为NULL,query fail
        '''
        sql = "insert into "+self.tb2+"(f1) values(NULL)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_057写入失败')







