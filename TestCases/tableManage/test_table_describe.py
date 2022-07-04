# -*- coding: utf-8 -*-
import unittest
from TestCases.tableManage.setupClass import *

db = 'test_tb_describe' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
class Test_tb_describe(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('类初始化--创建一个数据库')
        res = conn.query("create db if not exists  " + db + ";")
        print(f'类创建数据库的结果：{res}')
        usql = 'use ' + db + ''
        ret = createDB.createSql(None, usql)
        print(f'类use库结果是：{ret}')
        # cls.assertEqual( res , 0, msg='创建数据库失败')

    @classmethod
    def tearDownClass(cls) -> None:
        print('类清除--删除在初始化时创建的数据库')
        r = conn.query_reader("drop db " + db + ";")
        print(f'删除数据库的结果：{r}')
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
        self.assertEqual(drop, None, msg='tb_113删除创建的表')
    def test_tb_114(self):
        '''
        查看一个其他库的表
        现在已经有了一个test_db库，再创建一个库（query ok）， use 新库 （query ok）
        create 一个表(query ok)
        然后切换到test_db老库里面(query ok)， 去describe 刚刚创建的表(query fail)
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
        self.assertTrue(desc != 0 ,msg='tb_115查看一个不存在的表')

    def test_tb_116(self):
        '''
        describe不加关键字table 查看表
        create table table_093(id int ,name char(20))
        describe  table_093
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
        self.assertEqual(drop, None, msg='tb_116删除创建的表')

