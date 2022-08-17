# -*- coding: utf-8 -*-
from TestCases.tableManage.setupModule import *
import unittest
from Comm.pyrtdb import conn
from time import *
import datetime
from Conf.config import *
from Lib.tableOpt import *

db = 'test_tb_create' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

class Test_tb_create(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:

        res = conn.query("create db if not exists  " + db + ";")
        cls().assertEqual(res, 0, msg='初始化创建数据库失败')
        usql = 'use ' + db + ''
        ret = createDB.createSql(None, usql)
        cls().assertEqual( ret , 0, msg='初始化use数据库失败')

    @classmethod
    def tearDownClass(cls) -> None:

        # r = conn.query("drop db " + db + ";")
        dropDb = createDB.dropDB(db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_tb_004(self):
        '''
        使用create table 创建表 ,query ok
        '''
        tb = 'table1'
        cRes = tableOpt.createTb(tb,
                          {
                              'f1':data_type['int'],
                              'f2':data_type['bigint'],
                              'f3':data_type['float'],
                              'f4':data_type['bool'],
                              'f5':data_type['double'],
                              'f6':data_type['timestamp'],
                              'f7':data_type['varchar']+'(50)'
                          }
                          )
        self.assertEqual(cRes , 0, msg='tb_004创建表失败')
        desc = tableOpt.describeTb(tb)

        self.assertEqual(desc['name'] , ['time','f1','f2','f3','f4','f5','f6','f7'] ,msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'float', 'bool', 'float', 'timestamp', 'varchar'],
                         msg='验证字段类型')
        self.assertEqual(desc['lens'] ,[8, 4, 8, 4, 1, 4, 8, 50] ,msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop , 0 ,msg='tb_004删除创建的表')
    def test_tb_005(self):
        '''
        if not exist在表名前面创建数据库 , query ok
        '''
        tb = 'if not exist table2'
        cRes = tableOpt.createTb(tb,
                          {
                              'f1':data_type['int'],
                              'f2':data_type['bigint'],
                              'f3': data_type['float'],
                              'f4': data_type['bool'],
                              'f5': data_type['double'],
                              'f6': data_type['timestamp'],
                              'f7': data_type['varchar']+'(10)',
                          })
        self.assertEqual(cRes , 0 , msg='tb_005创建表失败')
        desc = tableOpt.describeTb('table2')

        self.assertEqual(desc['name'], ['time', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'float', 'bool', 'float', 'timestamp', 'varchar'],
                         msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 4, 1, 4, 8, 10], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')

        drop = tableOpt.dropTb('table2')
        self.assertEqual(drop, 0, msg='tb_005删除创建的表')
    def test_tb_006(self):
        '''
        if not exist在表名后面创建数据库 ,query ok
        '''
        tb = ' table3  if not exist '
        cRes = tableOpt.createTb(tb,
                          {
                              'f1':data_type['int'],
                              'f2': data_type['bigint'],
                              'f3': data_type['float'],
                              'f4': data_type['bool'],
                              'f5': data_type['double'],
                              'f6': data_type['timestamp'],
                              'f7': data_type['varchar']+'(10)'
                          })
        self.assertEqual(cRes , 0 ,msg='tb_006创建表失败')
        desc = tableOpt.describeTb('table3')
        self.assertEqual(desc['name'], ['time', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'float', 'bool', 'float', 'timestamp', 'varchar'],
                         msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 4, 1, 4, 8, 10], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')

        drop = tableOpt.dropTb('table3')
        self.assertEqual(drop, 0, msg='tb_006删除创建的表')
    def test_tb_007(self):
        '''
        if not exist在最后创建语句创建数据库, query fail
        '''
        csql = 'create table table4(f1 int,f2 bigint,f3 float,f4 bool,f5 double,f6 timestamp,f7 varchar(10)) if not exist '
        cRes = tableOpt.createTb(None,{},csql)
        self.assertTrue(cRes != 0 , msg='tb_007创建表失败')
        row = tableOpt.tbRowNum()
        self.assertTrue(row == 0, msg='返回0行')
    def test_tb_008(self):
        '''
        IFNOTEXIST大写在表名前面创建数据库，query ok
        '''
        tb = ' IF NOT EXIST table005 '
        cRes = tableOpt.createTb(tb,
                                 {
                                     'col1':data_type['int'],
                                     'col2':data_type['int']
                                 })
        self.assertEqual(cRes , 0 , msg= 'tb_008创建表失败')
        desc = tableOpt.describeTb('table005')
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'int'],msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb('table005')
        self.assertEqual(drop, 0, msg='tb_008删除创建的表')
    def test_tb_009(self):
        '''
        IFNOTEXIST大写在表名后面创建数据库 query ok
        '''

        cRes = tableOpt.createTb('table006 IF NOT EXIST',
                                 {
                                     'col1':'bool',
                                     'col2':'timestamp'
                                 })
        self.assertEqual(cRes , 0 , msg='tb_009创建表失败')
        desc = tableOpt.describeTb('table006')
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'bool', 'timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 1, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb('table006')
        self.assertEqual(drop, 0, msg='tb_009删除创建的表')
    def test_tb_010(self):
        '''
        IFNOTEXIST大写在创建语句的最后创建数据库, query fail
        '''
        sql = 'create table  table007 (col1 int ,col2 int) IF NOT EXIST'
        cRes = tableOpt.createTb(None,{},sql)
        self.assertTrue(cRes != 0 ,msg='tb_010创建表失败')
    def test_tb_011(self):
        '''
        使用if not exist创建一个已经存在的表,query ok
        '''
        tb = ' if not exist table011 '
        cRes1 = tableOpt.createTb(tb ,
                          {
                              'f1':data_type['int'],
                              'f2':data_type['bigint'],
                              'f3':data_type['float'],
                              'f4':data_type['bool'],
                              'f5':data_type['double'],
                              'f6':data_type['timestamp'],
                              'f7':data_type['varchar']+'(10)'
                          })
        self.assertEqual(cRes1 ,0  , msg='tb_011创建表失败')
        cRes2 = tableOpt.createTb(tb,
                                  {
                                      'col1':data_type['int'],
                                      'col2':data_type['int']
                                  })
        self.assertEqual(cRes2 , 0 ,msg='tb_011创建表失败2')

        desc = tableOpt.describeTb('table011')
        self.assertEqual(desc['name'], ['time', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'float', 'bool', 'float', 'timestamp', 'varchar'],
                         msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 4, 1, 4, 8, 10], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')

        drop = tableOpt.dropTb('table011')
        self.assertEqual(drop, 0, msg='tb_011删除创建的表')
    def test_tb_012(self):
        '''
        大写表名,query ok
        '''
        tb = 'TESTTABLE'
        cRes = tableOpt.createTb(tb,
                          {
                              'col1':data_type['int'],
                              'col2': data_type['int'],
                          })
        self.assertEqual(cRes , 0 , msg='tb_012创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'int'],msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4,  4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_012删除创建的表')
    def test_tb_013(self):
        '''
        小写表名,query ok
        '''
        tb = 'testtable'
        cRes = tableOpt.createTb(tb,
                                 {
                                     'col1': data_type['int'],
                                     'col2': data_type['int'],
                                 })
        self.assertEqual(cRes, 0, msg='tb_013创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_013删除创建的表')
    def test_tb_014(self):
        '''
        先创建一个大写的表名再创建一个同名的小写的表名,query ok
        '''
        c1 = tableOpt.createTb('SSDB',
                               {
                                   'col1': data_type['int'],
                                   'col2': data_type['int'],
                                   'col3': data_type['float']
                               })
        self.assertEqual(c1, 0 , msg='tb_014创建表')
        c2 = tableOpt.createTb('ssdb',
                               {
                                   'col1': data_type['int'],
                                   'col2': data_type['int']
                               })
        self.assertEqual(c2, 0 , msg='tb_014创建表名小写')
        show = tableOpt.showTable(1)
        for k,v in show.items():
            if k==0:
                self.assertEqual(v['name'],'SSDB', msg='验证名称')
                self.assertEqual(v['field'],4, msg='验证字段个数')
            if k == 1:
                self.assertEqual(v['name'], 'ssdb', msg='验证名称2')
                self.assertEqual(v['field'], 3, msg='验证字段个数2')
        drop1 = tableOpt.dropTb('SSDB')
        drop2 = tableOpt.dropTb('ssdb')
        self.assertEqual(drop1, 0, msg='删除大写的数据表')
        self.assertEqual(drop2, 0, msg='删除小写的数据表')

    def test_tb_015(self):
        '''
        表名以数字开头 ,query fail
        '''
        tb = '2test'
        cRes = tableOpt.createTb(tb,
                                 {
                                     'col1':data_type['int'],
                                     'col2':data_type['int']
                                 })
        self.assertTrue(cRes !=0 ,msg='tb_015以数字开头创建表，失败')
    def test_tb_016(self):
        '''
        表名以下划线开头 ,query fail
        '''
        tb = '_test'
        cRes = tableOpt.createTb(tb,
                          {
                              'col1':data_type['int']
                          })
        self.assertTrue(cRes !=0 , msg='tb_016以下划线开头的表名创建失败')
    def test_tb_017(self):
        '''
        表名中文,query ok
        '''
        res = tableOpt.createTb('时序库',{'f1':data_type['int']})
        self.assertEqual(res ,0 , msg='创建表')
        show =tableOpt.showTable()
        self.assertEqual(show['name'] , '时序库' , msg= '验证名称')
        self.assertEqual(show['field'], 2, msg='验证字段数量')
        drop = tableOpt.dropTb('时序库')
        self.assertEqual(drop , 0 ,msg='tb_017删除创建的表')
    def test_tb_018(self):
        '''
        表名以特殊字符*开头 ,query fail
        '''
        res = tableOpt.createTb('*test',{'f1':data_type['int']})
        self.assertTrue(res !=0 ,msg='表名以特殊字符开头，创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row ,0 , msg='创建失败，0行返回')
    def test_tb_019(self):
        '''
        表名以中文状态下的！开头, query ok
        '''
        tb = '！test'
        cRes = tableOpt.createTb(tb,
                                 {
                                     'col1':data_type['int'],
                                     'col2':data_type['int']
                                 })
        self.assertEqual(cRes , 0 ,msg='tb_019使用中文！号创建表成功了')
        show = tableOpt.showTable()
        self.assertEqual(show['name'] , tb , msg='tb019验证名称')
        self.assertEqual(show['field'] , 3, msg='tb019验证字段数量')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop , 0 ,msg='tb_019删除创建的表')
    def test_tb_020(self):
        '''
        表名中间包含特殊字符，query fail
        '''
        tb = 'test*&￥table'
        res = tableOpt.createTb(tb,{'col1':data_type['int']})
        self.assertTrue(res !=0 ,msg='tb_020创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row ,0 , msg='创建失败，行数为0')
    def test_tb_021(self):
        '''
        同一个名字作为表名的创建表, 1query ok, 2query fail
        '''
        tb = 'test_table021'
        c1 = tableOpt.createTb(tb,
                               {
                                   'col1': data_type['int'],
                                   'col2': data_type['int']
                               })
        self.assertEqual(c1, 0, msg='tb_021创建表')
        c2 = tableOpt.createTb(tb,
                               {
                                   'f1': data_type['int']
                               })
        self.assertTrue(c2 != 0, msg='tb_021创建表2')
        desc = tableOpt.describeTb(tb)

        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_021删除创建的表')
    def test_tb_022(self):
        '''
        关键字作为表名, query ok
        '''
        tb = 'create'
        res = tableOpt.createTb(tb,
                          {
                              'col1':data_type['int'],
                              'col2':data_type['bigint']
                          })
        self.assertEqual(res , 0 ,msg='tb_022创建表成功')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_022删除创建的表')
    def test_tb_023(self):
        '''
        以【】在包括列和数据类型 创建表
        '''
        sql = 'create table test1 【col1 int,col2 int】'
        res = tableOpt.createTb(None,{},sql)
        self.assertTrue(res !=0 , msg='tb_023创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row ,0 ,msg='tb_023返回0行')
    def test_tb_024(self):
        '''
        以{}在包括列和数据类型 创建表
        '''
        sql = 'create table table024 【col1 int,col2 int】'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_024创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_024返回0行')
    def test_tb_025(self):
        '''
        以[]在包括列和数据类型 创建表
        '''
        sql = 'create table table_025 [col1 int,col2 int]'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_025创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_025返回0行')
    def test_tb_026(self):
        '''
        以<>在包括列和数据类型 创建表
        '''
        sql = 'create table table_008 <col1 int,col2 int>'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_026创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_026返回0行')
    def test_tb_027(self):
        '''
        以《》在包括列和数据类型 创建表
        '''
        sql = 'create table table_027 《col1 int,col2 int》'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_027创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_027返回0行')
    def test_tb_028(self):
        '''
        以（））在包括列和数据类型 创建表
        '''
        sql = 'create table table_028 (col1 int,col2 int))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res == 0, msg='tb_028创建表失败')
        desc = tableOpt.describeTb('table_028')
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')
        drop = tableOpt.dropTb('table_028')
        self.assertEqual(drop, 0, msg='tb_028删除创建的表')
    def test_tb_029(self):
        '''
        以（（））在包括列和数据类型 创建表,query fail
        '''
        sql ='create table table_029 ((col1 int,col2 int))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_029创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_029返回0行')
    def test_tb_030(self):
        '''
        用空格分隔列与列
        '''
        sql = 'create table table_030 (c1 int c2 int c3 int)'
        res = tableOpt.createTb(None,{},sql)
        self.assertEqual(res, 0,msg='tb_030创建表成功')
        desc = tableOpt.describeTb('table_030')
        self.assertEqual(desc['name'], ['time', 'c1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb('table_030')
        self.assertEqual(drop, 0, msg='tb_030删除创建的表')
    def test_tb_031(self):
        '''
        使用| 分隔列与列
        '''
        sql = 'create table table_031 (c1 int | c2 int | c3 int)'
        res = tableOpt.createTb(None,{},sql)
        self.assertEqual(res, 0,msg='tb_031创建表成功')
        desc = tableOpt.describeTb('table_031')
        self.assertEqual(desc['name'], ['time', 'c1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb('table_031')
        self.assertEqual(drop, 0, msg='tb_031删除创建的表')
    def test_tb_032(self):
        '''
        使用中文逗号分隔,  win上失败了，服务器上是query ok的
        '''
        sql = 'create table table_032 (c1 int ， c2 int ，c3 int)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='tb_032创建表成功')
        desc = tableOpt.describeTb('table_032')
        self.assertEqual(desc['name'], ['time', 'c1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb('table_032')
        self.assertEqual(drop, 0, msg='tb_032删除创建的表')
    def test_tb_033(self):
        '''
        使用*分隔列与列, query ok
        '''
        sql = 'create table table_033 (c1 int * c2 int * c3 int)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='tb_033创建表成功')
        desc = tableOpt.describeTb('table_033')
        self.assertEqual(desc['name'], ['time', 'c1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb('table_033')
        self.assertEqual(drop, 0, msg='tb_033删除创建的表')
    def test_tb_034(self):
        '''
        使用英文逗号分隔
        '''
        sql = 'create table table_034 (c1 int , c2 int , c3 int)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='tb_034创建表成功')
        desc = tableOpt.describeTb('table_034')
        self.assertEqual(desc['name'], ['time', 'c1','c2','c3'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int','int','int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4,4,4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb('table_034')
        self.assertEqual(drop, 0, msg='tb_034删除创建的表')
    def test_tb_035(self):
        '''
        前面列使用空格分隔，最后一列加，
        '''
        sql = 'create table table_035 (c1 int c2 int c3 int,)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='tb_035创建表成功')
        desc = tableOpt.describeTb('table_035')
        self.assertEqual(desc['name'], ['time', 'c1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb('table_035')
        self.assertEqual(drop, 0, msg='tb_035删除创建的表')
    def test_tb_036(self):
        '''
        前面列使用空格，最后一列加中文）， query fail
        '''
        sql = 'create table table_036(c1 int c2 int c3 int)）'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_036创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_036返回0行')
    def test_tb_037(self):
        '''
        列名称全英文字母
        '''
        tb = 'table_037'
        cRes = tableOpt.createTb(tb,
                          {
                              'id':data_type['int'],
                              'name':data_type['varchar']+'(60)'
                          })
        self.assertEqual(cRes , 0 , msg='tb_037创建表失败')
        desc = tableOpt.describeTb(tb)

        self.assertEqual(desc['name'], ['time', 'id', 'name'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int',  'varchar'],msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 60], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_037删除创建的表')
    def test_tb_038(self):
        '''
        列名称数字开头,query fail
        '''
        sql = 'create table table_038(1c int ,2c int)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_038创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_038返回0行')
    def test_tb_039(self):
        '''
        列名称下划线开头, query fail
        '''
        sql = 'create table table_019(_col1 int ,_col2 int)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_039创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='tb_039返回0行')
    def test_tb_040(self):
        '''
        列名称为汉字, 服务器上ok， win上fail
        '''
        tb = 'table_040'
        cRes = tableOpt.createTb(tb,
                                 {
                                     '顺实科技': data_type['int'],
                                     '时序库': data_type['varchar'] + '(60)'
                                 })
        self.assertEqual(cRes, 0, msg='tb_040创建表失败')
        desc = tableOpt.describeTb(tb)

        self.assertEqual(desc['name'], ['time', '顺实科技', '时序库'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'varchar'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 60], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_040删除创建的表')
    def test_tb_041(self):
        '''
        列名称为汉字+数字组合 ,服务器上ok， win上fail
        '''
        tb = 'table_041'
        cRes = tableOpt.createTb(tb,
                                 {
                                     '顺实88': data_type['int'],
                                     '科技99': data_type['int']
                                 })
        self.assertEqual(cRes, 0, msg='tb_041创建表失败')
        desc = tableOpt.describeTb(tb)

        self.assertEqual(desc['name'], ['time', '顺实88', '科技99'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_041删除创建的表')
    def test_tb_042(self):
        '''
        列名称为英文+汉字组合，执行成功 query ok
        '''
        tb = 'table_042'
        res = tableOpt.createTb(tb,
                          {
                              'test_顺实':data_type['int'],
                              'test_科技':data_type['int']
                          })
        self.assertEqual(res ,0  ,msg='tb_042创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'test_顺实', 'test_科技'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')

        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_042删除创建的表')
    def test_tb_043(self):
        '''
        列名称以特殊符号*开头，query fail
        '''
        tb = 'table_043'
        res = tableOpt.createTb(tb,
                                {
                                    '*co11': data_type['int'],
                                    '*col2': data_type['int']
                                })
        self.assertTrue(res != 0, msg='tb_042创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row , 0 , msg='没有创建成功，返回0行')
    def test_tb_044(self):
        '''
        列名称以特殊符号&开头字母+汉字组合，query fail
        '''
        sql = 'create table table_044(&test顺实 int )'
        res = tableOpt.createTb(None,{},sql)
        self.assertTrue(res !=0 ,msg='tb_044创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_045(self):
        '''
        列名称以下划线开头字母+汉字组合，query fail
        '''
        sql = 'create table table_045(_test顺实 int )'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_045创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_046(self):
        '''
        列名称用()，执行失败
        '''
        sql = 'create table table_046((顺实科技) int)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_046创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_047(self):
        '''
        列名称以数字开头+汉字组合，query fail
        '''
        sql = 'create table table_047(88顺实 int )'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_047创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_048(self):
        '''
        列名称以汉字开头+数字组合，query ok
        '''
        tb = 'table_048'
        res = tableOpt.createTb(tb,
                          {
                              '顺实_88':data_type['int']
                          })
        self.assertEqual(res ,0  ,msg='tb_048创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', '顺实_88'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_048删除创建的表')
    def test_tb_049(self):
        '''
        列名称使用关键字：as  create等，query ok,但是 null 会失败
        '''
        tb = 'table_049'
        res = tableOpt.createTb(tb,
                                {
                                    'create': data_type['int'],
                                    'as': data_type['int'],
                                })
        self.assertEqual(res, 0, msg='tb_049创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'create','as'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int','int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4,4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_049删除创建的表')
    def test_tb_050(self):
        '''
        字段名称中英文混合 ，不指定类型 ，指定长度, query fail
        '''
        sql = 'create table table_050(test顺实 (10))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_050创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_051(self):
        '''
        中英文混合 ，不指定数据类型，不指定长度, query fail
        '''
        sql = 'create table table_051(顺实 , id  )'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_051创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_052(self):
        '''
        中英文混合 ，指定数据类型，不指定长度(varchar不指定长度),query failed
        '''
        sql = "create table test_052('顺实' int, id bigint,'数据库' varchar,col2 timestamp,col3 float,col4 double ,col5 boolean )"
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_052创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_053(self):
        '''
        字段名中英文混合，指定类型 ，varchar指定长度，query ok
        '''
        sql = "create table test_053('顺实' int, id bigint,'数据库' varchar(50),col2 timestamp,col3 float,col4 double ,col5 boolean )"
        res = tableOpt.createTb(None,{},sql)
        self.assertEqual(res, 0, msg='tb_053创建表失败')
        desc = tableOpt.describeTb('test_053')
        self.assertEqual(desc['name'], ['time', '顺实', 'id','数据库','col2','col3','col4','col5'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint','varchar','timestamp','float','float','bool'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8,4,8,50,8,4,4,1], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb('test_053')
        self.assertEqual(drop, 0, msg='tb_053删除创建的表')
    def test_tb_054(self):
        '''
        中英文混合，指定类型 ，int float等指定长度, query ok
        '''
        tb = 'table_054'
        res = tableOpt.createTb(tb ,
                          {
                              '顺实':data_type['int']+'(10)',
                              'id': data_type['bigint'] + '(10)',
                              '数据库': data_type['varchar'] + '(10)',
                              'col2': data_type['timestamp'] + '(10)',
                              'col3': data_type['float'] + '(2)',
                              'col4': data_type['double'] + '(2)',
                              'col5': data_type['bool'] + '(2)',
                          })
        self.assertEqual(res ,0 , msg='tb_054创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', '顺实', 'id', '数据库', 'col2', 'col3', 'col4', 'col5'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'varchar', 'timestamp', 'float', 'float', 'bool'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 10, 8, 4, 4, 1], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_054删除创建的表')
    def test_tb_055(self):
        '''
        全中文字段 ，不指定类型和长度,query failed
        '''
        sql = 'create table table_055(顺实,科技,公司)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_055创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_056(self):
        '''
        全中文字段，不指定类型，指定长度, query fail
        '''
        sql = "create table table_056('顺实'(10),'科技'(10),'公司'(5))"
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_056创建失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_057(self):
        '''
        全中文字段，指定类型，指定长度query ok
        '''
        tb = 'table_057'
        res = tableOpt.createTb(tb ,
                          {
                              '顺实':data_type['int'],
                              '科技': data_type['bigint']+'(10)',
                              '公司': data_type['varchar']+'(20)'
                          })
        self.assertEqual(res ,0 , msg='tb_057创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', '顺实', '科技', '公司'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'varchar'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 20], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_057删除创建的表')
    def test_tb_058(self):
        '''
        全中文字段,指定类型，不指定长度(不包含varchar类型),query ok
        '''
        tb = 'table_058'
        res = tableOpt.createTb(tb,
                          {
                              '顺实':data_type['int'],
                              '科技':data_type['bigint'],
                              '公司':data_type['float']
                          })
        self.assertEqual(res , 0 , msg='tb_058创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', '顺实', '科技', '公司'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'float'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, 0, msg='tb_058删除创建的表')
    def test_tb_059(self):
        '''
        全中文字段 ，指定类型， 不指定长度(包含varchar类型）query failed
        '''
        tb = 'table_059'
        res = tableOpt.createTb(tb,
                                {
                                    '顺实': data_type['int'],
                                    '科技': data_type['bigint'],
                                    '公司': data_type['float'],
                                    '数据库': data_type['varchar'],
                                })
        self.assertTrue(res != 0, msg='tb_058创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_060(self):
        '''
        列名相同，创建表 ,query fail
        '''
        sql = 'create table table_060(name varchar(10),name int)'
        res = tableOpt.createTb(None,{},sql)
        self.assertTrue(res != 0 ,msg='tb_060创建表成功')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')





























