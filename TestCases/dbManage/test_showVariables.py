# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *



class ShowVariables(unittest.TestCase):

    def test_show(self):
        '''
        show variables
        '''
        res = conn.query_reader('show variables')
        rc = res.get_row_count()
        self.assertEqual(int(rc),19,msg='返回记录数正确')
        i = 0
        while 0== res.cursor_next():
            name = res.get_string(0)
            # print(name)
            value = res.get_string(1)
            # print(value)
            readonly = res.get_bool(2)
            if 0==i:
                self.assertEqual(name, 'datadir')
                self.assertEqual(value, "E:\\rtdb_install\\rtdb\\v1\\win64\\RTDB\\rtdb\\DATABASES\\")
                self.assertFalse(readonly)
            if i==1:
                self.assertEqual(name, 'logpath')
                self.assertEqual(value, "E:\\rtdb_install\\rtdb\\v1\\win64\\RTDB\\rtdb\\LOG")
                self.assertFalse(readonly)
            if i==2:
                self.assertEqual(name, 'loglevel')
                self.assertEqual(value, "INFO")
                self.assertFalse(readonly)
            if i==3:
                self.assertEqual(name, 'init')
                self.assertEqual(value, "OK")
                self.assertTrue(readonly)
            if 4 == i:
                self.assertEqual(name,'config')
                self.assertEqual(value, 'E:\\rtdb_install\\rtdb\\v1\\win64\\RTDB\\rtdb\\ETC\\TSVR.CFG')
                self.assertTrue(readonly)
            if i==5:
                self.assertEqual(name, 'disk')
                self.assertEqual(value, "2")
                self.assertTrue(readonly)
            if i==6:
                self.assertEqual(name, 'mode')
                self.assertEqual(value, "normal")
                self.assertTrue(readonly)
            if i==7:
                self.assertEqual(name, 'svrexe')
                self.assertEqual(value, "E:\\rtdb_install\\rtdb\\v1\\win64\\bin\\rtdb_svr.exe")
                self.assertTrue(readonly)
            if i==8:
                self.assertEqual(name, 'svrstarttime')
                # self.assertEqual(value, "2022-06-06 12:58:48.048")
                self.assertTrue(readonly)
            if i==9:
                self.assertEqual(name, 'svrsize')
                # self.assertEqual(value, "2118656")
                self.assertTrue(readonly)
            if i==10:
                self.assertEqual(name, 'svrmd5')
                # self.assertEqual(value, "AEC8DB3BE22A2D03C1DDD63538110AB6")
                self.assertTrue(readonly)
            if i==11:
                self.assertEqual(name, 'svrpid')
                # self.assertEqual(value, "")
                self.assertTrue(readonly)
            if i==12:
                self.assertEqual(name, 'svrppid')
                # self.assertEqual(value, "")
                self.assertTrue(readonly)
            if i==13:
                self.assertEqual(name, 'svrver')
                # self.assertEqual(value, "[cli,core,dpr,dprs,face,sec,svr=202205311908]")
                self.assertTrue(readonly)
            if i==14:
                self.assertEqual(name, 'dbver')
                # self.assertEqual(value, "202205191908")
                self.assertTrue(readonly)
            if i==15:
                self.assertEqual(name, 'clidll')
                print('clidll的值：')
                print(value)
                self.assertEqual(value, "E:\\rtdbPython\\plugin\\python\\pyrtdb\\dll\\windows\\x64\\tsdb.dll")
                self.assertTrue(readonly)
            if i==16:
                self.assertEqual(name, 'cliver')
                self.assertEqual(value, "[cli,core,dpr,dprs,face,sec,svr=202205311908]")
                self.assertTrue(readonly)
            if i == 17:
                self.assertEqual(name, 'clisize')
                # self.assertEqual(value, "925184")
                self.assertTrue(readonly)
            if i == 18:
                self.assertEqual(name, 'climd5')
                # self.assertEqual(value, "356EF949B6DCD0B910BEA95DDCBAD22D")
                self.assertTrue(readonly)
            # print(res.cursor_next())
            i += 1
