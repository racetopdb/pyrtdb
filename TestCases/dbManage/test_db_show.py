# -*- coding: utf-8 -*-
from TestCases.dbManage.setupModule import *
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *
import datetime
logger = logging.getLogger('main.Test_db2')

class Test_db_show(unittest.TestCase):
    sleep(.1)
    db = 'test_db_show'+ datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertTrue(res == 0, msg='初始化创建库失败')

    @classmethod
    def tearDownClass(cls) -> None:
        '''
        teardown，删除初始化创建的数据库
        '''
        drop = createDB.dropDB(cls.db)
        cls().assertEqual(drop, 0, msg='删除初始化创建的数据库')

    def test_db_001(self):
        '''
            使用show databases
        '''
        show = conn.query_reader("show databases")
        while show.cursor_next() == 0:
            name = show.get_string(0)
            self.assertEqual(name,self.db,msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(7)
            if platform['system'] == 'Linux':
                self.assertEqual(path, sys_cfg['linux_data_dir']+self.db, msg='数据库存储路径不符')
            else:
                self.assertEqual(path, sys_cfg['win_data_dir'] + self.db, msg='数据库存储路径不符')
            dbver = show.get_string(9)
            self.assertEqual(dbver, sys_cfg['dbver'], msg='数据库版本不符')
    def test_db_002(self):
        '''
            使用show database
        '''
        show = conn.query_reader("show database")

        while show.cursor_next() == 0:
            name = show.get_string(0)
            self.assertEqual(name, self.db, msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(7)

            if platform['system'] == 'Linux':
                self.assertEqual(path, sys_cfg['linux_data_dir']+self.db, msg='数据库存储路径不符')
            else:
                self.assertEqual(path, sys_cfg['win_data_dir'] + self.db, msg='数据库存储路径不符')
            dbver = show.get_string(9)
            self.assertEqual(dbver, sys_cfg['dbver'], msg='数据库版本不符')
    def test_db_003(self):
        '''
            使用show db
        '''
        show = conn.query_reader("show db")

        while show.cursor_next() == 0:
            name = show.get_string(0)
            self.assertEqual(name, self.db, msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(7)
            if platform['system'] == 'Linux':
                self.assertEqual(path, sys_cfg['linux_data_dir']+self.db, msg='数据库存储路径不符')
            else:
                self.assertEqual(path, sys_cfg['win_data_dir'] + self.db, msg='数据库存储路径不符')
            dbver = show.get_string(9)
            self.assertEqual(dbver, sys_cfg['dbver'], msg='数据库版本不符')
    def test_db_004(self):
        '''
        使用show database,
        '''
        show = conn.query_reader("show database,")

        while show.cursor_next() == 0:
            name = show.get_string(0)
            self.assertEqual(name, self.db, msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(7)
            if platform['system'] == 'Linux':
                self.assertEqual(path, sys_cfg['linux_data_dir'] + self.db, msg='数据库存储路径不符')
            else:
                self.assertEqual(path, sys_cfg['win_data_dir'] + self.db, msg='数据库存储路径不符')
            dbver = show.get_string(9)
            self.assertEqual(dbver, sys_cfg['dbver'], msg='数据库版本不符')

class Test_db_use(unittest.TestCase):
    sleep(.1)
    db ='test_db_use'+  datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        '''
        初始化时，创建一个数据库，供测试用例进行use
        '''
        res = createDB.createSql(cls.db)
        cls().assertTrue(res == 0, msg='初始化创建库失败')
    @classmethod
    def tearDownClass(cls) -> None:
        '''
        teardown，删除初始化创建的数据库
        '''
        drop = createDB.dropDB(cls.db)
        cls().assertEqual(drop, 0, msg='删除初始化创建的数据库')
    def test_db_006(self):
        '''
        use test_db
        use test_db1,切换不同的数据库
        '''
        res = createDB.createSql('test_db006')
        self.assertEqual(res, 0, msg='创建数据库')

        use1 = conn.query('use '+self.db+';')
        self.assertTrue(use1 == 0, msg='use1 error')
        use2 = conn.query('use test_db006;')
        self.assertTrue(use2 == 0, msg='use2 error')

        dropDb = createDB.dropDB('test_db006')
        self.assertEqual(dropDb, 0, msg='删除创建的数据库')

    def test_db_008(self):
        '''
            使用select db 选择数据库
        '''
        sel = conn.query('select test_db;')
        self.assertTrue(sel!=0,msg='select test_db ERROR')
    def test_db_007(self):
        '''
        use 一个不存在的库，返回非0，验证通过
        '''
        use3 = conn.query('use test_99999')
        self.assertNotEqual(use3,0,msg='use一个不存在的库')





