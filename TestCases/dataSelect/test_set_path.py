# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *
from Lib.createDB import *
import logging
import datetime

# @unittest.skip('执行大批量时，跳过此用例')
class Test_set_path(unittest.TestCase):
    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_select_004(self):
        '''
        set datadir修改数据库存储目录，非系统盘根目录c:\RTDB\TEST_DB,query ok
        '''
        path = 'c:\RTDB\TEST_DB'
        sql = "set datadir='"+path+"'"

        res = createDB.createSql(None,sql)
        self.assertEqual(res , 0 ,msg='004设置存储目录失败')
        show = createDB.showVar()
        for k,val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'],path+'\\', msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
        db = 'testdb' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        cRes = createDB.createSql(db)
        self.assertEqual(cRes, 0, msg='004创建数据库失败')
        check = createDB.checkRes()
        self.assertEqual(check['path'], path+'\\'+db, msg='004验证数据库路径失败')
        #还原路径为系统默认路径
        sql2 = "set datadir=@'"+sys_cfg['win_data_dir']+"'"

        res2 = createDB.createSql(None,sql2)
        self.assertEqual(res2 , 0 ,msg='004还原系统默认数据库路径失败')
    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_select_005(self):
        '''
        setdatadir修改数据库存储目录至系统盘c:\Windows\test_0330,query fail
        '''
        path = 'c:\\Windows\\test_0711'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='005设置存储目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'], sys_cfg['win_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_select_006(self):
        '''
        set  datadir修改数据库存储目录，系统盘c:\Program Files\test_0330 , query fail
        '''
        path = 'c:\\Program Files\\test_0712'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='006设置存储目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'], sys_cfg['win_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_select_007(self):
        '''
        set  datadir修改数据库存储目录，系统盘下一级目录c:\TEST_DB,query fail
        '''
        path = 'c:\TEST_DB'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='007设置存储目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'], sys_cfg['win_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_select_008(self):
        '''
        Linux上set datadir 路径存储到系统盘 / ,query fail
        '''
        path = '/'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='008设置存储目录失败')
        show = createDB.showVar()

        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'], sys_cfg['linux_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_select_009(self):
        '''
        Linux上set datadir 路径存储到非系统盘 , query ok
        '''
        path = '/data/TEST_DB/'
        sql = "set datadir='" + path + "'"
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0, msg='设置存储目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'], path, msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
        db = 'testdb009' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        cRes = createDB.createSql(db)
        self.assertEqual(cRes, 0, msg='创建数据库失败')
        check = createDB.checkRes()
        self.assertEqual(check['path'], path  + db, msg='验证数据库路径失败')
        # 还原路径为系统默认路径
        sql2 = "set datadir=@'" + sys_cfg['linux_data_dir'] + "'"
        res2 = createDB.createSql(None, sql2)
        self.assertEqual(res2, 0, msg='还原系统默认数据库路径失败')

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def tset_select_010(self):
        '''
        Linux上set datadir 路径存储到系统盘下级目录/TEST , query fail
        '''
        path = '/TEST'
        sql = "set datadir='" + path + "'"
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='设置存储目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'], sys_cfg['linux_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_select_012(self):
        '''
        set logpath 修改日志路径到系统根目录c:\,query failed
        2、执行set logpath='c:\'
        3、show variables查看修改结果
        '''
        path = 'c:\\'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='设置存储目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                self.assertEqual(val['value'], sys_cfg['win_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_select_013(self):
        '''
         set logpath 修改日志路径到非系统根目录,query ok
        '''
        path = 'c:\RTDB\TEST_DB'
        sql = "set logpath='" + path + "'"
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0, msg='设置日志目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 1:
                self.assertEqual(val['name'], 'logpath', msg='验证logpath的名称')
                self.assertEqual(val['value'], path, msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')
        # 还原路径为系统默认路径
        sql2 = "set logpath=@'" + sys_cfg['win_log_path'] + "'"
        res2 = createDB.createSql(None, sql2)
        self.assertEqual(res2, 0, msg='还原系统默认数据库路径失败')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_select_014(self):
        '''
        setlogpath修改日志路径到系统盘目录，c:\Windows\test_0712,query fail
        '''
        path = 'c:\\Windows\\test_0712'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='设置日志目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 1:
                self.assertEqual(val['name'], 'logpath', msg='验证logpath的名称')
                self.assertEqual(val['value'],sys_cfg['win_log_path'], msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')

    @unittest.skipIf(platform['system'] == 'Linux', 'win平台不执行此用例')
    def test_select_015(self):
        '''
        set logpath修改日志路径到系统盘目录，c:\Program Files\test_015,query fail
        '''
        path = 'c:\\Program Files\\test_0712'
        sql = "set datadir='" + path + "'"
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='设置日志目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 1:
                self.assertEqual(val['name'], 'logpath', msg='验证logpath的名称')
                self.assertEqual(val['value'], sys_cfg['win_log_path'], msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_select_016(self):
        '''
        Linux上set logpath 路径存储到系统根目录,query fail
        '''
        path = '/'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='设置日志目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证logpath的名称')
                self.assertEqual(val['value'], sys_cfg['linux_data_dir'], msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_select_017(self):
        '''
        Linux上set logpath 路径存储到系统盘下级目录/TEST ,query fail
        '''
        path = '/TEST'
        sql = "set datadir=" + path + ""
        res = createDB.createSql(None, sql)
        self.assertTrue(res != 0, msg='设置日志目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证logpath的名称')
                self.assertEqual(val['value'], sys_cfg['linux_data_dir'], msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_select_019(self):
        '''
        Linux上set logpath 路径存储到系统盘下级目录/TEST/TEST_log,query ok
        '''
        path = '/TEST/TEST_log'
        sql = "set logpath='" + path + "'"
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0, msg='设置日志目录失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 1:
                self.assertEqual(val['name'], 'logpath', msg='验证logpath的名称')
                self.assertEqual(val['value'], path, msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')
        # 还原路径为系统默认路径
        sql2 = "set logpath=@'" + sys_cfg['linux_log_path'] + "'"
        res2 = createDB.createSql(None, sql2)
        self.assertEqual(res2, 0, msg='还原系统默认数据库路径失败')
    def test_select_020(self):
        '''
        set loglevel修改日志等级为DEBUG,query ok
        '''
        sql = "set loglevel='DEBUG' "
        res = createDB.createSql(None,sql)
        self.assertEqual(res, 0, msg='设置日志等级失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 2:
                self.assertEqual(val['name'], 'loglevel', msg='验证loglevel的名称')
                self.assertEqual(val['value'], 'DEBUG', msg='验证loglevel的值')
                self.assertFalse(val['readonly'], msg='验证loglevel的只读属性')
        # 还原路径为系统默认路径
        sql2 = "set loglevel=" + sys_cfg['loglevel'] + ""
        res2 = createDB.createSql(None, sql2)
        self.assertEqual(res2, 0, msg='还原系统默认数据库日志等级失败')
    def test_select_022(self):
        '''
        set config 修改配置文件路径,query fail
        '''
        sql = 'set config="c:\RTDB\TEST_DB" '
        res = createDB.createSql(None,sql)
        self.assertTrue(res !=0 , msg='设置config路径失败')
        show = createDB.showVar()
        for k, val in show.items():
            if k == 4:
                self.assertEqual(val['name'], 'config', msg='验证config的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_data_config'], msg='验证config的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_data_config'], msg='验证config的值')
                self.assertTrue(val['readonly'], msg='验证config的只读属性')
    def test_select_023(self):
        '''
        set disk 修改硬盘,query fail
        '''
        sql = 'set disk=64'
        res = createDB.createSql(None,sql)
        self.assertTrue(res != 0, msg='修改disk值失败')
    def test_select_024(self):
        '''
        set mode  修改服务器的启动状态, query fail
        '''
        sql  = "set mode='CRASH RECOVER!'"
        res = createDB.createSql(None,sql)
        self.assertTrue(res != 0, msg='修改mode值失败')