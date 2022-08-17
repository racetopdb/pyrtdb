# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
import datetime
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import logging
from Comm.convert import *




class Test_insert_time(unittest.TestCase):
    tb = 't_time'
    db = 'test_insert_time' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tres =tableOpt.createTb(cls.tb,{'f1':data_type['timestamp']})
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')


    def test_insert_017(self):
        '''
        timestamp类型，格式：月/日/年（简写）,query fail
        '''
        res = tableOpt.insertTb(self.tb,['f1'],['01/03/17'])
        self.assertTrue(res != 0 ,msg='insert_017写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_018(self):
        '''
        timestamp类型，格式：年（简写）.月.日 ,query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['17.01.03'])
        self.assertTrue(res != 0, msg='insert_018写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_019(self):
        '''
        timestamp类型，格式：日/月/年（简写）query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03/01/17'])
        self.assertTrue(res != 0, msg='insert_019写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_020(self):
        '''
        timestamp类型，格式：日.月.年（简写）query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03.01.17'])
        self.assertTrue(res != 0, msg='insert_020写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')

    def test_insert_021(self):
        '''
        timestamp类型，格式：日-月-年（简写）
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03-01-17'])
        self.assertTrue(res != 0, msg='insert_021写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_022(self):
        '''
        timestamp类型，格式：日 月 年（简写）
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03 01 17'])
        self.assertTrue(res != 0, msg='insert_022写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_023(self):
        '''
        timestamp类型，格式：日 月 ,年（简写）
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01 03, 17'])
        self.assertTrue(res != 0, msg='insert_023写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_024(self):
        '''
        timestamp类型，格式：时:分:秒
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['09:09:10'])
        self.assertTrue(res != 0, msg='insert_024写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_025(self):
        '''
        timestamp类型，格式：月 日 年 时:分:秒:毫秒AM
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01 3 2017 9:09:10:037AM'])
        self.assertTrue(res != 0, msg='insert_025写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_026(self):
        '''
        timestamp类型，格式：月-日-年（简写）
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01-03-17'])
        self.assertTrue(res != 0, msg='insert_026写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_027(self):
        '''
        timestamp类型，格式：年（简写）/月/日
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['17/01/03'])
        self.assertTrue(res != 0, msg='insert_027写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_028(self):
        '''
        timestamp类型，格式：年(简写）月日 query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['170103'])
        self.assertTrue(res == 0, msg='insert_028写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)

            self.assertEqual(f1 , 170103 ,msg='验证f1的值')
    def test_insert_029(self):
        '''
        timestamp类型，格式：日 月 年 时:分:秒:毫秒,query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03 01 2017 09:09:10:037'])
        self.assertTrue(res != 0, msg='insert_029写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)

            self.assertEqual(f1, 170103, msg='验证f1的值')
    def test_insert_030(self):
        '''
        timestamp类型，格式：时:分:秒:毫秒,query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['09:09:10:037'])
        self.assertTrue(res != 0, msg='insert_030写入失败')
    def test_insert_031(self):
        '''
        timestamp类型，格式：年-月-日 时:分:秒,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['2017-01-03 09:09:10'])
        self.assertTrue(res == 0, msg='insert_031写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)

            times = time.mktime(time.strptime('2017-01-03 09:09:10', '%Y-%m-%d %H:%M:%S'))

            self.assertEqual(f1, times * 1000, msg='验证f1值')
    def test_insert_032(self):
        '''
        timestamp类型，格式：年-月-日 时:分:秒.毫秒 ,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['2017-01-03 09:09:10.037'])
        self.assertTrue(res == 0, msg='insert_032写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)
            k = len(str(f1)) - 10
            f1Timestamp = datetime.datetime.fromtimestamp(f1 / (1 * 10 ** k))
            f1Datatime = f1Timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.assertEqual(f1Datatime, '2017-01-03 09:09:10.037', msg='验证f1值')
    def test_insert_033(self):
        '''
        timestamp类型，格式：月/日/年（简写） 时:分:秒 AM, query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01/03/17 9:09:10 AM'])
        self.assertTrue(res != 0, msg='insert_033写入失败')
    def test_insert_034(self):
        '''
        timestamp类型，格式：年-月-日,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['2017-01-03'])
        self.assertTrue(res == 0, msg='insert_034写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)
            k = len(str(f1)) - 10
            f1Timestamp = datetime.datetime.fromtimestamp(f1 / (1 * 10 ** k))
            f1Datatime = f1Timestamp.strftime("%Y-%m-%d")
            self.assertEqual(f1Datatime, '2017-01-03', msg='验证f1值')
    def test_insert_035(self):
        '''
        timestamp类型，格式：月 日 年 时:分AM, query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01 3 2017 9:09AM'])
        self.assertTrue(res != 0, msg='insert_035写入失败')
    def test_insert_036(self):
        '''
        timestamp类型，格式：月/日/年,query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01/03/2017'])
        self.assertTrue(res != 0, msg='insert_036写入失败')
    def test_insert_037(self):
        '''
        timestamp类型，格式：年.月.日, query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['2017.01.03'])
        self.assertTrue(res != 0, msg='insert_037写入失败')
    def test_insert_038(self):
        '''
        timestamp类型，格式：日/月/年, query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03/01/2017'])
        self.assertTrue(res != 0, msg='insert_038写入失败')
    def test_insert_039(self):
        '''
        timestamp类型，格式：日.月.年, query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03.01.2017'])
        self.assertTrue(res != 0, msg='insert_039写入失败')
    def test_insert_040(self):
        '''
        timestamp类型，格式：日-月-年
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03-01-2017'])
        self.assertTrue(res != 0, msg='insert_040写入失败')

    def test_insert_041(self):
        '''
        timestamp类型，格式：日 月 年
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03 01 2017'])
        self.assertTrue(res != 0, msg='insert_041写入失败')
    def test_insert_042(self):
        '''
        timestamp类型，格式：月 日，年
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01 03, 2017'])
        self.assertTrue(res != 0, msg='insert_042写入失败')
    def test_insert_043(self):
        '''
        timestamp类型，格式：月-日-年
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['01-03-2017'])
        self.assertTrue(res != 0, msg='insert_043写入失败')
    def test_insert_044(self):
        '''
        timestamp类型，格式：年/月/日, query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['2017/12/03'])
        self.assertTrue(res == 0, msg='insert_044写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)
            k = len(str(f1)) - 10
            f1Timestamp = datetime.datetime.fromtimestamp(f1 / (1 * 10 ** k))
            f1Datatime = f1Timestamp.strftime("%Y/%m/%d")
            self.assertEqual(f1Datatime, '2017/12/03', msg='验证f1值')
    def test_insert_045(self):
        '''
        timestamp类型，格式：年月日,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['20170103'])
        self.assertTrue(res == 0, msg='insert_045写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)
            k = len(str(f1)) - 10
            f1Timestamp = datetime.datetime.fromtimestamp(f1 / (1 * 10 ** k))
            f1Datatime = f1Timestamp.strftime("%Y%m%d")
            self.assertEqual(f1Datatime, '20170103', msg='验证f1值')

    def test_insert_046(self):
        '''
        timestamp类型，格式：年-月-日T时:分:秒.毫秒，queryok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['2017-01-03T09:45:10.011'])
        self.assertTrue(res == 0, msg='insert_046写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)
            k = len(str(f1)) - 10
            f1Timestamp = datetime.datetime.fromtimestamp(f1 / (1 * 10 ** k))
            f1Datatime = f1Timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.assertEqual(f1Datatime, '2017-01-03 09:45:10.011', msg='验证f1值')
    def test_insert_047(self):
        '''
        timestamp类型，格式：日/月/年 时:分:秒:毫秒AM,query fail
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['03/01/2017 9:09:10:037AM'])
        self.assertTrue(res != 0, msg='insert_047写入失败')
    def test_insert_048(self):
        '''
        写入timestamp类型，数据类型为：时间戳（毫秒）,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['1647964800000'])
        self.assertTrue(res == 0, msg='insert_048写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)
            self.assertEqual(f1, 1647964800000, msg='验证f1值')
    def test_insert_049(self):
        '''
        写入timestamp类型，数据类型为：时间戳（秒）,写入成功，但客户端显示1970
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['1347964800'])
        self.assertTrue(res == 0, msg='insert_049写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_datetime_ms(1)

            self.assertEqual(f1, 1347964800, msg='验证f1值')



class Test_insert_time2(unittest.TestCase):
    tbNotNull = 't_time2'
    db = 'test_insert_time2' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        tbRes = tableOpt.createTb(cls.tbNotNull, {'f1': data_type['timestamp']+' not null'})
        cls().assertEqual(tbRes, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        # 删除数据库
        dropTb = tableOpt.dropTb(cls.tbNotNull)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')


    def test_insert_050(self):
        '''
        timestamp类型，字段设为not null，输入NULL,query failed
        '''
        res = tableOpt.insertTb(self.tbNotNull, ['f1'], ['NULL'])
        self.assertTrue(res != 0, msg='insert_050写入失败')
        res2 = tableOpt.insertTb(self.tbNotNull, ['f1'], [''])
        self.assertTrue(res2 != 0, msg='insert_050写入失败')
        res3 = tableOpt.insertTb(self.tbNotNull, ['f1'], [])
        self.assertTrue(res3 != 0, msg='insert_050写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')
    def test_insert_051(self):
        '''
        timestamp类型，字段设为not null，主键输入NULL，其他字段输入NULL,query failed
        '''
        res = tableOpt.insertTb(self.tbNotNull, ['time','f1'], ['NULL','NULL'])
        self.assertTrue(res != 0, msg='insert_051写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'], 0, msg='写入失败，返回0行')