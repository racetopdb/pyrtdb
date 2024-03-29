# -*- coding: utf-8 -*-
from TestCases.tableManage.setupModule import *
import unittest
from Comm.pyrtdb import conn
from time import *
import datetime
from Conf.config import *
from Lib.tableOpt import *

db = 'test_tb_show' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

class Test_tb_show(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')


    @classmethod
    def tearDownClass(cls) -> None:
        '''
        show的类清除
        '''

        dropDb = createDB.dropDB(db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')


    def test_tb_001(self):
        '''
        show table
        '''
        res = tableOpt.createTb('test_001',
                                {
                                    'f1': data_type['int'],
                                    'f2': data_type['bigint']
                                }
                                )
        self.assertEqual(res, 0, msg='tb_001创建表失败')
        show = conn.query_reader('show table')
        while show.cursor_next() == 0:
            name = show.get_string(1)
            field = show.get_int(2)
            row = show.get_int(3)
            self.assertEqual('test_001' , name , msg='验证表名称')
            self.assertEqual(3, field, msg='验证字段数量')
            self.assertEqual(0, row, msg='验证行数')
        drop = tableOpt.dropTb('test_001')
        self.assertEqual(drop , 0 ,msg='删除创建的表')
    def test_tb_002(self):
        '''
        show tables
        '''
        res = tableOpt.createTb('test_002',
                                {
                                    'f1': data_type['int'],
                                    'f2': data_type['bigint'],
                                    'f3':data_type['bool']
                                }
                                )
        self.assertEqual(res, 0, msg='tb_002创建表失败')
        show = conn.query_reader('show tables')
        while show.cursor_next() == 0:
            name = show.get_string(1)
            field = show.get_int(2)
            row = show.get_int(3)
            self.assertEqual('test_002' , name , msg='验证表名称')
            self.assertEqual(4, field, msg='验证字段数量')
            self.assertEqual(0, row, msg='验证行数')
        drop = tableOpt.dropTb('test_002')
        self.assertEqual(drop , 0 ,msg='删除创建的表')
    def test_tb_003(self):
        '''
        show tb
        '''
        res = tableOpt.createTb('test_003',
                                {
                                    'f1': data_type['int'],
                                    'f2': data_type['bigint'],
                                    'f3':data_type['bool']
                                }
                                )
        self.assertEqual(res, 0, msg='tb_003创建表失败')
        show = conn.query_reader('show tb')
        while show.cursor_next() == 0:
            name = show.get_string(1)
            field = show.get_int(2)
            row = show.get_int(3)
            self.assertEqual('test_003' , name , msg='验证表名称')
            self.assertEqual(4, field, msg='验证字段数量')
            self.assertEqual(0, row, msg='验证行数')
        drop = tableOpt.dropTb('test_003')
        self.assertEqual(drop , 0 ,msg='删除创建的表')