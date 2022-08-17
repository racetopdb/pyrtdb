# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *
from Lib.createDB import *
import logging
import datetime
from Comm.data import *


@unittest.skip('执行大批量时，跳过此用例')
class Test_show_variables(unittest.TestCase):

    def test_select_001(self):
        '''
        show variables
        '''
        res = createDB.showVar()
        self.assertEqual(len(res) , 25 ,msg='验证show variables返回的条数')
        if platform['system'] == 'Linux':
            data_dict = read_excel(r"" + config['testDataPath'] + "\\variables_linux.xlsx", header=None)
        else:
            data_dict = read_excel(r"" + config['testDataPath'] + "\\variables_win.xlsx", header=None)
        for j, row in enumerate(data_dict):
            self.assertEqual(res[j]['name'], row[0], msg='验证name的值')
            if row[1] == 'disk':
                print(type(res[j]['value']))
                print(type(str(row[1])))
                self.assertTrue(res[j]['value'] == str(row[1]), msg='验证value的值')
            print(res[j]['name'])
            self.assertEqual(res[j]['value'], row[1], msg='验证value的值')

            # self.assertEqual(res[j]['readonly'], row[2], msg='验证readonly的值')


        # for k ,val in res.items():
        #
        #
        #     if k ==0:
        #         self.assertEqual(val['name'] ,'datadir',msg='验证datadir的名称')
        #         if platform['system'] == 'Linux':
        #             self.assertEqual(val['value'], sys_cfg['linux_data_dir'],msg='验证datadir的值')
        #         else:
        #             self.assertEqual(val['value'], sys_cfg['win_data_dir'],msg='验证datadir的值')
        #         self.assertFalse(val['readonly'],msg='验证datadir的只读属性')
        #     if k == 1:
        #         self.assertEqual(val['name'], 'logpath',msg='验证logpath的名称')
        #         if platform['system'] == 'Linux':
        #             self.assertEqual(val['value'], sys_cfg['linux_log_path'], msg='验证log的值')
        #         else:
        #             self.assertEqual(val['value'], sys_cfg['win_log_path'],msg='验证logpath的值')
        #         self.assertFalse(val['readonly'],msg='验证logpath的只读属性')
        #     if k == 2:
        #         self.assertEqual(val['name'], 'loglevel',msg='验证loglevel的名称')
        #         self.assertEqual(val['value'], sys_cfg['loglevel'],msg='验证loglevel的值')
        #         self.assertFalse(val['readonly'],msg='验证loglevel的只读属性')
        #     if k == 3:
        #         self.assertEqual(val['name'], 'init',msg='验证init的名称')
        #         self.assertEqual(val['value'], sys_cfg['server_init'],msg='验证init的值')
        #         self.assertTrue(val['readonly'],msg='验证init的只读属性')
        #     if k == 4:
        #         self.assertEqual(val['name'], 'config',msg='验证config的名称')
        #         if platform['system'] == 'Linux':
        #             self.assertEqual(val['value'], sys_cfg['linux_data_config'], msg='验证config的值')
        #         else:
        #             self.assertEqual(val['value'], sys_cfg['win_data_config'],msg='验证config的值')
        #         self.assertTrue(val['readonly'],msg='验证config的只读属性')
        #     if k == 5:
        #         self.assertEqual(val['name'], 'disk',msg='验证disk的名称')
        #         # self.assertEqual(val['value'], sys_cfg['server_disk'],msg='验证disk的值')
        #         self.assertTrue(val['readonly'],msg='验证datadir的只读属性')
        #     if k == 6:
        #         self.assertEqual(val['name'], 'ip',msg='验证ip的名称')
        #         self.assertTrue(val['readonly'],msg='验证mode的只读属性')
        #     if k == 7:
        #         self.assertEqual(val['name'], 'influxdb_protocol',msg='验证mode的名称')
        #         self.assertEqual(val['value'], 'true',msg='验证mode的值')
        #         self.assertTrue(val['readonly'],msg='验证mode的只读属性')
        #     if k == 8:
        #         self.assertEqual(val['name'], 'itink_forward_protocol', msg='验证mode的名称')
        #         self.assertEqual(val['value'], 'true', msg='验证mode的值')
        #         self.assertTrue(val['readonly'], msg='验证mode的只读属性')
        #     if k == 9:
        #         self.assertEqual(val['name'], 'flush_type', msg='验证mode的名称')
        #         self.assertEqual(val['value'], 'FLUSH(TABLE,PK_FIELD)', msg='验证mode的值')
        #         self.assertTrue(val['readonly'], msg='验证mode的只读属性')
        #     if k == 10:
        #         self.assertEqual(val['name'], 'intergrity_type', msg='验证intergrity_type的名称')
        #         self.assertEqual(val['value'], 'ENABLED(WRITE,READ)', msg='验证intergrity_type的值')
        #         self.assertTrue(val['readonly'], msg='验证mode的只读属性')
        #     if k == 11:
        #         self.assertEqual(val['name'], 'mode', msg='验证mode的名称')
        #         self.assertEqual(val['value'], sys_cfg['server_mode'], msg='验证mode的值')
        #         self.assertTrue(val['readonly'], msg='验证mode的只读属性')
        #     if k == 12:
        #         self.assertEqual(val['name'], 'svrexe',msg='验证svrexe的名称')
        #         if platform['system'] == 'Linux':
        #             self.assertEqual(val['value'], sys_cfg['linux_svrexe'], msg='验证svrexe的值')
        #         else:
        #             self.assertEqual(val['value'], sys_cfg['win_svrexe'],msg='验证svrexe的值')
        #         self.assertTrue(val['readonly'],msg='验证svrexe的只读属性')
        #     if k == 13:
        #         self.assertEqual(val['name'], 'svrstarttime',msg='验证svrstarttime的名称')
        #         # self.assertEqual(value, "2022-06-06 12:58:48.048")
        #         self.assertTrue(val['readonly'],msg='验证svrstarttime的只读属性')
        #     if k == 14:
        #         self.assertEqual(val['name'], 'svrsize',msg='验证svrsize的名称')
        #         # self.assertEqual(value, "2118656")
        #         self.assertTrue(val['readonly'],msg='验证svrsize的只读属性')
        #     if k == 15:
        #         self.assertEqual(val['name'], 'svrmd5',msg='验证svrmd5的名称')
        #         # self.assertEqual(value, "AEC8DB3BE22A2D03C1DDD63538110AB6")
        #         self.assertTrue(val['readonly'],msg='验证svrmd5的只读属性')
        #     if k == 16:
        #         self.assertEqual(val['name'], 'svrpid',msg='验证svrpid的名称')
        #         # self.assertEqual(value, "")
        #         self.assertTrue(val['readonly'],msg='验证svrpid的只读属性')
        #     if k == 17:
        #         self.assertEqual(val['name'], 'svrppid',msg='验证svrppid的名称')
        #         # self.assertEqual(value, "")
        #         self.assertTrue(val['readonly'],msg='验证svrppid的只读属性')
        #     if k == 18:
        #         self.assertEqual(val['name'], 'svrver',msg='验证svrver的名称')
        #          # self.assertEqual(value, "[cli,core,dpr,dprs,face,sec,svr=202205311908]")
        #         self.assertTrue(val['readonly'],msg='验证svrver的只读属性')
        #     if k == 19:
        #         self.assertEqual(val['name'], 'dbver',msg='验证dbver的名称')
        #          # self.assertEqual(value, "202205191908")
        #         self.assertTrue(val['readonly'],msg='验证dbver的只读属性')
        #     if k == 20:
        #         self.assertEqual(val['name'], 'clidll',msg='验证clidll的名称')
        #
        #         # if platform['system'] == 'Linux':
        #         #
        #         #     self.assertEqual(val['value'], sys_cfg['linux_clidll'], msg='linux验证clidll的值')
        #         # else:
        #         #     self.assertEqual(val['value'], sys_cfg['win_clidll'],msg='win验证clidll的值')
        #         self.assertTrue(val['readonly'],msg='验证clidll的只读属性')
        #     if k == 21:
        #         self.assertEqual(val['name'], 'cliver',msg='验证cliver的名称')
        #         # self.assertEqual(val['value'], sys_cfg['win_cliver'],msg='验证cliver的值')
        #         self.assertTrue(val['readonly'],msg='验证cliver的只读属性')
        #     if k == 22:
        #         self.assertEqual(val['name'], 'clisize',msg='验证clisize的名称')
        #         # self.assertEqual(value, "925184")
        #         self.assertTrue(val['readonly'],msg='验证clisize的只读属性')
        #     if k == 23:
        #         self.assertEqual(val['name'], 'climd5',msg='验证climd5的名称')
        #         # self.assertEqual(value, "356EF949B6DCD0B910BEA95DDCBAD22D")
        #         self.assertTrue(val['readonly'],msg='验证climd5的只读属性')

    def test_select_002(self):
        '''
        show variable
        '''
        res = createDB.showVar('show variable')
        self.assertEqual(len(res), 24, msg='验证show variable返回的条数')
        for k, val in res.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_data_dir'], msg='验证datadir的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
            if k == 1:
                self.assertEqual(val['name'], 'logpath', msg='验证logpath的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_log_path'], msg='验证log的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_log_path'], msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')
            if k == 2:
                self.assertEqual(val['name'], 'loglevel', msg='验证loglevel的名称')
                self.assertEqual(val['value'], sys_cfg['loglevel'], msg='验证loglevel的值')
                self.assertFalse(val['readonly'], msg='验证loglevel的只读属性')
            if k == 3:
                self.assertEqual(val['name'], 'init', msg='验证init的名称')
                self.assertEqual(val['value'], sys_cfg['server_init'], msg='验证init的值')
                self.assertTrue(val['readonly'], msg='验证init的只读属性')
            if k == 4:
                self.assertEqual(val['name'], 'config', msg='验证config的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_data_config'], msg='验证config的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_data_config'], msg='验证config的值')
                self.assertTrue(val['readonly'], msg='验证config的只读属性')
            if k == 5:
                self.assertEqual(val['name'], 'disk', msg='验证disk的名称')
                # self.assertEqual(val['value'], sys_cfg['server_disk'],msg='验证disk的值')
                self.assertTrue(val['readonly'], msg='验证datadir的只读属性')
            if k == 6:
                self.assertEqual(val['name'], 'ip', msg='验证ip的名称')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 7:
                self.assertEqual(val['name'], 'influxdb_protocol', msg='验证mode的名称')
                self.assertEqual(val['value'], 'true', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 8:
                self.assertEqual(val['name'], 'itink_forward_protocol', msg='验证mode的名称')
                self.assertEqual(val['value'], 'true', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 9:
                self.assertEqual(val['name'], 'flush_type', msg='验证mode的名称')
                self.assertEqual(val['value'], 'FLUSH(TABLE,PK_FIELD)', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 10:
                self.assertEqual(val['name'], 'intergrity_type', msg='验证intergrity_type的名称')
                self.assertEqual(val['value'], 'ENABLED(WRITE,READ)', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 11:
                self.assertEqual(val['name'], 'mode', msg='验证mode的名称')
                self.assertEqual(val['value'], sys_cfg['server_mode'], msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 12:
                self.assertEqual(val['name'], 'svrexe', msg='验证svrexe的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_svrexe'], msg='验证svrexe的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_svrexe'], msg='验证svrexe的值')
                self.assertTrue(val['readonly'], msg='验证svrexe的只读属性')
            if k == 13:
                self.assertEqual(val['name'], 'svrstarttime', msg='验证svrstarttime的名称')
                # self.assertEqual(value, "2022-06-06 12:58:48.048")
                self.assertTrue(val['readonly'], msg='验证svrstarttime的只读属性')
            if k == 14:
                self.assertEqual(val['name'], 'svrsize', msg='验证svrsize的名称')
                # self.assertEqual(value, "2118656")
                self.assertTrue(val['readonly'], msg='验证svrsize的只读属性')
            if k == 15:
                self.assertEqual(val['name'], 'svrmd5', msg='验证svrmd5的名称')
                # self.assertEqual(value, "AEC8DB3BE22A2D03C1DDD63538110AB6")
                self.assertTrue(val['readonly'], msg='验证svrmd5的只读属性')
            if k == 16:
                self.assertEqual(val['name'], 'svrpid', msg='验证svrpid的名称')
                # self.assertEqual(value, "")
                self.assertTrue(val['readonly'], msg='验证svrpid的只读属性')
            if k == 17:
                self.assertEqual(val['name'], 'svrppid', msg='验证svrppid的名称')
                # self.assertEqual(value, "")
                self.assertTrue(val['readonly'], msg='验证svrppid的只读属性')
            if k == 18:
                self.assertEqual(val['name'], 'svrver', msg='验证svrver的名称')
                # self.assertEqual(value, "[cli,core,dpr,dprs,face,sec,svr=202205311908]")
                self.assertTrue(val['readonly'], msg='验证svrver的只读属性')
            if k == 19:
                self.assertEqual(val['name'], 'dbver', msg='验证dbver的名称')
                # self.assertEqual(value, "202205191908")
                self.assertTrue(val['readonly'], msg='验证dbver的只读属性')
            if k == 20:
                self.assertEqual(val['name'], 'clidll', msg='验证clidll的名称')
                # if platform['system'] == 'Linux':
                #     self.assertEqual(val['value'], sys_cfg['linux_clidll'], msg='验证clidll的值')
                # else:
                #     self.assertEqual(val['value'], sys_cfg['win_clidll'], msg='验证clidll的值')
                self.assertTrue(val['readonly'], msg='验证clidll的只读属性')
            if k == 21:
                self.assertEqual(val['name'], 'cliver', msg='验证cliver的名称')
                # self.assertEqual(val['value'], sys_cfg['win_cliver'],msg='验证cliver的值')
                self.assertTrue(val['readonly'], msg='验证cliver的只读属性')
            if k == 22:
                self.assertEqual(val['name'], 'clisize', msg='验证clisize的名称')
                # self.assertEqual(value, "925184")
                self.assertTrue(val['readonly'], msg='验证clisize的只读属性')
            if k == 23:
                self.assertEqual(val['name'], 'climd5', msg='验证climd5的名称')
                # self.assertEqual(value, "356EF949B6DCD0B910BEA95DDCBAD22D")
                self.assertTrue(val['readonly'], msg='验证climd5的只读属性')

    def test_select_003(self):
        '''
        select *
        '''
        res = createDB.showVar('select *')
        self.assertEqual(len(res), 24, msg='验证select *返回的条数')
        for k, val in res.items():
            if k == 0:
                self.assertEqual(val['name'], 'datadir', msg='验证datadir的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_data_dir'], msg='验证datadir的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_data_dir'], msg='验证datadir的值')
                self.assertFalse(val['readonly'], msg='验证datadir的只读属性')
            if k == 1:
                self.assertEqual(val['name'], 'logpath', msg='验证logpath的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_log_path'], msg='验证log的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_log_path'], msg='验证logpath的值')
                self.assertFalse(val['readonly'], msg='验证logpath的只读属性')
            if k == 2:
                self.assertEqual(val['name'], 'loglevel', msg='验证loglevel的名称')
                self.assertEqual(val['value'], sys_cfg['loglevel'], msg='验证loglevel的值')
                self.assertFalse(val['readonly'], msg='验证loglevel的只读属性')
            if k == 3:
                self.assertEqual(val['name'], 'init', msg='验证init的名称')
                self.assertEqual(val['value'], sys_cfg['server_init'], msg='验证init的值')
                self.assertTrue(val['readonly'], msg='验证init的只读属性')
            if k == 4:
                self.assertEqual(val['name'], 'config', msg='验证config的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_data_config'], msg='验证config的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_data_config'], msg='验证config的值')
                self.assertTrue(val['readonly'], msg='验证config的只读属性')
            if k == 5:
                self.assertEqual(val['name'], 'disk', msg='验证disk的名称')
                # self.assertEqual(val['value'], sys_cfg['server_disk'],msg='验证disk的值')
                self.assertTrue(val['readonly'], msg='验证datadir的只读属性')
            if k == 6:
                self.assertEqual(val['name'], 'ip', msg='验证ip的名称')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 7:
                self.assertEqual(val['name'], 'influxdb_protocol', msg='验证mode的名称')
                self.assertEqual(val['value'], 'true', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 8:
                self.assertEqual(val['name'], 'itink_forward_protocol', msg='验证mode的名称')
                self.assertEqual(val['value'], 'true', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 9:
                self.assertEqual(val['name'], 'flush_type', msg='验证mode的名称')
                self.assertEqual(val['value'], 'FLUSH(TABLE,PK_FIELD)', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 10:
                self.assertEqual(val['name'], 'intergrity_type', msg='验证mode的名称')
                self.assertEqual(val['value'], 'ENABLED(WRITE,READ)', msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 11:
                self.assertEqual(val['name'], 'mode', msg='验证mode的名称')
                self.assertEqual(val['value'], sys_cfg['server_mode'], msg='验证mode的值')
                self.assertTrue(val['readonly'], msg='验证mode的只读属性')
            if k == 12:
                self.assertEqual(val['name'], 'svrexe', msg='验证svrexe的名称')
                if platform['system'] == 'Linux':
                    self.assertEqual(val['value'], sys_cfg['linux_svrexe'], msg='验证svrexe的值')
                else:
                    self.assertEqual(val['value'], sys_cfg['win_svrexe'], msg='验证svrexe的值')
                self.assertTrue(val['readonly'], msg='验证svrexe的只读属性')
            if k == 13:
                self.assertEqual(val['name'], 'svrstarttime', msg='验证svrstarttime的名称')
                # self.assertEqual(value, "2022-06-06 12:58:48.048")
                self.assertTrue(val['readonly'], msg='验证svrstarttime的只读属性')
            if k == 14:
                self.assertEqual(val['name'], 'svrsize', msg='验证svrsize的名称')
                # self.assertEqual(value, "2118656")
                self.assertTrue(val['readonly'], msg='验证svrsize的只读属性')
            if k == 15:
                self.assertEqual(val['name'], 'svrmd5', msg='验证svrmd5的名称')
                # self.assertEqual(value, "AEC8DB3BE22A2D03C1DDD63538110AB6")
                self.assertTrue(val['readonly'], msg='验证svrmd5的只读属性')
            if k == 16:
                self.assertEqual(val['name'], 'svrpid', msg='验证svrpid的名称')
                # self.assertEqual(value, "")
                self.assertTrue(val['readonly'], msg='验证svrpid的只读属性')
            if k == 17:
                self.assertEqual(val['name'], 'svrppid', msg='验证svrppid的名称')
                # self.assertEqual(value, "")
                self.assertTrue(val['readonly'], msg='验证svrppid的只读属性')
            if k == 18:
                self.assertEqual(val['name'], 'svrver', msg='验证svrver的名称')
                # self.assertEqual(value, "[cli,core,dpr,dprs,face,sec,svr=202205311908]")
                self.assertTrue(val['readonly'], msg='验证svrver的只读属性')
            if k == 19:
                self.assertEqual(val['name'], 'dbver', msg='验证dbver的名称')
                # self.assertEqual(value, "202205191908")
                self.assertTrue(val['readonly'], msg='验证dbver的只读属性')
            if k == 20:
                self.assertEqual(val['name'], 'clidll', msg='验证clidll的名称')
                # if platform['system'] == 'Linux':
                #     self.assertEqual(val['value'], sys_cfg['linux_clidll'], msg='验证clidll的值')
                # else:
                #     self.assertEqual(val['value'], sys_cfg['win_clidll'], msg='验证clidll的值')
                self.assertTrue(val['readonly'], msg='验证clidll的只读属性')
            if k == 21:
                self.assertEqual(val['name'], 'cliver', msg='验证cliver的名称')
                # self.assertEqual(val['value'], sys_cfg['win_cliver'],msg='验证cliver的值')
                self.assertTrue(val['readonly'], msg='验证cliver的只读属性')
            if k == 22:
                self.assertEqual(val['name'], 'clisize', msg='验证clisize的名称')
                # self.assertEqual(value, "925184")
                self.assertTrue(val['readonly'], msg='验证clisize的只读属性')
            if k == 23:
                self.assertEqual(val['name'], 'climd5', msg='验证climd5的名称')
                # self.assertEqual(value, "356EF949B6DCD0B910BEA95DDCBAD22D")
                self.assertTrue(val['readonly'], msg='验证climd5的只读属性')








