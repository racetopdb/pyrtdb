# -*- coding: utf-8 -*-
from TestCases.dbManage.setupModule import *
import time
logger = logging.getLogger('main.Test_db_drop')

class Test_db_drop(unittest.TestCase):

    def test_db_060(self):
        '''
        删除一个已经存在的库
        '''
        dbName = 'test_' + str(int(time.time()))
        res = createDB.createSql(dbName)
        self.assertEqual(res , 0, msg='先创建一个库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'],dbName,msg='验证创建的库和查询到的库是否一致')
        dRes = createDB.dropDB(dbName)
        self.assertEqual(dRes , 0 ,msg='删除创建的数据库db_060')
        row = createDB.rowNum()
        self.assertEqual(row ,0 ,msg='db_060删除完之后，剩下0行')
    def test_db_061(self):
        '''
        删除一个不存在的库
        '''
        dbName = 'test061_' + str(int(time.time()))
        res = createDB.dropDB(dbName)
        self.assertTrue(res != 0, msg='删除失败')

    def test_db_062(self):
        '''
        删除一个已经删除过的库
        '''
        dbName = 'test062_' + str(int(time.time()))
        res = createDB.createSql(dbName)
        self.assertEqual(res, 0, msg='先创建一个库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName, msg='验证创建的库和查询到的库是否一致')
        dRes = createDB.dropDB(dbName)
        self.assertEqual(dRes, 0, msg='删除创建的数据库db_062')
        row = createDB.rowNum()
        self.assertEqual(row, 0, msg='db_062删除完之后，剩下0行')
        dRes2 = createDB.dropDB(dbName)
        self.assertTrue(dRes2 !=0, msg='删除一个已经删除的库，fail')
    def test_db_063(self):
        '''
        删除正在运行的库，
        手动执行此用例
        '''
        pass
    def test_db_064(self):
        '''
        删除正在执行脚本写入的库，
        手动执行此用例
        '''
        pass
    def test_db_065(self):
        '''
        删除一个数据量很大的库，
        手动执行此用例，看看服务是否hang住
        '''
        pass
    def test_db_066(self):
        '''
        删除一个名称拼写错的库
        '''
        dbName ='test066'
        res = createDB.createSql(dbName)
        self.assertEqual(res ,0 ,msg='创建一个库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'] , dbName ,msg='验证创建的库名和查询到的库名是否一致')
        dRes = createDB.dropDB('tes066')  #dbname拼写错误
        self.assertTrue( dRes != 0,msg='库名拼写错误，删除失败')
    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_067(self):
        '''
        win: 使用路径删除一个库，query fail
        '''
        sql = 'create db @"E:/JunXia_test/testdb067"'
        res = createDB.createSql(None,sql)
        self.assertEqual(res ,0 ,msg='带路径创建数据库失败')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb067', msg='验证创建的库名和查询到的库名是否一致')
        dRes = createDB.dropDB('"E:/JunXia_test/testdb067"')
        self.assertTrue(dRes != 0, msg='带路径，删除失败')
        dRes2 = createDB.dropDB('testdb067')
        self.assertTrue(dRes2 == 0, msg='删除创建的数据库')

    @unittest.skipIf(platform['system'] == 'Windows', 'windows平台跳过此用例')
    def test_db_068(self):
        '''
        linux: 使用路径删除一个库，路径带引号，query fail
        '''
        sql = "create db '/junxiatest/testdb068'"
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0, msg='带路径创建数据库失败')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb068', msg='验证创建的库名和查询到的库名是否一致')
        dRes = createDB.dropDB('"/junxiatest/testdb068"')
        self.assertTrue(dRes != 0, msg='带路径，删除失败')
        dRes2 = createDB.dropDB('testdb068')
        self.assertTrue(dRes2 == 0, msg='删除创建的数据库')