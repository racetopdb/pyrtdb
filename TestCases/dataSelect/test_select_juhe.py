# -*- coding: utf-8 -*-
import unittest,datetime
from Comm.pyrtdb import conn
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import os,sys
from Comm.convert import *
from Comm.data import *

print(config['testDataPath'])
path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
# print(f'聚合里面的文件路径是：{path}')
@unittest.skip('执行大批量时，跳过此用例')
class Test_tb_juhe(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        sql = 'use DB_TEST_WRITE_100'
        res = tableOpt.querySql(sql)
        cls().assertEqual(res ,0 ,msg='初始化use数据库')

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_juhe_001(self):
        '''
        聚合函数count,
        分组类型：周（w,week,interval '1 week'）,
        数据类型： int
        '''
        sql = "select bound_first(*),count(F_1) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1w)"
        res = tableOpt.querySql(sql,1)
        row = res.get_row_count()
        self.assertEqual(row , 3 ,msg='验证行数')
        i = 0
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            countF_1 = res.get_int(1)
            if i == 0:
                self.assertEqual(countF_1,6048001,msg='验证f_1的值')
                self.assertEqual(bound_first,1640966400000, msg='验证bound_first的值')
            if i ==1:
                self.assertEqual(countF_1, 6048001, msg='验证f_1的值')
                self.assertEqual(bound_first, 1641571200000, msg='验证bound_first的值')
            if i == 2:
                self.assertEqual(countF_1, 2903998, msg='验证f_1的值')
                self.assertEqual(bound_first, 1642176000000, msg='验证bound_first的值')
            i+=1

    def test_juhe_002(self):
        '''
        聚合函数:count，
        分组类型：日（d, day ,interval '1 day'），
        数据类型为bigint,查询成功
        '''
        sql = "select bound_first(*), count(F_2) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1day)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 19, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            countF_1 = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'countF_1': countF_1
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None,sheet_name='juhe_002')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['countF_1'], int(row[1]), msg='验证countF_1的值')


    def test_juhe_003(self):
        '''
        聚合函数：count，
        分组类型：时（h,hour, interval '1 hour')，
        数据类型：float
        '''
        sql = "select bound_first(*),count(F_3) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1hour)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 433, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            countF_3 = res.get_int(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'countF_3': countF_3
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_003')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['countF_3'], float(row[1]), msg='验证countF_3的值')
    def test_juhe_004(self):
        '''
        聚合函数：count,
        分组类型：分钟（m,minute,interval '1 minute'）
        数据类型： timestamp
        '''
        sql = "select bound_first(*),count(F_6) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1000m)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 26, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            countF_1 = res.get_int(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'countF_1': countF_1
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_004')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['countF_1'], int(row[1]), msg='验证countF_1的值')
    def test_juhe_005(self):
        '''
        聚合函数：count,
        分组类型：秒（s,second,interval '1 second'）
        数据类型： boolean
        '''
        sql = "select bound_first(*),count(F_0) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(50000second)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 32, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            countF_1 = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'countF_1': countF_1
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_005')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['countF_1'], int(row[1]), msg='验证countF_1的值')
    def test_juhe_006(self):
        '''
        聚合函数：count,
        分组类型：毫秒（ms,interval '1 ms'）
        数据类型： varchar
        '''
        sql = "select bound_first(*),count(F_5) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1000009ms)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 1556, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            countF_1 = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'countF_1': countF_1
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_006')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['countF_1'], int(row[1]), msg='验证countF_1的值')
    def test_juhe_007(self):
        '''
        聚合函数：avg
        分组类型：周（w,week,interval '1 week'）
        数据类型：bigint
        '''
        sql = "select bound_first(*),avg(F_2) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1w)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 3, msg='验证行数')
        i = 0
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            avgF_2 = res.get_int64(1)
            if i == 0:
                self.assertEqual(avgF_2,2157598,msg='验证f_2的值')
                self.assertEqual(bound_first,1640966400000, msg='验证bound_first的值')
            if i ==1:
                self.assertEqual(avgF_2, 2339196, msg='验证f_2的值')
                self.assertEqual(bound_first, 1641571200000, msg='验证bound_first的值')
            if i == 2:
                self.assertEqual(avgF_2, 3548001, msg='验证f_2的值')
                self.assertEqual(bound_first, 1642176000000, msg='验证bound_first的值')
            i += 1
    def test_juhe_008(self):
        '''
        聚合函数：avg
        分组类型：日（d,day,interval '1 day'）
        数据类型：int
        '''
        sql = "select bound_first(*),avg(F_1) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1d)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 19, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            avgF_1 = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'avgF_1': avgF_1
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_008')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['avgF_1'], int(row[1]), msg='验证avgF_1的值')
    def test_juhe_009(self):
        '''
        聚合函数：avg
        分组类型：时（h,hour,interval '1 hour'）
        数据类型：timestamp
        '''
        sql = "select bound_first(*),avg(F_6) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1h)"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='查询失败，时间格式不支持avg')
    def test_juhe_010(self):
        '''
        聚合函数：avg
        分组类型：分（m,minute,interval '1 minute'）
        数据类型：float
        '''
        sql = "select bound_first(*),avg(F_3) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(720m)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 37, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            avgF_3 = res.get_float(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'avgF_3': avgF_3
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_010')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['avgF_3'], row[1], msg='验证avgF_3的值')
    def test_juhe_011(self):
        '''
        聚合函数：avg
        分组类型：秒（s,second,interval '1 second'）
        数据类型：varchar
        '''
        sql = "select bound_first(*),avg(F_5) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1s)"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='查询失败，varchar不支持avg')
    def test_juhe_012(self):
        '''
        聚合函数：avg
        分组类型：毫秒（ms,interval '1 ms'）
        数据类型：boolean
        '''
        sql = "select bound_first(*),AVG(F_0) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1000000ms)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 1556, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            avgF_0 = res.get_bool(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'avgF_0': avgF_0
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_012')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['avgF_0'], row[1], msg='验证avgF_0的值')
    def test_juhe_013(self):
        '''
        聚合函数：sum
        分组类型：周（w,week,interval '1 week'）
        数据类型：float
        '''
        sql ="select bound_first(*),sum(F_3) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1week)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 3, msg='验证行数')
        i = 0
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            sumF_3 = res.get_float(1)
            if i == 0:
                self.assertEqual(sumF_3, 26098305859584.000000, msg='验证f_3的值')
                self.assertEqual(bound_first, 1640966400000, msg='验证bound_first的值')
            if i == 1:
                self.assertEqual(sumF_3, 28294917390336.000000, msg='验证f_3的值')
                self.assertEqual(bound_first, 1641571200000, msg='验证bound_first的值')
            if i == 2:
                self.assertEqual(sumF_3, 20606774935552.000000, msg='验证f_3的值')
                self.assertEqual(bound_first, 1642176000000, msg='验证bound_first的值')
            i += 1
    def test_juhe_014(self):
        '''
        聚合函数：sum
        分组类型：日（d,day,interval '1 day'）
        数据类型：timestamp
        '''
        sql = "select  bound_first(*),sum(F_6) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1day)"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='查询失败，timestamp不支持sum')
    def test_juhe_015(self):
        '''
        聚合函数：sum
        分组类型：时（h,hour,interval '1 hour'）
        数据类型：int
        '''
        sql = "select bound_first(*),sum(F_1) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(48hour)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 10, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            sumF_0 = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'sumF_0': sumF_0
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_015')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['sumF_0'], row[1], msg='验证sumF_0的值')
    def test_juhe_016(self):
        '''
        聚合函数：sum
        分组类型：分（m,minute,interval '1 minute'）
        数据类型：bigint
        '''
        sql = "select bound_first(*),sum(F_2) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(interval '120 minute')"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 217, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            sumF_0 = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'sumF_0': sumF_0
            })
            i += 1

        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_016')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['sumF_0'], row[1], msg='验证sumF_0的值')
    def test_juhe_017(self):
        '''
        聚合函数：sum
        分组类型：秒（s,second,interval '1 second'）
        数据类型：int
        '''
        sql = "select  bound_first(*),sum(F_1) from T_0 where time between '2022-01-01 ' and '2022-01-19' group by time(interval '1000000 second')"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 2, msg='验证行数')
        i = 0
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            sumInt = res.get_int64(1)
            if i == 0:
                self.assertEqual(sumInt, 25000005000003, msg='验证值')
                self.assertEqual(bound_first, 1640966400000, msg='验证bound_first的值')
            if i == 1:
                self.assertEqual(sumInt, 12500002499997, msg='验证值')
                self.assertEqual(bound_first, 1641966400000, msg='验证bound_first的值')
            i += 1
    def test_juhe_018(self):
        '''
        聚合函数：sum
        分组类型：毫秒（ms,interval '1 ms'）
        数据类型：bigint
        '''
        sql = "select  bound_first(*),sum(F_2) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(interval '10000000 ms')"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 156, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            sumBig = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'sumBig': sumBig
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_018')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['sumBig'], row[1], msg='验证sumBig的值')
    def test_juhe_019(self):
        '''
        聚合函数：sum
        分组类型：all
        数据类型：boolean
        '''
        sql = "select bound_first(*),sum(F_0) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(all)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 1, msg='验证行数')
        i = 0
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            sumInt = res.get_int(1)
            if i == 0:
                self.assertEqual(sumInt, 7500000, msg='验证值')
                self.assertEqual(bound_first, 1640966400000, msg='验证bound_first的值')
            i += 1
    def test_juhe_020(self):
        '''
        聚合函数：max
        分组类型：周（w,week,interval '1 week'）
        数据类型：timestamp
        '''
        sql = "select  bound_first(*),max(F_6) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1 week)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 3, msg='验证行数')
        i = 0
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            maxTime = res.get_datetime_ms(1)
            if i == 0:
                self.assertEqual(maxTime, 1641571199901, msg='验证值')
                self.assertEqual(bound_first, 1640966400000, msg='验证bound_first的值')
            if i == 1:
                self.assertEqual(maxTime, 1642175999902, msg='验证值')
                self.assertEqual(bound_first, 1641571200000, msg='验证bound_first的值')
            if i == 2:
                self.assertEqual(maxTime, 1642466399702, msg='验证值')
                self.assertEqual(bound_first, 1642176000000, msg='验证bound_first的值')
            i += 1
    def test_juhe_021(self):
        '''
        聚合函数：max
        分组类型：日（d,day,interval '1 day'）
        数据类型：float
        '''
        sql ="select  bound_first(*),max(F_3) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(2 day)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 10, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            maxFloat = res.get_float(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'maxFloat': maxFloat
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_021')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['maxFloat'], float(row[1]), msg='验证maxFloat的值')
    def test_juhe_022(self):
        '''
        聚合函数：max
        分组类型：时（h,hour,interval '1 hour'）
        数据类型：bigint
        '''
        sql = "select bound_first(*),max(F_2) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(2h)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 217, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            maxBig = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'maxBig': maxBig
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_022')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['maxBig'], row[1], msg='验证maxBig的值')
    def test_juhe_023(self):
        '''
        聚合函数：max
        分组类型：分（m,minute,interval '1 minute'）
        数据类型：int
        '''
        sql = "select bound_first(*),max(F_1) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(1000m)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 26, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            maxInt = res.get_int(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'maxBig': maxInt
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_023')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['maxInt'], row[1], msg='验证maxInt的值')
    def test_juhe_024(self):
        '''
        聚合函数：max
        分组类型：秒（s,second,interval '1 second'）
        数据类型：bigint
        '''
        sql = "select bound_first(*),max(F_2) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(300000 s)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 6, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            maxBig = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'maxBig': maxBig
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_024')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['maxBig'], row[1], msg='验证maxInt的值')
    def test_juhe_025(self):
        '''
        聚合函数：max
        分组类型：毫秒（ms,interval '1 ms'）
        数据类型：int
        '''
        sql = "select bound_first(*),max(F_1) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(3000000 ms)"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 519, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            maxInt = res.get_int(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'maxInt': maxInt
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_025')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['maxInt'], row[1], msg='验证maxInt的值')
    def test_juhe_026(self):
        '''
        聚合函数：max
        分组类型：all
        数据类型：varchar
        '''
        sql ="select  bound_first(*),max(F_5) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(all)"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='查询失败，varchar不支持max')
    def test_juhe_027(self):
        '''
        聚合函数：min
        分组类型：周（w,week,interval '1 week'）
        数据类型：boolean
        '''
        sql = "select bound_first(*),min(F_0) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(interval '1 week')"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 3, msg='验证行数')
        i = 0
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            minbool = res.get_bool(1)
            if i == 0:
                self.assertEqual(minbool, False, msg='验证值')
                self.assertEqual(bound_first, 1640966400000, msg='验证bound_first的值')
            if i == 1:
                self.assertEqual(minbool, False, msg='验证值')
                self.assertEqual(bound_first, 1641571200000, msg='验证bound_first的值')
            if i == 2:
                self.assertEqual(minbool, False, msg='验证值')
                self.assertEqual(bound_first, 1642176000000, msg='验证bound_first的值')
            i += 1
    def test_juhe_028(self):
        '''
        聚合函数：min
        分组类型：日（d,day,interval '1 day'）
        数据类型：varchar
        '''
        sql = "select  bound_first(*),min(F_5) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(interval '1day')"
        res = tableOpt.querySql(sql)
        self.assertTrue(res != 0, msg='查询失败，varchar不支持min')
    def test_juhe_029(self):
        '''
        聚合函数：min
        分组类型：时（h,hour,interval '1 hour'）
        数据类型：int
        '''
        sql = "select  bound_first(*),min(F_1),first(time),last(time) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(interval '24 hour')"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 19, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            minInt = res.get_int(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'minInt': minInt
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_029')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['minInt'], row[1], msg='验证minInt的值')
    def test_juhe_030(self):
        '''
        聚合函数：min
        分组类型：分（m,minute,interval '1 minute'）
        数据类型：bigint
        '''
        sql = "select  bound_first(*),min(F_2) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(interval '360 minute')"
        res = tableOpt.querySql(sql, 1)
        row = res.get_row_count()
        self.assertEqual(row, 73, msg='验证行数')
        i = 0
        result = {}
        while res.cursor_next() == 0:
            bound_first = res.get_datetime_ms(0)
            minInt = res.get_int64(1)
            result[i] = dict()
            result[i].update({
                'bound_first': bound_first,
                'minInt': minInt
            })
            i += 1
        data_dict = read_excel(r"" + config['testDataPath'] + "\\juhe_02_040.xlsx", header=None, sheet_name='juhe_030')
        for j, row in enumerate(data_dict):
            self.assertEqual(result[j]['bound_first'], int(row[0][25:38]), msg='验证bound_first的值')
            self.assertEqual(result[j]['minInt'], row[1], msg='验证minInt的值')
    def test_juhe_031(self):
        '''
        聚合函数：min
        分组类型：秒（s,second,interval '1 second'）
        数据类型：float
        '''
        sql = "select bound_first(*),min(F_3) from T_0 where time between '2022-01-01' and '2022-01-19' group by time(interval '10000 second')"



