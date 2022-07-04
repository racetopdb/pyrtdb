# -*- coding: utf-8 -*-
from TestCases.tableManage.setupModule import *
import unittest
from Comm.pyrtdb import conn
from time import *
import datetime
from Conf.config import *
from Lib.tableOpt import *


db = 'test_tb_create2' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

class Test_tb_create2(unittest.TestCase):
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
    def test_tb_061(self):
        '''
        不设定数据类型,query fail
        '''
        sql = 'create table table_061(col1 ,col2,col3)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='tb_061创建表成功')
        conn.get_db_current()
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_062(self):
        '''
        设定数据类型 query ok
        '''
        tb = 'table_062'
        res = tableOpt.createTb(tb,
                          {
                              'col1':data_type['int'],
                              'col2': data_type['float'],
                              'col3': data_type['bigint'],
                              'col4': data_type['timestamp'],
                              'col5': data_type['bool'],
                              'col6': data_type['varchar']+'(10)',
                              'col7': data_type['double'],
                          })
        self.assertEqual(res ,0 ,msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        # print(desc)
        # print([x.strip() for x in desc['type']])
        self.assertEqual([x.strip() for x in desc['name']], ['time', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'], msg='验证字段名称')
        self.assertEqual([x.strip() for x in desc['type']], ['timestamp', 'int', 'float', 'bigint','timestamp','bool','varchar','double'], msg='验证字段类型')
        self.assertEqual([x.strip() for x in desc['lens']], [8, 4, 4, 8,8,1,10,4], msg='验证字段长度')
        self.assertEqual([x.strip() for x in desc['isList']], [False, True, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=' '+ tb + ' 删除创建的表')
    def test_tb_063(self):
        '''
        类型的长度设置，int float double timestamp boolean varchar bigint 全都设置类型长度值,query ok
        '''
        tb = 'table_063'
        res = tableOpt.createTb(tb,
                          {
                              'col1':data_type['int']+'(10)',
                              'col2': data_type['float']+'(10)',
                              'col3': data_type['bigint']+'(10)',
                              'col4': data_type['timestamp']+'(10)',
                              'col5': data_type['bool']+'(10)',
                              'col6': data_type['varchar']+'(10)',
                              'col7': data_type['double']+'(10)',
                          })
        self.assertEqual(res ,0 ,msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'float', 'bigint','timestamp','bool','varchar','double'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 4, 8,8,1,10,4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_064(self):
        '''
        int 设置类型长度为0  ,query ok
        '''
        tb = 'table_064'
        sql = 'create table '+tb+'(f1 int (0))'
        res = tableOpt.createTb(None,{},sql)
        self.assertEqual(res ,0 ,msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_065(self):
        '''
        int设置类型长度 为10 ,query ok
        '''
        tb = 'table_065'
        sql = 'create table '+tb+'(f1 int(10))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_066(self):
        '''
        int 设置类型长度 为250
        '''
        tb = 'table_066'
        sql = 'create table '+tb+'(f1 int(250))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_067(self):
        '''
        bigint 设置类型长度 为0
        '''
        tb = 'table_067'
        sql = 'create table '+tb+'(f1 bigint(0))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'bigint'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_068(self):
        '''
        bigint设置类型长度 为10
        '''
        tb = 'table_068'
        sql = 'create table '+tb+'(f1 bigint(10))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'bigint'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_069(self):
        '''
        bigint 设置类型长度 为250
        '''
        tb = 'table_069'
        sql = 'create table '+tb+'(f1 bigint(250))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'bigint'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_070(self):
        '''
        float 设置类型长度 为0
        '''
        tb = 'table_070'
        sql = 'create table '+tb+'(f1 float(0))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'float'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_071(self):
        '''
        float设置类型长度 为10
        '''
        tb = 'table_071'
        sql = 'create table '+tb+'(f1 float(10))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'float'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_072(self):
        '''
        float设置类型长度 为250
        '''
        tb = 'table_072'
        sql = 'create table '+tb+'(f1 float(250))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'float'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_073(self):
        '''
        double 设置类型长度 为0
        '''
        tb = 'table_073'
        sql = 'create table '+tb+'(f1 double(0))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'float'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_074(self):
        '''
        double设置类型长度 为10
        '''
        tb = 'table_074'
        sql = 'create table '+tb+'(f1 double(10))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'float'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')

    def test_tb_075(self):
        '''
        double设置类型长度 为250
        '''
        tb = 'table_075'
        sql = 'create table '+tb+'(f1 double(250))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'float'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_076(self):
        '''
        timestamp设置类型长度 为0
        '''
        tb = 'table_076'
        sql = 'create table '+tb+'(f1 timestamp(0))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_077(self):
        '''
        timestamp设置类型长度 为10
        '''
        tb = 'table_077'
        sql = 'create table '+tb+'(f1 timestamp(10))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_078(self):
        '''
        timestamp设置类型长度 为250
        '''
        tb = 'table_078'
        sql = 'create table '+tb+'(f1 timestamp(250))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_079(self):
        '''
        boolean设置类型长度 为0
        '''
        tb = 'table_079'
        sql = 'create table '+tb+'(f1 bool(0))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'bool'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 1], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_080(self):
        '''
        boolean类型长度 为10
        '''
        tb = 'table_080'
        sql = 'create table '+tb+'(f1 bool(10))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'bool'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 1], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_081(self):
        '''
        boolean设置类型长度 为250
        '''
        tb = 'table_081'
        sql = 'create table '+tb+'(f1 bool(250))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'bool'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 1], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg=''+tb+'删除创建的表')
    def test_tb_082(self):
        '''
        varchar设置类型长度为0, query fail
        '''
        tb = 'table_082'
        sql = 'create table '+tb+'(f1 varchar(0))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg=''+tb+'创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg=''+tb+'返回0行')
    def test_tb_083(self):
        '''
        varchar设置类型长度为1,query ok
        '''
        tb = 'table_083'
        sql = 'create table ' + tb + '(f1 varchar(1))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'varchar'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 1], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_084(self):
        '''
        varchar设置类型长度为250
        '''
        tb = 'table_084'
        sql = 'create table ' + tb + '(f1 varchar(250))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'varchar'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 250], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_085(self):
        '''
        varchar设置类型长度为254, query ok
        '''
        tb = 'table_085'
        sql = 'create table ' + tb + '(f1 varchar(254))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'f1'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'varchar'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 254], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_086(self):
        '''
        varchar设置类型长度为255, query fail
        '''
        tb = 'table_086'
        sql = 'create table ' + tb + '(f1 varchar(255))'
        res = tableOpt.createTb(None, {}, sql)
        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row ,0  ,msg='' + tb + '返回0行')
    def test_tb_087(self):
        '''
        指定类型，指定长度, queryo k
        '''
        tb = 'table_087'
        res = tableOpt.createTb(tb,
                          {
                              'col1':data_type['int']+'(10)',
                              'col2': data_type['bigint'] + '(10)',
                              'col3': data_type['bool'] + '(10)',
                              'col4': data_type['varchar'] + '(10)',
                              'col5': data_type['float'] + '(10)',
                              'col6': data_type['double'] + '(10)',
                              'col7': data_type['timestamp'] + '(10)',
                          })
        self.assertEqual(res ,0,msg=''+tb+'创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time','col1','col2','col3','col4','col5','col6','col7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp','int','bigint','bool', 'varchar','float','float','timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4,8,1,10,4,4,8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_088(self):
        '''
        指定类型，不指定长度(包含varchar类型） query fail
        '''
        tb = 'table_088'
        res = tableOpt.createTb(tb,
                          {
                              'col1':data_type['int'],
                              'col2': data_type['bigint'],
                              'col3': data_type['bool'] ,
                              'col4': data_type['varchar'],
                              'col5': data_type['float'] ,
                              'col6': data_type['double'] ,
                              'col7': data_type['timestamp'] ,
                          })
        self.assertTrue(res !=0,msg=''+tb+'创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row , 0 ,msg=''+tb+'返回0行')
    def test_tb_089(self):
        '''
        指定类型，不指定长度(不包含varchar类型）,query ok
        '''
        tb = 'table_089'
        res = tableOpt.createTb(tb,
                                {
                                    'col1': data_type['int'],
                                    'col2': data_type['bigint'],
                                    'col3': data_type['bool'],
                                    'col5': data_type['float'],
                                    'col6': data_type['double'],
                                    'col7': data_type['timestamp'],
                                })
        self.assertEqual(res , 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2', 'col3',  'col5', 'col6', 'col7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'bool' ,'float', 'float', 'timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 1, 4, 4, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_090(self):
        '''
        不指定类型，指定长度, query fail
        '''
        tb = 'table_090'
        res = tableOpt.createTb(tb,
                                {
                                    'col1': '(10)',
                                    'col2': '(10)',
                                    'col3': '(10)',
                                    'col4': '(10)',
                                    'col5': '(10)',
                                    'col6': '(10)',
                                    'col7': '(10)',
                                })
        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')
    def test_tb_091(self):
        '''
        不指定类型，不指定长度,query fail
        '''
        tb = 'table_091'
        sql ='create table '+tb+'(col1,col2,col3)'
        res = tableOpt.createTb(tb,{},sql)
        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')
    def test_tb_092(self):
        '''
        int等类型不指定长度，varchar指定长度, query ok
        '''
        tb = 'table_092'
        res = tableOpt.createTb(tb,
                                {
                                    'col1': data_type['int'] ,
                                    'col2': data_type['bigint'] ,
                                    'col3': data_type['bool'] ,
                                    'col4': data_type['varchar'] + '(20)',
                                    'col5': data_type['float'] ,
                                    'col6': data_type['double'] ,
                                    'col7': data_type['timestamp'],
                                })
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'bool', 'varchar', 'float', 'float', 'timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 1, 20, 4, 4, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_093(self):
        '''
        列名在数据类型的后面(不包括varchar类型)，query ok
        '''
        tb = 'table_093'
        res = tableOpt.createTb(tb,
                                {
                                    data_type['int']: 'col1',
                                    data_type['bigint']: 'col2',
                                    data_type['bool']: 'col3',
                                    data_type['float']: 'col5',
                                    data_type['double']: 'col6',
                                    data_type['timestamp']: 'col7',
                                })
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2', 'col3',  'col5', 'col6', 'col7'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'int', 'bigint', 'bool', 'float', 'float', 'timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 4, 8, 1,  4, 4, 8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True, True, True, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_094(self):
        '''
        数据类型为varchar的在列名的前面,query failed
        '''
        tb = 'table_094'
        sql = 'create table ' + tb + '(varchar col1 ,col2 int)'
        res = tableOpt.createTb(tb, {}, sql)
        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')
    def test_tb_095(self):
        '''
        数据类型为varchar 的在列名的后面并设置长度,query ok
        '''
        tb = 'table_095'
        res = tableOpt.createTb(tb,
                                {
                                    'col1' : data_type['varchar']+'(20)',
                                    'col2': data_type['int']
                                })
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'varchar','int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 20, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_096(self):
        '''
        数据类型为varchar ，长度设为0,query failed
        '''
        tb = 'table_095'
        res = tableOpt.createTb(tb,
                                {
                                    'col1': data_type['varchar'] + '(0)',
                                    'col2': data_type['int']
                                })

        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')
    def test_tb_097(self):
        '''
        数据类型为varchar ，长度溢出,query failed
        '''
        tb = 'table_097'
        res = tableOpt.createTb(tb,
                                {
                                    'col1': data_type['varchar'] + '(255)',
                                    'col2': data_type['int']
                                })

        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')
    def test_tb_098(self):
        '''
        列 设为null,query ok
        '''
        tb = 'table_098'
        res = tableOpt.createTb(tb,
                                {
                                    'col1': data_type['varchar'] + '(25) null ',
                                    'col2': data_type['int'] + ' null '
                                })
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'varchar', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 25, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_099(self):
        '''
        列设为not null, query ok
        '''
        tb = 'table_099'
        res = tableOpt.createTb(tb,
                                {
                                    'col1': data_type['varchar'] + '(25) not null ',
                                    'col2': data_type['int'] + ' not null '
                                })
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'col1', 'col2'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'varchar', 'int'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 25, 4], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, False, False], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_100(self):
        '''
        0个字段, query fail
        '''
        tb = 'table_100'
        sql = 'create table '+tb+'()'
        res = tableOpt.createTb(tb,{},sql)
        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')

    def test_tb_101(self):
        '''
        1个字段 ,query ok
        '''
        tb = 'table_101'
        res = tableOpt.createTb(tb,
                                {
                                    'name': data_type['varchar'] + '(25)'
                                })
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        desc = tableOpt.describeTb(tb)
        self.assertEqual(desc['name'], ['time', 'name'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp', 'varchar'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8, 25], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False, True], msg='验证是否空')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_102(self):
        '''
        288个字段,query ok
        字段数量的边界值不明，稍后再说
        '''
        pass
    def test_tb_104(self):
        '''
        create table 不带字段创建表，query ok
        '''
        sql = 'create table show'
        res = tableOpt.createTb(None,{},sql)
        self.assertEqual(res , 0 ,msg='tb_104创建表失败')
        desc = tableOpt.describeTb('show')
        self.assertEqual(desc['name'], ['time'], msg='验证字段名称')
        self.assertEqual(desc['type'], ['timestamp'], msg='验证字段类型')
        self.assertEqual(desc['lens'], [8], msg='验证字段长度')
        self.assertEqual(desc['isList'], [False], msg='验证是否空')
        drop = tableOpt.dropTb('show')
        self.assertEqual(drop, None, msg='tb_104删除创建的表')
    def test_tb_105(self):
        '''
        creat 拼写有误 ,query fail
        '''
        tb = 'table_105'
        sql = 'creat table ' + tb + '()'
        res = tableOpt.createTb(tb, {}, sql)
        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')
    def test_tb_106(self):
        '''
        create 不加关键字table 创建表, query fail
        '''
        tb = 'table_106'
        sql = 'creat  ' + tb + '()'
        res = tableOpt.createTb(tb, {}, sql)
        self.assertTrue(res != 0, msg='' + tb + '创建表失败')
        row = tableOpt.tbRowNum()
        self.assertEqual(row, 0, msg='' + tb + '返回0行')
    def test_tb_109(self):
        '''
        删除存在的表, query ok
        '''
        tb = 'table_109'
        sql = 'create table '+tb+'(id int)'
        res = tableOpt.createTb(None,{},sql)
        self.assertEqual(res, 0, msg=''+tb+'创建表失败')
        drop = tableOpt.dropTb(tb)
        self.assertEqual(drop, None, msg='' + tb + '删除创建的表')
    def test_tb_110(self):
        '''
        删除不存在的表, query fail
        '''
        tb = 'table_110'
        drop = tableOpt.dropTb(tb)
        self.assertTrue(drop != None, msg='' + tb + '删除创建的表')
    def test_tb_111(self):
        '''
        drop 不带table关键字删除表 ,query fail
        '''
        tb = 'table_111'
        sql = 'create table ' + tb + '(id int)'
        res = tableOpt.createTb(None, {}, sql)
        self.assertEqual(res, 0, msg='' + tb + '创建表失败')
        drop = tableOpt.dropTb(tb,'drop '+tb+' ')
        self.assertTrue(drop !=None, msg='' + tb + '删除失败')
    def test_tb_112(self):
        '''
        删除数据量千万级别以上的表 , pass . 需要手动执行
        '''
        pass


