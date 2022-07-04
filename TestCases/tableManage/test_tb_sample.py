import random
import unittest

from Conf.config import data_type
from Lib.tableOpt import *
from Lib.createDB import *
# from TestCases.tableManage.setupClass import *
import random

db = 'testdb'+str(random.randrange(1,10000,100))

@unittest.skip('执行大批量时，跳过此用例')
class Test_tb_sample(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print('sample类初始化--创建一个数据库')

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

    def test_tb_sample1(self):
        show = conn.query_reader('show tb')
        conn.print_stdout()
        # sql = 'create table table_061(col1 ,col2,col3)'
        # res = tableOpt.createTb(None, {}, sql)
        # self.assertTrue(res != 0, msg='tb_061创建表成功')
        # row = conn.query_reader('show tb')
        # print(f'1表创建失败之后的行数是：{row}')
        # print(f'1失败后的行数是：{row.get_row_count()}')
        # self.assertEqual(row, 0, msg='没有创建成功，返回0行')
    def test_tb_sample2(self):
        pass
        # sql = 'create table table_062(col1 int )'
        # res = tableOpt.createTb(None, {}, sql)
        # self.assertTrue(res == 0, msg='tb_061创建表成功')
        # row = conn.query_reader('show tb')
        # print(f'2表创建成功之后的是：{row}')
        # print(f'2成功后的行数是：{row.get_row_count()}')
        # self.assertEqual(row, 0, msg='没有创建成功，返回0行')

