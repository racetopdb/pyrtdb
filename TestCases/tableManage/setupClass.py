# -*- coding: utf-8 -*-
from TestCases.tableManage.setupModule import *
import unittest
from Comm.pyrtdb import conn
from time import *
import datetime
from Conf.config import *
from Lib.tableOpt import *

db = 'test_db' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

class setupTb(unittest.TestCase):

        @classmethod
        def setUpClass(cls) -> None:
                print('类初始化--创建一个数据库')

                res = conn.query("create db if not exists  "+db+";")
                print(f'类创建数据库的结果：{res}')
                usql = 'use '+db+''
                ret = createDB.createSql(None, usql)
                print(f'类use库结果是：{ret}')
                # cls.assertEqual( res , 0, msg='创建数据库失败')

        @classmethod
        def tearDownClass(cls) -> None:
                print('类清除--删除在初始化时创建的数据库')

                r = conn.query_reader("drop db "+db+";")
                print(f'删除数据库的结果：{r}')

