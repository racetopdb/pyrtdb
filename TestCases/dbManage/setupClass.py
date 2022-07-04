# -*- coding: utf-8 -*-
from TestCases.dbManage.setupModule import *
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *

class setupDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        '''
        初始化时，创建一个数据库，供测试用例进行use
        '''

        res = createDB.createSql('test_db')
        print(f'初始化创建库的结果：{res}')
        # cls.assertTrue(setUpClass,res ==0 ,msg='初始化创建库失败')


    @classmethod
    def tearDownClass(cls) -> None:
        '''
        teardown，删除初始化创建的数据库
        '''
        drop = createDB.dropDB('test_db')
        print(f'初始化删除结果：{drop}')
        # cls.assertEqual(drop ,None ,msg='删除初始化创建的数据库')
