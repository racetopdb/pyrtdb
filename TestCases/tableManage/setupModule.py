# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import logging

def setUpModule():
    print('表管理模块集成测试 >>>>>>>>>>>>>>开始')
    res = conn.query_reader('show database')
    dbnames = []
    # row = res.get_row_count()
    # print(f'获取行数：{row}')
    # conn.print_stdout()
    # print(f'获取的列表结果：{res}')
    # print(f'cursor_next的结果是：{res.cursor_next()}')
    try:
        print('进入try')
        while res.cursor_next() == 0:
            print('进入while')
            name = res.get_string(0)
            dbnames.append(name)
        for dbname in dbnames:
            print('进入dbname循环删除')
            # createDB.dropDB(dbname)
            dropRes = conn.query("drop db '" + dbname + "';")
            print("drop db '" + dbname + "';")
            print(f'setupModule删除结果是：{dbname}--{dropRes}')
    except Exception as e:
        print('Module异常：',e)


'''
    集成测试断开连接
'''
def tearDownModule():
    print("表管理模块集成测试 >>>>>>>>>>>>>>结束,关闭连接")

