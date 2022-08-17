# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
import datetime
from Conf.config import *
from Lib.createDB import *
from Lib.tableOpt import *
import logging
from Comm.convert import *


class Test_insert_value1(unittest.TestCase):
    db = 'test_insert_value1' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    tb = 'type_val'
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        #创建表
        tres =tableOpt.createTb(cls.tb,
                                {
                                    'f1':data_type['int'],
                                    'f2':data_type['bigint'],
                                    'f3':data_type['bool'],
                                    'f4':data_type['varchar']+'(50)',
                                    'f5':data_type['float'],
                                    'f6':data_type['double'],
                                    'f7':data_type['timestamp']
                                })
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')


    def test_insert_085(self):
        '''
        字段数量>值数量，忽略time主键,query fail
        '''

        res = tableOpt.insertTb(self.tb,['f1','f2','f3','f4','f5','f6','f7'],[1,12234,True,'顺实科技数据库' ,123.365,1234.2])
        self.assertTrue(res != 0 ,msg='insert_085写入失败')
    def test_insert_086(self):
        '''
        字段数量<值数量，，忽略time主键,query fail
        '''
        res = tableOpt.insertTb(self.tb,
                                ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'],
                                [1,12234,True,'顺实科技数据库' ,123.365,1234.2 ,'1648539213000',123]
                                )
        self.assertTrue(res != 0, msg='insert_086写入失败')
    def test_insert_087(self):
        '''
        字段数量=值数量，忽略time主键,query ok
        '''
        res = tableOpt.insertTb(self.tb,
                                ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'],
                                [1,12234,True,'顺实科技数据库' ,123.365,1234.2 ,'1648539213000']
                                )
        self.assertTrue(res == 0, msg='insert_086写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 1, msg='验证f1值')
            f2 = lastObj.get_int64(2)
            self.assertEqual(f2, 12234, msg='验证f2值')
            f3 = lastObj.get_bool(3)
            self.assertEqual(f3, True, msg='验证f3值')
            f4 = lastObj.get_string(4)
            self.assertEqual(f4, '顺实科技数据库', msg='验证f4值')
            f5 = lastObj.get_float(5)
            self.assertEqual(format(f5, '.3f'), format(123.365, '.3f'), msg='验证f1值')
            f6 = lastObj.get_float(6)
            self.assertEqual(format(f6, '.1f'), format(1234.2, '.1f'), msg='验证f6值')
            f7 = lastObj.get_datetime_ms(7)
            self.assertEqual(f7, 1648539213000, msg='验证f7值')
    def test_insert_088(self):
        '''
        字段数量=值数量，time主键值手动填入,query ok
        '''
        sleep(.1)
        nowDate = convert.get_date_stamp()
        res = tableOpt.insertTb(self.tb,
                                ['time','f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'],
                                [nowDate,1, 12234, True, '顺实科技数据库', 123.365, 1234.2, '1648539213000']
                                )
        self.assertEqual(res , 0, msg='insert_086写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            timekey = lastObj.get_datetime_ms(0)
            #把时间戳转成日期格式
            dates = convert.get_date_stamp(timekey)
            self.assertEqual(dates, nowDate, msg='验证time值')
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 1, msg='验证f1值')
            f2 = lastObj.get_int64(2)
            self.assertEqual(f2, 12234, msg='验证f2值')
            f3 = lastObj.get_bool(3)
            self.assertEqual(f3, True, msg='验证f3值')
            f4 = lastObj.get_string(4)
            self.assertEqual(f4, '顺实科技数据库', msg='验证f4值')
            f5 = lastObj.get_float(5)
            self.assertEqual(format(f5, '.3f'), format(123.365, '.3f'), msg='验证f1值')
            f6 = lastObj.get_float(6)
            self.assertEqual(format(f6, '.1f'), format(1234.2, '.1f'), msg='验证f6值')
            f7 = lastObj.get_datetime_ms(7)
            self.assertEqual(f7, 1648539213000, msg='验证f7值')

class Test_insert_value2(unittest.TestCase):
    tb = 'type_val2'
    db = 'test_insert_value2' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        # 创建表
        tres = tableOpt.createTb(cls.tb,
                                 {
                                     'f1': data_type['varchar'] + '(20) not null'
                                 })
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        # 删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')
    def test_insert_089(self):
        '''
        字段设为not null 输入空字符串'' ,[这是一个失败的用例]
        '''
        sql = " insert into "+self.tb+"(f1) values('') "
        res = tableOpt.insertTb(self.tb,[],[],sql)
        self.assertTrue(res == 0, msg='insert_089写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, '', msg='验证f1值')
            # self.assertIsNone(f1 ,msg='验证f1值')
    def test_insert_090(self):
        '''
        字段设为not null 不填值,query fail
        '''
        sql = " insert into type_val2(f1) values() "
        res = tableOpt.insertTb(self.tb,[],[],sql)
        self.assertTrue(res != 0, msg='insert_090写入失败')
    def test_insert_091(self):
        '''
        字段设为not null 填值,query ok
        '''
        res = tableOpt.insertTb(self.tb, ['f1'], ['2022-03-23'])
        self.assertTrue(res == 0, msg='insert_091写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, '2022-03-23', msg='验证f1值')

class Test_insert_value3(unittest.TestCase):
    tb = 'type_val3'
    db = 'test_insert_value3' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        # 创建表
        tres = tableOpt.createTb(cls.tb,
                                 {
                                     'f1': data_type['int'] + ' null'
                                 })
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        # 删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')
    def test_insert_092(self):
        '''
        字段设为null 不填值,query fail
        '''
        sql = " insert into "+self.tb+"(f1) values() "
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_092写入失败')
    def test_insert_093(self):
        '''
        字段设为null 填入空字符串'',query fail
        '''
        sql = " insert into " + self.tb + "(f1) values('') "
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_093写入失败')
    def test_insert_094(self):
        '''
        字段设为null 填入NULL,query ok
        '''
        sql = " insert into " + self.tb + "(f1) values(NULL) "
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_094写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 0, msg='验证f1值')
    def test_insert_095(self):
        '''
        字段设为null 填值,query ok
        '''
        sql = " insert into " + self.tb + "(f1) values(1222) "
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_095写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 1222, msg='验证f1值')

class Test_insert_value4(unittest.TestCase):
    tb = 'type_val4'
    db = 'test_insert_value4' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        # 创建表
        tres = tableOpt.createTb(cls.tb,
                                 {
                                     'desc': data_type['varchar'] + '(20)',
                                     'phone':data_type['int']
                                 })
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        # 删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')
    def test_insert_096(self):
        '''
        写入时字段的拼写有误，query fail
        '''
        res = tableOpt.insertTb(self.tb, ['des','phone'], ['描述信息',13808888888])
        self.assertTrue(res != 0, msg='insert_096写入失败')
        ret = tableOpt.showTable()
        self.assertEqual(ret['row'] , 0 ,msg='写入失败，返回0行')
    def test_insert_097(self):
        '''
        写入时，字段间没有分隔符，query fail
        '''
        sql = "insert into "+self.tb+"(desc  phone) values('描述信息',13808888888)"
        res = tableOpt.insertTb(None, [], [],sql)
        self.assertTrue(res != 0, msg='insert_097写入失败')
    def test_insert_098(self):
        '''
        写入时，最后一个values值加一个,，query fail
        '''
        sql = "insert into "+self.tb+"(desc ,phone) values('描述信息',19,)"
        res = tableOpt.insertTb(None, [], [],sql)
        self.assertTrue(res != 0, msg='insert_098写入失败')
    def test_insert_099(self):
        '''
        写入时：7个字段写入正确的数据类型,query ok
        '''
        tb5 = 'type_val5'
        cRes = tableOpt.createTb(tb5,
                                 {
                                     'f1':data_type['int'],
                                     'f2': data_type['bigint'],
                                     'f3': data_type['float'],
                                     'f4': data_type['bool'],
                                     'f5': data_type['double'],
                                     'f6': data_type['timestamp'],
                                     'f7': data_type['varchar']+'(10)',
                                 })
        self.assertEqual(cRes , 0 ,msg='099创建表失败')
        insert = tableOpt.insertTb(tb5,['f1','f2','f3','f4','f5','f6','f7'],[1,32,123.33,True,23.33,'2022-03-24','顺实科'])
        self.assertEqual(insert , 0 ,msg='099写入失败')
        lastObj = tableOpt.selectLast(tb5)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 1,msg='验证f1的值')
            f2 = lastObj.get_int64(2)
            self.assertEqual(f2, 32, msg='验证f2的值')
            f3 = lastObj.get_float(3)
            self.assertEqual(format(f3, '.2f'),  format(123.33, '.2f'), msg='验证f3的值')
            f4 = lastObj.get_bool(4)
            self.assertEqual(f4,True,msg='验证f4的值')
            f5 = lastObj.get_float(5)
            self.assertEqual(format(f5, '.2f'), format(23.33, '.2f'), msg='验证f5的值')
            f6 = lastObj.get_datetime_ms(6)

            k = len(str(f6)) - 10
            f6Timestamp = datetime.datetime.fromtimestamp(f6 / (1 * 10 ** k))

            f6Datatime = f6Timestamp.strftime("%Y-%m-%d")
            self.assertEqual(f6Datatime, '2022-03-24', msg='验证f6值')
            f7 = lastObj.get_string(7)
            self.assertEqual(f7, '顺实科', msg='验证f7值')
        droptb = tableOpt.dropTb(tb5)
        self.assertEqual(droptb,0,msg='删除创建的表')
    def test_insert_100(self):
        '''
        创建200个字段的表，写入200个值，queryok
        '''
        pass
    def test_insert_101(self):
        '''
        insert into 不加字段 不加values,query fail
        '''
        sql ="insert into "+self.tb+" ('描述信息',2)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_101写入失败')
    def test_insert_102(self):
        '''
        insert into 加字段 不加values,query fail
        '''
        sql = "insert into "+self.tb+"(desc,phone)  ('1',2)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_102写入失败')
    def test_insert_103(self):
        '''
        insert into字段与values直接不加空格,query ok
        '''
        sql = "insert into "+self.tb+"(desc,phone)values(1,2)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_103写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, '1', msg='验证f1值')
            f2 = lastObj.get_int(2)
            self.assertEqual(f2, 2, msg='验证f2值')
    def test_insert_104(self):
        '''
        insert into 表(字段1,字段2) value (值1,值2),query ok
        '''
        sql = "insert into " + self.tb + "(desc,phone)values('1',2)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='insert_104写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, '1', msg='验证f1值')
            f2 = lastObj.get_int(2)
            self.assertEqual(f2, 2, msg='验证f2值')
    def test_insert_105(self):
        '''
        insert into 表(字段1,字段2) ,value , (值1,值2),query fail
        '''
        sql = "insert into " + self.tb + "(desc,phone) ,value, (1,2)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_105写入失败')
    def test_insert_106(self):
        '''
        insert into 表(字段1,字段2) | value | (值1,值2),query fail
        '''
        sql = "insert into " + self.tb + "(desc,phone) |value| (1,2)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='insert_106写入失败')
    def test_insert_107(self):
        '''
        int：填入字母或汉字,query fail
        '''
        res = tableOpt.createTb('t_int',{'f1':data_type['int']})
        self.assertEqual(res, 0 ,msg='107创建表失败')
        ret = tableOpt.insertTb('t_int',['f1'],['顺实'])
        self.assertTrue(ret != 0, msg='insert_107写入失败')
        droptb = tableOpt.dropTb('t_int')
        self.assertEqual(droptb,0 ,msg='107删除表')
    def test_insert_108(self):
        '''
        float：填入整型或汉字 字母,queryfail
        '''
        res = tableOpt.createTb('t_float', {'f1': data_type['float']})
        self.assertEqual(res, 0, msg='108创建表失败')
        ret = tableOpt.insertTb('t_float', ['f1'], ['shunshi'])
        self.assertTrue(ret != 0, msg='insert_108写入失败')
        droptb = tableOpt.dropTb('t_float')
        self.assertEqual(droptb, 0, msg='108删除表')
    def test_insert_109(self):
        '''
        double：填入整型 汉字 字母,queryfail
        '''
        res = tableOpt.createTb('t_double', {'f1': data_type['double']})
        self.assertEqual(res, 0, msg='109创建表失败')
        ret = tableOpt.insertTb('t_double', ['f1'], ['shunshi'])
        self.assertTrue(ret != 0, msg='insert_109写入失败')
        droptb = tableOpt.dropTb('t_double')
        self.assertEqual(droptb, 0, msg='109删除表')
    def test_insert_110(self):
        '''
        bigint：填入特殊字符 汉字 字母,query fail
        '''
        res = tableOpt.createTb('t_bigint', {'f1': data_type['bigint']})
        self.assertEqual(res, 0, msg='109创建表失败')
        ret = tableOpt.insertTb('t_bigint', ['f1'], ['_test'])
        self.assertTrue(ret != 0, msg='insert_110写入失败')
        droptb = tableOpt.dropTb('t_bigint')
        self.assertEqual(droptb, 0, msg='110删除表')
    def test_insert_111(self):
        '''
        varchar：填入特殊字符 汉字 字母,query ok
        '''
        tb111 = 't_varchar'
        res = tableOpt.createTb(tb111, {'f1': data_type['varchar']+'(32)'})
        self.assertEqual(res, 0, msg='109创建表失败')
        ret = tableOpt.insertTb(tb111, ['f1'], ['*&^^*顺实科技_test'])
        self.assertTrue(ret == 0, msg='insert_111写入失败')
        lastObj = tableOpt.selectLast(tb111)
        while lastObj.cursor_next() == 0:
            f1 = lastObj.get_string(1)
            self.assertEqual(f1, '*&^^*顺实科技_test', msg='验证f1值')
        droptb = tableOpt.dropTb(tb111)
        self.assertEqual(droptb, 0, msg='111删除表')
    def test_insert_112(self):
        '''
        timstamp：填入不支持的日期格式 或者 字母 数字 特殊字符,query fail
        '''
        tb112 = 't_time'
        res = tableOpt.createTb(tb112, {'f1': data_type['timestamp']})
        self.assertEqual(res, 0, msg='112创建表失败')
        ret = tableOpt.insertTb(tb112, ['f1'], ['002_test'])
        self.assertTrue(ret != 0, msg='insert_112写入失败')
        droptb = tableOpt.dropTb(tb112)
        self.assertEqual(droptb, 0, msg='112删除表')
    def test_insert_113(self):
        '''
        boolean：填入 特殊字符*1,query fail
        '''
        tb113 ='t_bool'
        res = tableOpt.createTb(tb113, {'f1': data_type['bool']})
        self.assertEqual(res, 0, msg='113创建表失败')
        ret = tableOpt.insertTb(tb113, ['f1'], ['*1'])
        self.assertTrue(ret != 0, msg='insert_113写入失败')
        droptb = tableOpt.dropTb(tb113)
        self.assertEqual(droptb, 0, msg='113删除表')

class Test_insert_value5(unittest.TestCase):
    db = 'test_insert_value6' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    tb = 'type_val6'
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')

        #创建表
        tres =tableOpt.createTb(cls.tb,
                                {
                                    'f1':data_type['int'],
                                    'f2':data_type['int'],
                                    'f3':data_type['int']
                                })
        cls().assertEqual(tres, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb = tableOpt.dropTb(cls.tb)
        cls().assertEqual(dropTb, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_insert_114(self):
        '''
        值之间用：分隔,query fail
        '''
        sql = 'insert into '+self.tb+'(f1,f2,f3) values (1:3:4)'
        res = tableOpt.insertTb(None,[],[],sql)
        self.assertTrue(res != 0,msg='114写入失败')
    def test_insert_115(self):
        '''
        值之间用空格分隔,query fail
        '''
        sql = 'insert into '+self.tb+'(f1,f2,f3) values (1 3 4)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='115写入失败')
    def test_insert_116(self):
        '''
        值之间用|分隔,query fail
        '''
        sql = ' insert into '+self.tb+'(f1,f2,f3) values (1|3|4)'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='116写入失败')
    def test_insert_117(self):
        '''
        值之间用换行分隔,query fail
        '''
        pass
    def test_insert_118(self):
        '''
        values括号使用【】,query fail
        '''
        sql = ' insert into ' + self.tb + '(f1,f2,f3) values 【1,3,4】'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='118写入失败')
    def test_insert_119(self):
        '''
        values括号使用{},query fail
        '''
        sql = ' insert into ' + self.tb + '(f1,f2,f3) values {1,3,4}'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='119写入失败')
    def test_insert_120(self):
        '''
        values括号使用[],query fail
        '''
        sql = ' insert into ' + self.tb + '(f1,f2,f3) values [1,3,4]'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='120写入失败')
    def test_insert_121(self):
        '''
        values不使用(),query fail
        '''
        sql = ' insert into ' + self.tb + '(f1,f2,f3) values 1,3,4'
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='121写入失败')
    def test_insert_122(self):
        '''
         不加字段（字段1，字段2）写入,query ok
        '''
        nowDate = convert.get_date_stamp()
        res = tableOpt.insertTb(self.tb, [], [nowDate,1,2,3])
        self.assertTrue(res == 0, msg='122写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            timekey = lastObj.get_datetime_ms(0)
            # 把时间戳转成日期格式
            dates = convert.get_date_stamp(timekey)
            self.assertEqual(dates, nowDate, msg='验证time值')
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 1, msg='验证f1的值')
            f2 = lastObj.get_int(2)
            self.assertEqual(f2, 2, msg='验证f2的值')
            f3 = lastObj.get_int(3)
            self.assertEqual(f3, 3, msg='验证f3的值')
    def test_insert_123(self):
        '''
        写入时：带字段和值 query ok
        '''
        nowDate = convert.get_date_stamp()
        res = tableOpt.insertTb(self.tb, [], [nowDate, 88, 99, 77])
        self.assertTrue(res == 0, msg='123写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            timekey = lastObj.get_datetime_ms(0)
            # 把时间戳转成日期格式
            dates = convert.get_date_stamp(timekey)
            self.assertEqual(dates, nowDate, msg='验证time值')
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 88, msg='验证f1的值')
            f2 = lastObj.get_int(2)
            self.assertEqual(f2, 99, msg='验证f2的值')
            f3 = lastObj.get_int(3)
            self.assertEqual(f3, 77, msg='验证f3的值')
    def test_insert_124(self):
        '''
        值后面多加特殊符号写入,query fail
        '''
        sql = "insert into " + self.tb + " values ('2022/03/24',1,2,3,)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='124写入失败')
    def test_insert_125(self):
        '''
        值前面加单行注释,query fail
        '''
        sql = "insert into " + self.tb + " values  #单行注释 ('2022/03/24',1,2,3)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='125写入失败')
    def test_insert_126(self):
        '''
        值后面加多行注释,query ok
        '''
        sleep(.1)
        nowDate = convert.get_date_stamp()
        sql = "insert into "+self.tb+" values /*多行注释*/ ('"+nowDate+"',1,2,3)"

        res = tableOpt.insertTb(None, [], [],sql)
        self.assertEqual(res , 0, msg='126写入失败')
        lastObj = tableOpt.selectLast(self.tb)
        while lastObj.cursor_next() == 0:
            timekey = lastObj.get_datetime_ms(0)
            # 把时间戳转成日期格式
            dates = convert.get_date_stamp(timekey)
            self.assertEqual(dates, nowDate, msg='验证time值')
            f1 = lastObj.get_int(1)
            self.assertEqual(f1, 1, msg='验证f1的值')
            f2 = lastObj.get_int(2)
            self.assertEqual(f2, 2, msg='验证f2的值')
            f3 = lastObj.get_int(3)
            self.assertEqual(f3, 3, msg='验证f3的值')
    def test_insert_127(self):
        '''
        一次写入多条数据，不加字段列,query ok
        '''
        sql = "insert into "+self.tb+" values ('2022/06/24', 11, 2,4)  ( '2022/06/25', 511, 2,4)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='127写入失败')
    def test_insert_128(self):
        '''
        一次写入多条数据，加字段列,query ok
        '''
        sql = "insert into "+self.tb+"(time,f1,f2,f3) values ('2022/06/09', 11, 2,4)  ( '2022/06/10', 5511, 102,465)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='128写入失败')
    def test_insert_129(self):
        '''
        多条数据之间加换行,query fail
        '''
        sql = "insert into "+self.tb+"(time,f1,f2,f3) values ('2022/03/24', 11, 2,4) \n ( '2022/03/24', 511, 2,4)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='129写入失败')
    def test_insert_130(self):
        '''
        多条数据之间加多行注释,query ok
        '''
        sql = "insert into "+self.tb+"(time,f1,f2,f3) values ('2022/06/10 01:00:00', 555, 2,4)  /**多行注释文本**/ ( '2022/06/10 01:02:00' , 666, 2,4)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='130写入失败')
    def test_insert_131(self):
        '''
        多条数据之间用逗号分隔,query ok
        '''
        sql = "insert into "+self.tb+"(time,f1,f2,f3) values ('2022/06/10 01:02:03', 777, 2,4) ,('2022/06/10 01:02:04', 888, 2,4), ('2022/06/10 01:02:05', 999, 333,444)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='131写入失败')


class Test_insert_value6(unittest.TestCase):
    db = 'test_insert_value7' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    tb7 = 'type_val7'
    tb8 = 'type_val8'
    @classmethod
    def setUpClass(cls) -> None:
        res = createDB.createSql(cls.db)
        cls().assertEqual(res, 0, msg='初始化创建数据库')
        usql = 'use ' + cls.db + ''
        use = createDB.createSql(None, usql)
        cls().assertEqual(use, 0, msg='初始化use数据库')
        res1 =tableOpt.createTb(cls.tb7,
                                {
                                    'f1':data_type['int'],
                                    'f2':data_type['float'],
                                    'f3':data_type['timestamp']
                                })
        cls().assertEqual(res1, 0, msg='初始化创建表')
        res2 = tableOpt.createTb(cls.tb8,
                                 {
                                     'f1': data_type['bool'],
                                     'f2': data_type['varchar']+'(20)',
                                     'f3': data_type['bigint']
                                 })
        cls().assertEqual(res2, 0, msg='初始化创建表')

    @classmethod
    def tearDownClass(cls) -> None:
        #删除数据库
        dropTb7 = tableOpt.dropTb(cls.tb7)
        cls().assertEqual(dropTb7, 0, msg='初始化删除表')
        dropTb8 = tableOpt.dropTb(cls.tb8)
        cls().assertEqual(dropTb8, 0, msg='初始化删除表')
        dropDb = createDB.dropDB(cls.db)
        cls().assertEqual(dropDb, 0, msg='删除初始化创建的数据库')

    def test_insert_132(self):
        '''
        多条数据，不带字段列写入,query ok
        '''
        sql = "insert into "+self.tb7+" values ('1648606533000',1,2.03,'2022/03/24 10:52:52')  ('1648606544000',6,2.03,'2022/03/24 10:52:52') "+self.tb8+" values ('1648606555000',True,'顺实科技',123) ('1648606566000',yes,'数据库',4567)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='132写入失败')
    def test_insert_133(self):
        '''
        多条数据，带字段列写入,query ok
        '''
        sql = "insert into "+self.tb7+"(time,f1,f2,f3) values ('1654741847991',1,2.03,'2022/03/24 10:52:52') ('1654741861669',6,2.03,'2022/03/24 10:52:52') "+self.tb8+"(time,f1,f2,f3) values ('1654741871716',True,'顺实科技',123) ('1654741882201',yes,'数据库',4567)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='133写入失败')
    def test_insert_134(self):
        '''
        多表单条数据写入,query ok
        '''
        sql = "insert into "+self.tb7+"(time,f1,f2,f3) values ('1657276817201',1,2.03,'2022/03/24 10:52:52') "+self.tb8+"(time,f1,f2,f3) values ('1657276852265',True,'顺实科技',123)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertEqual(res , 0, msg='134写入失败')
    def test_insert_135(self):
        '''
        多个表，表与表之间的分隔符，逗号,query ok
        '''
        sql = "insert into "+self.tb7+"(time,f1,f2,f3) values ('1654743353788',1,2.03,'2022/03/24 10:52:52')  ('1654743360787',6,2.03,'2022/03/24 10:52:52') ,"+self.tb8+"(time,f1,f2,f3) values ('1654743371429',True,'顺实科技',123) ('1654743378832',yes,'数据库',4567)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='134写入失败')
    def test_insert_136(self):
        '''
        多个表，表与表之间的分隔符 空格,query ok
        '''
        sql = "insert into "+self.tb7+" values('2022/03/24',1,2.02,'2022-07-08 10:48:00') ('2022/03/25',9,4.04,'2022-07-08 10:50:00') "+self.tb8+" values('2022/03/24',1,'rtdb',123456) ('2022/03/25',0,'rtdb88',789456)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='136写入失败')
    def test_insert_137(self):
        '''
        多个表，表与表之间的分隔符 |,query fail
        '''
        sql = "insert into "+self.tb7+"(time,f1,f2,f3) values ('1654744192566',1,2.03,'2022/03/24 10:52:52')  ('1654744200690',6,2.03,'2022/03/24 10:52:52') | "+self.tb8+"(time,f1,f2,f3) values ('1654744207435',True,'顺实科技',123) ('1654744215098',yes,'数据库',4567)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='137写入失败')
    def test_insert_138(self):
        '''
        多个表，表与表之间的单行注释,query ok
        '''
        sql = "insert into "+self.tb7+"(time,f1,f2,f3) values ('1654744253620',1,2.03,'2022/03/24 10:52:52')  ('1654744263853',6,2.03,'2022/03/24 10:52:52') #单行注释 "+self.tb8+"(time,f1,f2,f3) values ('1654744274467',True,'顺实科技',123) ('1654744282819',yes,'数据库',4567)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='138写入失败')
    def test_insert_139(self):
        '''
        多个表，表与表之间的多行注释,query ok
        '''
        sql = "insert into "+self.tb7+"(time,f1,f2,f3) values ('1654744716119',1,2.03,'2022/03/24 10:52:52')  ('1654744732232',6,2.03,'2022/03/24 10:52:52') /*多行注释*/ "+self.tb8+"(time,f1,f2,f3) values ('1654744741544',True,'顺实科技123',123) ('1654744752086',yes,'数据库45678999',4567)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='139写入失败')
    def test_insert_140(self):
        '''
        每个表的value之间的分隔符 空格,query ok
        '''
        sql = "insert into "+self.tb7+" values ('1654745781077',1,2.03,'2022/03/24 10:52:52')  ('1654745787386',6,2.03,'2022/03/24 10:52:52') "+self.tb8+" values ('1654745792766',True,'顺实科技123',123) ('1654745798677',yes,'数据库45678999',4567)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='140写入失败')
    def test_insert_141(self):
        '''
        每个表的value之间的分隔符 换行,query fail
        '''
        sql = "insert into "+self.tb7+"values\n('2022-07-08 10:20:00',1,2.03,'2022/03/24 10:52:52')\n('2022-07-08 10:21:00',1,2.03,'2022/03/24 10:52:52') "+self.tb8+" values ('2022-07-08 11:00:00',True,'顺实科技123',123)\n ('2022-07-08 11:01:00',True,'顺实科技123',123)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='141写入失败')
    def test_insert_142(self):
        '''
        每个表的value之间的分隔符 逗号,query ok
        '''

        sql = "insert into "+self.tb7+" values ('2022-07-10 10:00:01',1,2.03,'2022/03/24 10:52:52'), ('2022-07-10 10:00:02',6,2.03,'2022/03/24 10:52:52') "+self.tb8+" values ('2022-07-10 10:00:01',True,'顺实科技123',123), ('2022-07-10 10:00:02',yes,'数据库45678999',4567)"

        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='142写入失败')
    def test_insert_143(self):
        '''
        每个表的value之间的单行注释,注释前的queryok
        '''
        sql = "insert into "+self.tb7+" values ('2022-07-11 10:00:04',1,2.03,'2022/03/24 10:52:52')  #单行注释 ('2022-07-11 10:00:05',9,12.03,'2022/03/29 10:52:52')  "+self.tb8+" values ('2022-07-11 10:00:04',True,'顺实科技',123)  #单行注释 ('2022-07-11 10:00:05',True,'顺实科技123',456) "
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='143写入失败')
    def test_insert_144(self):
        '''
        每个表的value之间的多行注释,query ok
        '''
        sql = "insert into "+self.tb7+" values ('2022-07-11 10:00:09',1,2.03,'2022/03/24 10:52:52')  /*多行注释*/ ('2022-07-11 10:00:10',9,12.03,'2022/03/29 10:52:52') "+self.tb8+" values ('2022-07-11 10:00:10',True,'顺实科技',123) /*多行注释*/ ('2022-07-17 10:00:16',True,'顺实科技123',11111)"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res == 0, msg='144写入失败')
    def test_insert_145(self):
        '''
        主键time的值相同的数据，重复写入,query fail
        '''
        sql = "insert into "+self.tb7+" values ('2022-07-11 10:00:11',30,2.03,'2022/03/24 10:52:52') , ('2022-07-11 10:00:11',31,12.03,'2022/03/25 10:52:52'),('2022-07-11 10:00:11',32,12.03,'2022/03/26 10:52:52'),('2022-07-11 10:00:11',33,12.03,'2022/03/27 10:52:52')"
        res = tableOpt.insertTb(None, [], [], sql)
        self.assertTrue(res != 0, msg='144写入失败')










