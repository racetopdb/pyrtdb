# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *
from Lib.createDB import *
import logging

def setUpModule():
    print('数据库管理集成测试 >>>>>>>>>>>>>>开始')
    res = conn.query_reader('show database')

    dbnames = []
    try:
        while res.cursor_next() == 0:
            name = res.get_string(0)
            dbnames.append(name)
        for dbname in dbnames:
            dropRes = conn.query("drop db '" + dbname + "';")
            print(f'setupModule删除结果是：{dbname}--{dropRes}')
    except Exception as e:
        print('Module异常：',e)


'''
    集成测试断开连接
'''
def tearDownModule():
    print("数据库管理集成测试 >>>>>>>>>>>>>>结束,关闭连接")

# setUpModule()