# -*- coding: utf-8 -*-
from TestCases.dbManage.setupClass import *


logger = logging.getLogger('main.Test_db2')

class Test_db_show(setupDB):

    def test_db_001(self):
        '''
            使用show databases
        '''
        print('test_db_001第一个测试用例')
        show = conn.query_reader("show databases")
        while show.cursor_next() == 0:
            name = show.get_string(0)
            print(f'数据库名称是{name}')
            self.assertEqual(name,'test_db',msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(6)
            self.assertEqual(path, sys_cfg['local_path']+'test_db', msg='数据库存储路径不符')
            dbver = show.get_string(8)
            self.assertEqual(dbver, '202205191908', msg='数据库版本不符')
    def test_db_002(self):
        '''
            使用show database
        '''

        show = conn.query_reader("show database")
        while show.cursor_next() == 0:
            name = show.get_string(0)
            self.assertEqual(name, 'test_db', msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(6)
            self.assertEqual(path, sys_cfg['local_path']+'test_db', msg='数据库存储路径不符')
            dbver = show.get_string(8)
            self.assertEqual(dbver, '202205191908', msg='数据库版本不符')
    def test_db_003(self):
        '''
            使用show db
        '''

        show = conn.query_reader("show db")
        while show.cursor_next() == 0:
            name = show.get_string(0)
            print(f'查询到的数据库名称是：{name}')
            print(f'期望值：test_db')
            self.assertEqual(name, 'test_db', msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(6)
            self.assertEqual(path, sys_cfg['local_path']+'test_db', msg='数据库存储路径不符')
            dbver = show.get_string(8)
            self.assertEqual(dbver, '202205191908', msg='数据库版本不符')
    def test_db_004(self):
        '''
           用例ID:db_004 使用show database,
        '''
        show = conn.query_reader("show database,")
        while show.cursor_next() == 0:
            name = show.get_string(0)
            self.assertEqual(name, 'test_db', msg='数据库名称不符')
            tableCount = show.get_int(5)
            self.assertEqual(tableCount, 0, msg='表数量不符')
            path = show.get_string(6)
            self.assertEqual(path, sys_cfg['local_path']+'test_db', msg='数据库存储路径不符')
            dbver = show.get_string(8)
            self.assertEqual(dbver, '202205191908', msg='数据库版本不符')

class Test_db_use(setupDB):
    def setUp(self) -> None:
        print('use 库初始化创建一个库')
        res = conn.query('create db if not exist test_db1;')
        self.assertEqual(res,0,msg='初始化创建数据库失败')
    def tearDown(self) -> None:
        print('use db清除，删除掉初始化创建的库')
        res = conn.query('drop db test_db1;')
        self.assertEqual(res,0,msg='清除创建的数据库失败')
    def test_db_006(self):
        '''
            use test_db
            use test_db1,切换不同的数据库
        '''
        use1 = conn.query('use test_db;')
        self.assertTrue(use1 == 0, msg='use1 error')
        use2 = conn.query('use test_db1;')
        self.assertTrue(use2 == 0, msg='use2 error')

    def test_db_008(self):
        '''
            使用select db 选择数据库
        '''
        sel = conn.query('select test_db;')
        print(f'select 来当use使用：{sel}')
        self.assertTrue(sel!=0,msg='select test_db ERROR')

class Test_db_use2(setupDB):

    def test_db_007(self):
        '''
        use 一个不存在的库，返回非0，验证通过
        '''
        use3 = conn.query('use test_99999')
        print(f'use3的结果返回是：{use3}')
        print(f'期望值是：！0')
        self.assertNotEqual(use3,0,msg='use一个不存在的库')





