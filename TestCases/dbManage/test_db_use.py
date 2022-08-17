# -*- coding: utf-8 -*-
from TestCases.dbManage.setupModule import *


logger = logging.getLogger('main.Test_db_use')

class Test_db_use(unittest.TestCase):
    def test_db_085(self):
        '''
        use ''
        '''
        dbName = 'testdb085'
        res = createDB.createSql(dbName)
        self.assertEqual(res , 0)
        usql = 'use testdb085'
        uRes = createDB.createSql(None,usql)
        self.assertEqual(uRes,0)
        currentDB = createDB.currentDB()
        self.assertEqual(currentDB, 'testdb085')
        usql2 = "use '' "
        uRes2 = createDB.createSql(None, usql2)
        self.assertEqual(uRes2, 0)
        currentDB2 = createDB.currentDB()
        self.assertEqual(currentDB2, 'testdb085')
        drop = createDB.dropDB('testdb085')
        self.assertEqual(drop , 0,msg='删除创建的库')
    def test_db_086(self):
        '''
        use
        '''
        usql = 'use  '
        res = createDB.createSql(None,usql)
        self.assertNotEqual(res ,0 ,msg='use后面空的，执行失败')


@unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
class Test_db_use_win(unittest.TestCase):

    def test_db_069(self):
        '''
        win平台：use 直接打开一个路径，路径未转义 未带引号,query fail
        '''
        sql = 'create db @"E:/rtdb_test/db_use069"'
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0)
        #use
        sql = 'use E:\\rtdb_test\db_use069'
        use = createDB.createSql(None,sql)
        self.assertTrue(use != 0, msg='use error')
        # currentDB = createDB.currentDB()
        # self.assertTrue(currentDB == 'db_use069', msg='use error')
        drop = createDB.dropDB('db_use069')
        self.assertEqual(drop, 0)
    def test_db_070(self):
        '''
        win:use 带路径，路径不带\转义并带引号，query fail
        '''
        sql = 'create db @"E:/rtdb_test/db_use070"'
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0,msg='创建数据库失败db_use070')
        # use
        sql = "use 'E:\\rtdb_test\db_use070'"
        use = createDB.createSql(None, sql)

        self.assertTrue(use != 0, msg='use error')
        # currentDB = createDB.currentDB()
        # self.assertTrue(currentDB == 'db_use070', msg='use error')
        drop = createDB.dropDB('db_use070')
        self.assertEqual(drop, 0)
    def test_db_071(self):
        '''
        win:use 带路径，路径使用\转义并带引号,query ok
        '''
        sql = 'create db @"E:/rtdb_test/db_use071"'
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0)
        # use
        sql = "use 'E:\\\\rtdb_test\\\\db_use071'"
        use = createDB.createSql(None, sql)
        self.assertTrue(use == 0, msg='use error')
        currentDB = createDB.currentDB()
        self.assertTrue(currentDB == 'db_use071', msg='use error')
        drop = createDB.dropDB('db_use071')
        self.assertEqual(drop, 0)
    def test_db_072(self):
        '''
        win : use 带路径，路径单\，前面有@,query ok
        '''
        sql = 'create db @"E:/rtdb_test/db_use072"'
        res = createDB.createSql(None, sql)
        self.assertEqual(res ,0 )
        # use
        usql = 'use @"E:\\rtdb_test\db_use072"'
        use = createDB.createSql(None, usql)
        self.assertTrue(use == 0, msg='use error')
        currentDB = createDB.currentDB()
        self.assertTrue(currentDB == 'db_use072', msg='use error')
        drop = createDB.dropDB('db_use072')
        self.assertEqual(drop , 0)
    def test_db_073(self):
        '''
        win平台：use 带路径的库，路径是单/并带引号，query ok
        '''
        sql = 'create db @"E:/rtdb_test/db_use073"'
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0)
        # use
        usql = "use 'E:/rtdb_test/db_use073'"
        use = createDB.createSql(None, usql)
        self.assertTrue(use == 0, msg='use error')
        currentDB = createDB.currentDB()
        self.assertTrue(currentDB == 'db_use073', msg='use error')
        drop = createDB.dropDB('db_use073')
        self.assertEqual(drop, 0)
    def test_db_074(self):
        '''
        win平台：use 带路径的库,路径是两个//并带引号, query ok
        '''
        sql = 'create db @"E:/rtdb_test/db_use074"'
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0)
        # use
        usql = "use 'E://rtdb_test//db_use074'"
        use = createDB.createSql(None, usql)
        self.assertTrue(use != 0, msg='use error')

        drop = createDB.dropDB('db_use074')
        self.assertEqual(drop, 0)

    def test_db_075(self):
        '''
        先use 一个库，show tb ,然后去关掉服务，重新开启服务，执行show tb
        试着用自动化执行一下看看, 如果不行，就手动执行此用例
        '''
        # dbName = 'testdb075'
        # res = createDB.createSql(dbName)
        # self.assertEqual(res ,0 ,msg='创建数据库')
        # usql = 'use testdb075'
        # use = createDB.createSql(None,usql)
        # self.assertEqual(use, 0, msg='use数据库')
        # currentDB = createDB.currentDB()
        # self.assertEqual(currentDB, 'testdb075', msg='use数据库')
        # #关闭服务  这个地方需要输入密码，怎么处理？？
        # stop = createDB.createSql(None ,'sudo service rtdb_svr stop')

    def test_db_076(self):
        '''
        win平台：use 打开使用带@符号的路径,query ok
        '''
        sql = 'create db @"E:/rtdb_test/db_use076"'
        res = createDB.createSql(None, sql)
        self.assertEqual(res, 0,msg='createdb fail')

        usql = "use @'E:\\rtdb_test\db_use076'"
        use = createDB.createSql(None, usql)
        self.assertTrue(use == 0, msg='use error')
        currentDB = createDB.currentDB()
        self.assertTrue(currentDB == 'db_use076', msg='currentDB use error')
        drop = createDB.dropDB('db_use076')
        self.assertEqual(drop, 0)
    def test_db_077(self):
        '''
        win平台：use 一个不存在的路径,query fail
        '''
        sql = "use 'E:\\rtdb_test\\db_use077'"
        use = createDB.createSql(None, sql)
        self.assertTrue(use != 0, msg='use error')

@unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
class Test_db_use_linux(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        sql = "create db '/var/lib/RTDB/rtdb/DATABASES/db_use'"
        res = createDB.createSql(None,sql)
        cls().assertEqual(res ,0 ,msg='初始化创建数据库')
    @classmethod
    def tearDownClass(cls) -> None:
        drop = createDB.dropDB('db_use')
        cls().assertEqual(drop , 0 ,msg='删除初始化时创建的库')
    def test_db_078(self):
        '''
        Linux：use @'/var/lib/RTDB/rtdb/DATABASES/顺实科技'
        '''
        sql = "create db @'/var/lib/RTDB/rtdb/DATABASES/顺实科技'"
        cRes = createDB.createSql(None,sql)
        self.assertEqual(cRes , 0 ,msg='创建成功')
        usql = "use @'/var/lib/RTDB/rtdb/DATABASES/顺实科技'"
        use = createDB.createSql(None, usql)
        self.assertTrue(use == 0, msg='use error')
        currentDB = conn.get_db_current()
        self.assertTrue(currentDB == '顺实科技', msg='use error')
        drop = createDB.dropDB('顺实科技')
        self.assertEqual(drop , 0,msg='删除创建的数据库')

    def test_db_079(self):
        '''
        Linux：use '\\usr\\bin\\rtdb\\db_use'  ,query fail
        '''
        usql = "use '\\usr\\bin\\rtdb\\db_use'"
        use = createDB.createSql(None, usql)
        self.assertTrue(use != 0, msg='use error')
        # currentDB = createDB.currentDB()
        # print(currentDB)
        # self.assertTrue(currentDB == 'db_use', msg='use error')
    def test_db_080(self):
        '''
        Linux:use '\\rtdbtest\\testdb080' ,query ok
        '''
        csql = 'create db @"\\rtdbtest\\testdb080"'

        res = createDB.createSql(None,csql)
        self.assertEqual(res ,0 ,msg='创建数据库')
        usql = "use '\\\\rtdbtest\\\\testdb080'"
        use = createDB.createSql(None, usql)
        self.assertTrue(use == 0, msg='use error')
        currentDB = conn.get_db_current()
        self.assertTrue(currentDB == 'testdb080', msg='use error')
        drop = createDB.dropDB('testdb080')
        self.assertEqual(drop , 0,msg='删除创建的数据库')
    def test_db_081(self):
        '''
        Linux: use '/var/lib/RTDB/rtdb/DATABASES/时序库'  ,query ok
        '''
        dbName = '时序库'
        res = createDB.createSql(dbName)
        self.assertEqual(res, 0, msg='创建数据库')
        #这里应该先获取当前的datadir是什么地址
        show =  createDB.showVar()
        datadir = show[0]['value']

        usql = "use '"+datadir+"时序库'"

        use = createDB.createSql(None, usql)
        self.assertTrue(use == 0, msg='use error')
        currentDB = conn.get_db_current()
        self.assertTrue(currentDB == '时序库', msg='use error')
        drop = createDB.dropDB('时序库')
        self.assertEqual(drop, 0, msg='删除创建的数据库')
    def test_db_082(self):
        '''
        Linux: use /var/lib/RTDB/rtdb/DATABASES/testdb082  ,query fail
        '''
        dbName = 'testdb082'
        res = createDB.createSql(dbName)
        self.assertEqual(res ,0  ,msg='创建数据库')
        show =  createDB.showVar()
        datadir = show[0]['value']
        usql = "use "+datadir+""+dbName+""
        # usql = 'use /var/lib/RTDB/rtdb/DATABASES/testdb082'
        use = createDB.createSql(None,usql)
        self.assertTrue(use !=0 , msg='use 失败')
        drop = createDB.dropDB('testdb082')
        self.assertEqual(drop, 0, msg='删除创建的数据库')
    def test_db_083(self):
        '''
        Linux:  先在默认目录建一个testdb083的库，然后执行use '/testdb083'，query fail
        '''
        dbName = 'testdb083'
        res = createDB.createSql(dbName)
        self.assertEqual(res, 0, msg='创建数据库')
        usql = "use '/testdb083'"
        use = createDB.createSql(None, usql)
        self.assertTrue(use != 0, msg='use 失败')
        drop = createDB.dropDB('testdb083')
        self.assertEqual(drop, 0, msg='删除创建的数据库')

    def test_db_084(self):
        '''
        Linux:先创建一个库testdb084，并use testdb084库创建表test001 ，
        然后use '/testdb084',query fail
        '''
        dbName = 'testdb084'
        res = createDB.createSql(dbName)
        self.assertEqual(res, 0, msg='创建数据库')
        usql = "use testdb084"
        use = createDB.createSql(None, usql)
        self.assertTrue(use == 0, msg='use 失败')
        currentDB = createDB.currentDB()
        self.assertTrue(currentDB == 'testdb084', msg='use error')
        tableSql = 'create table test001(f1 int,f2 int);'
        table = createDB.createSql(None, tableSql)
        self.assertEqual(table, 0)
        insert = createDB.createSql(None, 'insert into test001(f1,f2) values(1,2)')
        self.assertEqual(insert, 0)
        usql2 = "use '/testdb084'"
        use2 = createDB.createSql(None,usql2)
        self.assertNotEqual(use2 , 0, msg="use '/testdb084'应该失败")
        drop = createDB.dropDB('testdb084')
        self.assertEqual(drop, 0, msg='删除创建的数据库')





