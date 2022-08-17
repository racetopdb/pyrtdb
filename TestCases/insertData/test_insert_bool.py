# -*- coding: utf-8 -*-
import time
import unittest
from Comm.pyrtdb import conn
import datetime
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import logging
from Comm.convert import *
# from TestCases.insertData.setUpInsert import *

class Test_insert_bool(unittest.TestCase):
    db = 'test_insert_value' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    tb = 't_bool'
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres =tableOpt.createTb(cls.tb,{'f1':data_type['bool']})
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')
        
    def test_insert_066(self):
        '''
        写入boolean类型，数据填入TRUE,querok
        '''
        sql = 'insert into '+self.tb+'(f1) values(TRUE)'
        res = tableOpt.insertTb(None, [], [] , sql)
        self.assertEqual(res , 0, msg='insert_066写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, True, msg='验证f1值')
    def test_insert_067(self):
        '''
        写入boolean类型，数据填入FALSE,query ok
        '''

        sql = 'insert into '+self.tb+'(f1) values(FALSE)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='insert_067写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, False, msg='验证f1值')
    def test_insert_068(self):
        '''
        写入boolean类型，数据填入yes
        '''
        sql = 'insert into '+self.tb+'(f1) values(yes)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='insert_068写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, True, msg='验证f1值')
    def test_insert_069(self):
        '''
        写入boolean类型，数据填入no,query ok
        '''
        sql = 'insert into ' + self.tb + '(f1) values(no)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_069写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, False, msg='验证f1值')
    def test_insert_070(self):
        '''
        写入boolean类型，数据填入true,query ok
        '''
        sql = 'insert into ' + self.tb + '(f1) values(true)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_070写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, True, msg='验证f1值')
    def test_insert_071(self):
        '''
        写入boolean类型，数据填入false,query ok
        '''

        sql = 'insert into ' + self.tb + '(f1) values(false)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='insert_071写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, False, msg='验证f1值')
    def test_insert_072(self):
        '''
        写入boolean类型，数据填入True,query ok
        '''

        sql = 'insert into ' + self.tb + '(f1) values(True)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_072写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, True, msg='验证f1值')
    def test_insert_073(self):
        '''
        写入boolean类型，数据填入False,query ok
        '''

        sql = 'insert into ' + self.tb + '(f1) values(False)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='insert_073写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, False, msg='验证f1值')
    def test_insert_074(self):
        '''
        写入boolean类型，数据填入YES,query ok
        '''

        sql = 'insert into ' + self.tb + '(f1) values(YES)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_074写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, True, msg='验证f1值')
    def test_insert_075(self):
        '''
        写入boolean类型，数据填入NO,query ok
        '''

        sql = 'insert into ' + self.tb + '(f1) values(NO)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res ,0, msg='insert_075写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, False, msg='验证f1值')
    def test_insert_076(self):
        '''
        写入boolean类型，数据填入Yes
        '''

        sql = 'insert into ' + self.tb + '(f1) values(Yes)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_076写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, True, msg='验证f1值')
    def test_insert_077(self):
        '''
        写入boolean类型，数据填入No,query ok
        '''

        sql = 'insert into ' + self.tb + '(f1) values(No)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='insert_077写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, False, msg='验证f1值')
    def test_insert_078(self):
        '''
        写入boolean类型，数据填入T,query fail
        '''
        sql = 'insert into ' + self.tb + '(f1) values(T)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_078写入失败')
    def test_insert_079(self):
        '''
        写入boolean类型，数据填入F,query fail
        '''
        sql = 'insert into ' + self.tb + '(f1) values(F)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_079写入失败')
    def test_insert_080(self):
        '''
        写入boolean类型，数据填入Y,query fail
        '''
        sql = 'insert into ' + self.tb + '(f1) values(Y)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_080写入失败')
    def test_insert_081(self):
        '''
        写入boolean类型，数据填入N ,query fail
        '''
        sql = 'insert into ' + self.tb + '(f1) values(N)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_081写入失败')
    def test_insert_082(self):
        '''
        写入boolean类型，数据填入1,query ok
        '''
        sql = 'insert into ' + self.tb + '(f1) values(1)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_082写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, True, msg='验证f1值')
    def test_insert_083(self):
        '''
        写入boolean类型，数据填入1,query ok
        '''

        sql = 'insert into ' + self.tb + '(f1) values(0)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='insert_083写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_bool(1)
            self.assertEqual(f1, False, msg='验证f1值')
    def test_insert_084(self):
        '''
        写入boolean类型，字段设置为not null ，数据不填,query fail
        '''
        tb2 = 't_bool2'
        cRes = tableOpt.createTb(tb2,{'f1':data_type['bool']+' not null'})
        self.assertEqual(cRes,0,msg='084创建表失败')
        sql = 'insert into ' + tb2 + '(f1) values('')'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_084写入失败')
        dropTb = tableOpt.dropTb(tb2)
        self.assertEqual(dropTb , 0,msg='084删除创建的表')


