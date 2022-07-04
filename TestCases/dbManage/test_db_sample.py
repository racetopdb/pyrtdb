# -*- coding: utf-8 -*-

from TestCases.dbManage.setupModule import *

logger = logging.getLogger('main.Test_db3')

class Test_db_sample(unittest.TestCase):
    def test_db_sample(self):
        pass

        # dbName = 'testdb0620'
        # res = createDB.createSql(dbName)
        # print(res)
        # sql = 'show db'
        # show = createDB.createSql(None,sql)


        # reader  = conn.query_reader('show db')
        # conn.print_stdout()
        # while 0 == reader.cursor_next():
        #   #  print(conn.print_str())
        #     print(2222)
        #     name = reader.get_string(0)
        #     id = reader.get_int(1)
        #     email = reader.get_string(2)
        #     password = reader.get_string(3)
        #     print("one row data", id, email, password)

        # dbName = 'rtdb_test'+str(int(time.time()))
        # res = createDB.createSql(None,'create db '+dbName+'')
        # self.assertEqual(res ,0 )
        # use = createDB.createSql(None,'use '+dbName+'')
        # self.assertEqual(use ,0 )
        # currentDB = conn.get_db_current()
        # print(f'当前use的数据库是：{currentDB}')
        # self.assertEqual(currentDB,dbName)
        # table = createDB.createSql(None,'create table test001(f1 int,f2 int);')
        # table2 = createDB.createSql(None, 'create table test002(f1 int,f2 int);')
        # self.assertEqual(table,0)
        # insert = createDB.createSql(None,'insert into test001(f1,f2) values(1,2)')
        # insert2 = createDB.createSql(None, 'insert into test002(f1,f2) values(1,2)')
        # print(f'写入的结果是：{insert}')
        # self.assertEqual(insert, 0)
        #
        # showTb = createDB.showTable()
        # print(f'showtb的结果是：{showTb}')

        # drop = createDB.dropDB(dbName)
        # self.assertEqual(drop, None)

