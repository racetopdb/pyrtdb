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


class Test_insert_int(unittest.TestCase):
    tb = 't_int'
    db = 'test_insert_int' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres =tableOpt.createTb(cls.tb,{'f1':data_type['int']})
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_insert_001(self):
        '''
        写入表中int整型字段，数据溢出,query fail
        '''
        res = tableOpt.insertTb(self.tb,['f1'],[2147483647])
        self.assertTrue(res != 0,msg='insert_001写入成功')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'] , 0 ,msg='写入失败，返回0行')
    def test_insert_002(self):
        '''
        写入表中int整型字段，数据为临界值,query ok
        '''
        res = tableOpt.insertTb(self.tb,['f1'],[2147483646])
        self.assertEqual(res ,0 ,msg='insert_002写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 2147483646, msg='验证f1值')

    def test_insert_003(self):
        '''
        写入表中int整型字段，数据为正常整型数值
        '''
        res = tableOpt.insertTb(self.tb,['f1'],[112233])
        self.assertEqual(res, 0, msg='insert_003写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 112233, msg='验证f1值')
    def test_insert_004(self):
        '''
        写入表中int整型字段，数据为负数临界值,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], [-2147483648])
        self.assertEqual(res, 0, msg='insert_004写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, -2147483648, msg='验证f1值')
    def test_insert_005(self):
        '''
        写入表中int整型字段，数据为负数溢出值,query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], [-2147483649])
        self.assertTrue(res != 0, msg='insert_005写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertNotEqual(f1, -2147483649, msg='验证f1值')
    def test_insert_006(self):
        '''
        写入表中int整型字段，数据为字母 、汉字、特殊字符,query fail
        '''

        res1 = tableOpt.insertTb(self.tb,['f1'],['顺实'])
        self.assertTrue(res1 != 0 ,msg='insert_006汉字写入整型，写入失败')
        res2 = tableOpt.insertTb(self.tb, ['f1'], ['ss'])
        self.assertTrue(res2 != 0, msg='insert_006字符串写入整型，写入失败')
        res3 = tableOpt.insertTb(self.tb, ['f1'], ['ss'])
        self.assertTrue(res3 != 0, msg='insert_006特殊字符写入整型，写入失败')


class Test_insert_bigint(unittest.TestCase):
    tbBigint = 't_bigint'
    db = 'test_insert_bigint' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres =tableOpt.createTb(cls.tbBigint,{'f1':data_type['bigint']})
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库

        dropTb = tableOpt.dropTb(cls.tbBigint)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_insert_007(self):
        '''
        写入表中bigint类型字段，数据为负数溢出值,query fail
        '''
        res = tableOpt.insertTb(self.tbBigint,['f1'],[-4611686018427387903])
        self.assertTrue(res != 0, msg='insert_007bigint溢出值写入，写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_008(self):
        '''
        写入表中bigint类型字段，数据为负数临界值 query ok
        '''
        res = tableOpt.insertTb(self.tbBigint,['f1'],[-4611686018427387902])
        self.assertEqual(res ,0 ,msg='self.tb_008写入失败')
        lastObj = tableOpt.selectLast(self.tbBigint)
        while lastObj.cursor_next() ==0:
            f1 = lastObj.get_int64(1)
            self.assertEqual(f1,-4611686018427387902,msg='验证f1值失败')
    def test_insert_009(self):
        '''
        写入表中bigint类型字段，数据为正常bigint数值 query ok
        '''
        res = tableOpt.insertTb(self.tbBigint, ['f1'], [4611680183])
        self.assertEqual(res, 0, msg='self.tb_009写入失败')
        lastObj = tableOpt.selectLast(self.tbBigint)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int64(1)
            self.assertEqual(f1, 4611680183, msg='验证f1值失败')
    def test_insert_010(self):
        '''
        写入表中bigint类型字段，数据为正数临界值,queryok
        '''
        res = tableOpt.insertTb(self.tbBigint, ['f1'], [4611686018427387902])
        self.assertEqual(res, 0, msg='self.tb_010写入失败')
        lastObj = tableOpt.selectLast(self.tbBigint)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int64(1)
            self.assertEqual(f1, 4611686018427387902, msg='验证f1值失败')
    def test_insert_011(self):
        '''
        写入表中bigint类型字段，数据为正数溢出值,queryfail
        '''
        res = tableOpt.insertTb(self.tbBigint, ['f1'], [4611686018427387903])
        self.assertTrue(res != 0, msg='self.tb_011写入失败')
        lastObj = tableOpt.selectLast(self.tbBigint)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int64(1)
            self.assertNotEqual(f1, 4611686018427387903, msg='验证f1值失败')
    def test_insert_012(self):
        '''
        写入表中bigint类型字段，数据为字母，汉字，特殊字符,queryfail
        '''
        res1 = tableOpt.insertTb(self.tbBigint, ['f1'], ['ff'])
        self.assertTrue(res1 != 0, msg='insert_006汉字写入整型，写入失败')
        res2 = tableOpt.insertTb(self.tbBigint, ['f1'], ['顺实'])
        self.assertTrue(res2 != 0, msg='insert_006字符串写入整型，写入失败')
        res3 = tableOpt.insertTb(self.tbBigint, ['f1'], ['*99'])
        tableOpt.insertTb(None,[],[],'insert into '+self.tbBigint+'(f1) values (*99)')
        self.assertTrue(res3 != 0, msg='insert_006特殊字符写入整型，写入失败')

class Test_insert_float(unittest.TestCase):
    tbfloat = 't_float'
    db = 'test_insert_float' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres =tableOpt.createTb(cls.tbfloat,{'f1':data_type['float']})
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb = tableOpt.dropTb(cls.tbfloat)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_insert_013(self):
        '''
        float类型，小数位：小于6位，补0,queryok
        '''
        res = tableOpt.insertTb(self.tbfloat, ['f1'], [1.12345])
        self.assertEqual(res, 0, msg='tb_013写入失败')
        lastObj = tableOpt.selectLast(self.tbfloat)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_float(1)
            self.assertEqual(format(f1, '.6f'),  format(1.12345, '.6f'), msg='验证f1值失败')
    def test_insert_014(self):
        '''
        float类型，小数位：等于6位，query ok
        '''
        res = tableOpt.insertTb(self.tbfloat, ['f1'], [1.123456])
        self.assertEqual(res, 0, msg='tb_014写入失败')
        lastObj = tableOpt.selectLast(self.tbfloat)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_float(1)

            self.assertEqual(format(f1, '.6f'), format(1.123456, '.6f'), msg='验证f1值失败')
    def test_insert_015(self):
        '''
        float类型，小数位：大于6位，且第7位大于等于5，向前进位，输出的小数位数仍是6位,ok
        '''
        res = tableOpt.insertTb(self.tbfloat, ['f1'], [1.1234567])
        self.assertEqual(res, 0, msg='self.tb_015写入失败')
        lastObj = tableOpt.selectLast(self.tbfloat)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_float(1)
            self.assertEqual(format(f1, '.6f'), format(1.1234567, '.6f'), msg='验证f1值失败')
    def test_insert_016(self):
        '''
        float类型，小数位：大于6位，且第7位小于5，舍去第七位之后的位数，输出的小数位数仍是6位
        '''
        res = tableOpt.insertTb(self.tbfloat, ['f1'], [1.1234564])
        self.assertEqual(res, 0, msg='self.tb_016写入失败')
        lastObj = tableOpt.selectLast(self.tbfloat)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_float(1)
            self.assertEqual(format(f1, '.6f'), format(1.1234564, '.6f'), msg='验证f1值失败')


















