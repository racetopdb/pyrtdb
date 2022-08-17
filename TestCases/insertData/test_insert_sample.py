import random
import unittest
from Conf.config import data_type
from Lib.tableOpt import *
from Lib.createDB import *
import random
import time
import datetime
from Comm.convert import *

db = 'test_insert_sample'+str(random.randrange(1,10000,100))
tb = 't_sample'+str(random.randrange(1,100000,10))
@unittest.skip('执行大批量时，跳过此用例')
class Test_insert_sample(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        res = conn.query("create db if not exists  " + db + ";")
        usql = 'use ' + db + ''
        ret = createDB.createSql(None, usql)
        tres = tableOpt.createTb(tb,
                                 {
                                     'f1': data_type['timestamp'],
                                     'f2':data_type['varchar']+'(50)',
                                     'f3':data_type['bigint'],
                                     'f4':data_type['float'],
                                     'f5':data_type['bool'],
                                     'f6':data_type['timestamp']
                                 })
        print(f'表的创建结果是：{tres}')
        # cls.assertEqual(tres, 0, msg='初始化创建表')
        # cls.assertEqual( res , 0, msg='创建数据库失败')

    @classmethod
    def tearDownClass(cls) -> None:

        tableOpt.dropTb(tb)
        r = conn.query_reader("drop db " + db + ";")
        # print(f'删除数据库的结果：{r}')
    @unittest.skip('跳过此用例')
    def test_tb_sample3(self):
        '''
        sampl3
        '''
        tb2 = tableOpt.createTb('test_0707tb',{'f1':data_type['int']})
        print(f'tb2的结果是：{tb2}')
        show2 = tableOpt.showTable()
        print(f'show2的结果是：{show2}')
        conn.print_stdout()
        tb3 = tableOpt.createTb('test_0707tb3', {'f1': data_type['int']})
        print(f'tb3的结果是：{tb3}')
        show3 = tableOpt.showTable()
        print(f'show3的结果是：{show3}')
        conn.print_stdout()


    @unittest.skip('跳过此用例')
    def test_tb_sample2(self):

        res = tableOpt.insertTb(tb, ['f1'],['1347964800'] )
        print(f'写入的结果是：{res}')
        show = tableOpt.showTable()
        print(f'show的结果是：{show}')
        last = tableOpt.selectLast(tb)
        print(f'last的结果是：{last}')
        conn.print_stdout()
        while last.cursor_next() == 0:
            f1 = last.get_datetime_ms(1)
            print(f1)
            # k = len(str(f1)) - 10
            # f1Timestamp = datetime.datetime.fromtimestamp(f1 / (1 * 10 ** k))
            # print(f1Timestamp)
            # f1Datatime = f1Timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            # print(f1Datatime)


    @unittest.skip('跳过此用例')
    def test_tb_sample1(self):
        # insert into t_int(f1) values(2147483646)
        nowDate = convert.get_date_stamp()
        res = tableOpt.insertTb(tb, ['time','f1','f2','f3','f4','f5','f6'], [nowDate,2147483646,'rtdb',4611686018427387902,1.22,True,'2022-07-05 10:00:00'])
        show = tableOpt.showTable()
        last = tableOpt.selectLast(tb)
        print(f'last的结果是：{last}')
        conn.print_stdout()
        while last.cursor_next() == 0:
            timekey = last.get_datetime_ms(0)
            print(timekey)
            f1 = last.get_int(1)
            print(f1)
            self.assertEqual(f1 , 2147483646 , msg='验证f1值')
            f2 = last.get_string(2)
            print(f2)
            self.assertEqual(f2 , 'rtdb' , msg='验证f2值')
            f3 = last.get_int64(3)
            print(f3)
            self.assertEqual(f3 , 4611686018427387902 , msg='验证f3值')
            f4 = last.get_float(4)
            print(format(f4,'.6f'))
            self.assertEqual(format(f4,'.6f') ,format(1.22,'.6f') , msg='验证f4值')
            f5 = last.get_bool(5)
            print(f5)
            self.assertEqual(f5 , True , msg='验证f5值')
            f6 = last.get_datetime_ms(6)
            print(f6)  # 1656986400000
            times = time.mktime(time.strptime('2022-07-05 10:00:00','%Y-%m-%d %H:%M:%S'))
            print(times*1000)
            self.assertEqual(f6 , times*1000, msg='验证f6值')

