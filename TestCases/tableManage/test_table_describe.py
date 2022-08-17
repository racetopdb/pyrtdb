# -*- coding: utf-8 -*-
from TestCases.tableManage.setupModule import *
import unittest
from Comm.pyrtdb import conn
from time import *
import datetime
from Conf.config import *
from Lib.tableOpt import *

db = 'test_tb_describe' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
class Test_tb_describe(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')

    @classmethod
    def tearDownClass(cls) -> None:
        dropDb = createDB.dropDB(db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_tb_113(self):
        '''
        查看一个存在的表, query ok
        '''
        tb = 'table_113'
        cRes = tableOpt.createTb(tb,
                                 {
                                     'f1': data_type['int'],
                                     'f2': data_type['bigint']
                                 }
                                 )
        self.assertEqual(cRes, 0, msg='tb_113创建表失败')
        desc = tableOpt.describeTb(tb)

        self.assertEqual(desc['name'], ['time', 'f1', 'f2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_113删除创建的表')
    def test_tb_114(self):
        '''
        查看一个其他库的表
        '''
        dbName = 'test_db114'
        dbRes = createDB.createSql(dbName)
        self.assertEqual(dbRes , 0 , msg='tb_114创建库成功')
        use = createDB.useDB(dbName)
        self.assertEqual(use ,0 ,msg='tb_114 use 数据库成功')
        currentdb = createDB.currentDB()
        self.assertEqual(currentdb, dbName, msg='tb_114 当前数据库为test_db114')
        tb = 'tb_114'
        res = tableOpt.createTb(tb,
                          {
                              'f1':data_type['int']
                          })
        self.assertEqual(res , 0, msg='tb_114创建表成功')
        use = createDB.useDB(db)
        self.assertEqual(use, 0, msg='tb_114 use 数据库成功')
        parentdb = createDB.currentDB()
        self.assertEqual(parentdb, db, msg=f'当前数据库为父类的库{db}')
        desc = conn.query_reader('describe table ' + tb + '')
        self.assertTrue(desc == None, msg='tb_114查看一个不存在的表')


    def test_tb_115(self):
        '''
        查看一个不存在的表
        '''
        tb = 'table_115'
        desc = conn.query_reader('describe table '+tb+'')
        self.assertTrue(desc == None ,msg='tb_115查看一个不存在的表')

    def test_tb_116(self):
        '''
        describe不加关键字table 查看表
        '''
        tb = 'table_116'
        cRes = tableOpt.createTb(tb,
                                 {
                                     'f1': data_type['int'],
                                     'f2': data_type['bigint']
                                 }
                                 )
        self.assertEqual(cRes, 0, msg='tb_116创建表失败')
        desc = conn.query_reader('describe '+tb+'')
        self.assertTrue(desc == None, msg='tb_116描述失败')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_116删除创建的表')

