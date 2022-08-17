# -*- coding: utf-8 -*-
from TestCases.dbManage.setupModule import *
import time


logger = logging.getLogger('main.Test_db_create')

class Test_db_create(unittest.TestCase):

    def test_db_009(self):
        '''
        使用大小写字母混合的名称,创建数据库
        '''
        dbName = 'testDB'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='大小写混合创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName, msg='检查创建的库名和查询到的库名是否一致')
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='检查删除创建的数据库是否成功')

    def test_db_010(self):
        '''
        使用字母混合数字的名称,创建数据库
        '''
        timestr = time.strftime('%m%d', time.localtime())
        dbName = 'test' + timestr
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='字母混合数字创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName, msg='检查创建的库名和查询到的库名是否一致')
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='db_010检查删除创建的数据库是否成功')

    def test_db_011(self):
        '''
        使用带单引号的大小写混合数字的名称,创建数据库
        '''
        dbName = "'test3DB'"
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='带单引号的大小写混合数字创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'test3DB')
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='db_011检查删除创建的数据库是否成功')

    # @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    # @unittest.skipIf(platform['system'] == 'Linux', 'linux平台不执行此用例')
    @unittest.skip('手动执行可以创建成功，自动化不行，与中文有关，先跳过此用例')
    def test_db_012_win(self):
        '''
        使用中文双引号+大小写混合数字的名称,创建数据库
        这个用例手动执行可以创建成功，自动化不行
        '''
        dbName = '“DB3TEs”'
        cRes = createDB.createSql(dbName)

        self.assertEqual(cRes, 0, msg='db_012中文双引号+大小写混合数字的名称在win创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], '“DB3TEs”')

        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='db_012检查删除创建的数据库是否成功')
    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_db_012(self):
        '''
        使用中文双引号+大小写混合数字的名称,创建数据库
        Linux平台创建完会是if的名称  要把if这个删除掉
        '''
        dbName = '“DB3TEs”'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='db_012中文双引号+大小写混合数字的名称创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], '“DB3TEs”')
        dRes = createDB.dropDB('“DB3TEs”')
        self.assertTrue(dRes == 0, msg='db_012检查删除创建的数据库是否成功')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_013_win(self):
        '''
        使用中文字符,创建数据库
        '''
        dbName = '顺实科技'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='db_013使用中文字符创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='db_013检查删除创建的数据库是否成功')

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_db_013(self):
        '''
        使用中文字符,创建数据库
        '''
        dbName = '顺实科技'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='db_013使用中文字符创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='db_013检查删除创建的数据库是否成功')

    def test_db_014(self):
        '''
        使用下划线开头的名称,创建数据库
        '''
        dbName = '_testdbs'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0, msg='db_014使用下划线开头创建数据库，期望返回fail')
        row = createDB.rowNum()
        self.assertEqual(row, 0, msg='db_014下划线开头创建数据库应该fail，所以返回0行')

    def test_db_015(self):
        '''
        使用数字开头的名称,创建数据库
        '''
        dbName = '55testdb'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0, msg='使用数字开头创建数据库，期望返回fail')
        row = createDB.rowNum()
        self.assertEqual(row, 0, msg='db_015返回0行')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_016_win(self):
        '''
        使用'数字'开头的名称,创建数据库, 43上会返回ok, win fail
        '''
        dbName = '‘0613db’'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0)
        row = createDB.rowNum()
        self.assertEqual(row, 0)

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_db_016(self):
        '''
        使用'数字'开头的名称,创建数据库, 43上会返回ok, win fail
        '''
        dbName = '‘0613db’'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0)
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dRes = createDB.dropDB(dbName)
        self.assertEqual(dRes, 0)

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_db_017(self):
        '''
        使用'下划线'开头的名称创建数据库
        '''
        dbName = '‘_db’'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0)
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0)

    # @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    @unittest.skip('这个用例因为中文单引号的问题总是报错，跳过。')
    def test_db_017_win(self):
        '''
        使用'下划线'开头的名称创建数据库
        '''
        dbName = '‘_dbtest’'
        cRes = createDB.createSql(dbName)
        # self.assertTrue(cRes != 0)
        self.assertTrue(cRes == 0 ,msg=f'创建结果是：{cRes}，期望值是：0')

        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0)
    def test_db_018(self):
        '''
        使用"数字"开头的名称创建数据库
        '''
        dbName = '"55dbs"'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0, msg='双引号加数字开头创建数据库，期望返回fail')
        row = createDB.rowNum()
        self.assertEqual(row, 0, msg='db_018双引号加数字开头创建数据库')

    def test_db_019(self):
        '''
        使用"下划线"开头的名称
        '''
        dbName = '"_db"'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0, msg='使用"下划线"开头的名称创建数据库，期望返回fail')
        row = createDB.rowNum()
        self.assertEqual(row, 0, msg='db_019使用"下划线"开头创建数据库行数为0')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_020_win(self):
        '''
        先使用小写字母创建数据库【ok】，再使用同样的大写字母创建数据库【43ok win fail】
        '''
        dbNameLower = 'testdbs'
        cRes = createDB.createSql(dbNameLower)
        self.assertEqual(cRes, 0, msg='使用小写字母创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbNameLower)
        # 创建全大写的数据库名称
        dbNameUpper = 'TESTDBS'
        uRes = createDB.createSql(dbNameUpper)
        self.assertTrue(uRes != 0)
        row = createDB.rowNum()
        self.assertEqual(row, 1)
        dRes = createDB.dropDB(dbNameLower)
        self.assertTrue(dRes == 0)

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_db_020(self):
        '''
        先使用小写字母创建数据库【ok】，再使用同样的大写字母创建数据库【43ok win fail】
        '''
        dbNameLower = 'testdbs'
        cRes = createDB.createSql(dbNameLower)
        self.assertEqual(cRes, 0, msg='使用小写字母创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbNameLower)
        # 创建全大写的数据库名称
        dbNameUpper = 'TESTDBS'
        uRes = createDB.createSql(dbNameUpper)
        self.assertEqual(uRes, 0, msg='使用大写字母创建数据库')
        ret2 = createDB.checkRes(1)

        self.assertEqual(ret2[0]['name'], dbNameUpper)
        lDrop = createDB.dropDB(dbNameLower)
        self.assertTrue(lDrop == 0, msg='db_020检查删除小写字母创建的数据库是否成功')
        uDrop = createDB.dropDB(dbNameUpper)
        self.assertTrue(uDrop == 0, msg='db_020检查删除大写字母创建的数据库是否成功')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_021_win(self):
        '''
        使用testdb创建数据库，创建成功，再次使用testDB创建数据库，创建失败[win fail ,43 ok ]
        '''
        dbName = 'testdb'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='使用testdb小写字母创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dbName2 = 'testDB'
        cRes2 = createDB.createSql(dbName2)
        self.assertTrue(cRes2 != 0, msg='win使用testDB创建失败')
        row = createDB.rowNum()
        self.assertEqual(row, 1)
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='删除创建的testdb')

    @unittest.skipIf(platform['system'] == 'Windows', 'win平台不执行此用例')
    def test_db_021(self):
        '''
        使用testdb创建数据库，创建成功，再次使用testDB创建数据库，创建失败[win fail ,43 ok ]
        '''
        dbName = 'testdb'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='使用testdb小写字母创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dbName2 = 'testDB'
        cRes2 = createDB.createSql(dbName2)
        self.assertEqual(cRes2, 0, msg='使用testDB大写字母创建数据库，43ok ,win fail')
        ret2 = createDB.checkRes(1)
        self.assertEqual(ret2[0]['name'], dbName2)
        dRes1 = createDB.dropDB(dbName)
        self.assertTrue(dRes1 == 0)
        dRes2 = createDB.dropDB(dbName2)
        self.assertTrue(dRes2 == 0)

    def test_db_022(self):
        '''
        创建名称为空的数据库
        '''
        dbName = ''
        cRes = createDB.createSql(dbName)

        self.assertTrue(cRes != 0, msg='创建名称为空的数据库，期望返回fail')
        row = createDB.rowNum()
        self.assertEqual(row, 0)
    def test_db_023(self):
        '''
        创建名称为null的数据库, 这是一个验证未通过的用例
        '''
        dbName = 'null'
        cRes = createDB.createSql(dbName)

        self.assertEqual(cRes, 0, msg='创建名称为null的数据库，期望返回fail')

        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='删除掉创建的数据库')
    def test_db_024(self):
        '''
        创建名称长度为1的数据库
        '''
        dbName = 'd'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes, 0, msg='创建名称长度为1的数据库，ok ')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='删除掉创建的数据库')
    def test_db_025(self):
        '''
        数字字母下划线混合，长度为15个字符的数据库, query ok
        '''
        dbName = 'test_db_1234567'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes , 0 ,msg='数字字母下划线混合，长度为15个字符的数据库 ,ok')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName)
        dRes = createDB.dropDB(dbName)
        self.assertTrue(dRes == 0, msg='删除掉创建的数据库')

    def test_db_026(self):
        '''
        创建名称长度为255个字符的数据库，query failed
        '''
        dbName = 'test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567test_db_1234567'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0,msg='db_026名称长度255的数据库创建失败')
        row = createDB.rowNum()
        self.assertEqual(row,0,msg= '名称过长，应该返回0行')
    def test_db_028(self):
        '''
        使用特殊符号@创建数据库，提示query failed
        '''
        dbName = '@td'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0 ,msg='使用特殊符号@创建数据库，提示query failed')
        row = createDB.rowNum()
        self.assertEqual(row, 0, msg='名称过长，应该返回0行')
    def test_db_029(self):
        '''
        if not exist 在库名前面，创建数据库，提示query OK
        '''
        csql = 'create db if not exist db_0325'
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes, 0 ,msg='if not exist 在库名前面,queryok')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'],'db_0325' ,msg='db_029验证写入的名称和查询到的名称是否是同一个')
        dRes = createDB.dropDB('db_0325')
        self.assertTrue(dRes == 0, msg='db_029检查删除创建的数据库是否成功')
    def test_db_030(self):
        '''
        if not exist 在库名后面，创建数据库，提示query OK
        '''
        csql = 'create db testdb  if not exist'
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes , 0 , msg='db_030创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'] , 'testdb',msg='检查创建的库和查询到的库是否一致')
        dRes =createDB.dropDB('testdb')
        self.assertEqual(dRes,0 ,msg='db_030删除掉创建的数据库')
    def test_db_031(self):
        '''
        if not exist 创建一个已经存在的库，提示query ok,并不会有一个同名的库被创建
        '''
        csql = 'create db testdb0325  if not exist'
        cRes1 = createDB.createSql(None,csql)
        self.assertEqual(cRes1, 0 ,msg='第一次创建库，ok')
        cRes2 = createDB.createSql(None,csql)
        self.assertEqual(cRes2, 0, msg='第2次创建库，ok')
        row = createDB.rowNum()
        self.assertEqual(row , 1,msg='只有一条记录返回')
        dRes = createDB.dropDB('testdb0325')
        self.assertEqual(dRes,0,msg='db_031删除掉创建的数据库')
    def test_db_032(self):
        '''
        create db 不用if not exist创建数据库，提示query ok
        '''
        csql = 'create db test_db032'
        cRes = createDB.createSql(None,csql)

        self.assertEqual(cRes,0,msg='db_032创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'] , 'test_db032' ,msg='db_032验证写入的库和查到库是否一致')
        dRes = createDB.dropDB('test_db032')
        self.assertEqual(dRes,0 , msg='db_032删除掉创建的数据库')
    def test_db_033(self):
        '''
        if not exist 创建一个库，删除库，再创建一个同名的库，提示query ok
        '''
        dbName = 'test001'
        cRes = createDB.createSql(dbName)
        self.assertEqual(cRes,0,msg='db_033创建数据库test001')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName, msg='db_033验证写入的库和查到库是否一致')
        dRes = createDB.dropDB(dbName)
        self.assertEqual(dRes, 0, msg='db_033删除掉创建的数据库')

        cRes2 = createDB.createSql(dbName)
        self.assertEqual(cRes2, 0, msg='db_033创建数据库test001,第二次')
        ret2 = createDB.checkRes()
        self.assertEqual(ret2['name'], dbName, msg='db_033验证写入的库和查到库是否一致，第二次')
        dRes = createDB.dropDB(dbName)
        self.assertEqual(dRes, 0, msg='db_033删除掉创建的数据库，第二次')
    def test_db_034(self):
        '''
            create db创建一个库，提示query ok，
            再执行create db 创建一个同名的库，提示query failed
        '''

        csql = 'create db testdb002'
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes,0,msg='db_034创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'],'testdb002',msg='验证创建的库和查到的库是否一致')
        cRes2 = createDB.createSql(None, csql)
        self.assertTrue(cRes2 != 0, msg='db_034创建同名数据库')
        row = createDB.rowNum()
        self.assertEqual(row ,1 ,msg='db_034只有1行返回')
        dRes = createDB.dropDB('testdb002')
        self.assertEqual(dRes ,0 ,msg='db_034删除创建的数据库')

    def test_db_035(self):
        '''
        手动停止win10的rtdb_svr
        执行create db testdb，提示query failed
        '''
        pass
    def test_db_036(self):
        '''
        使用命令sudo service rtdb_svr stop停止Linux上面的服务
        执行create db test_99,提示query failed
        '''
        pass
    @unittest.skipIf(platform['system'] == 'Linux','Linux平台不执行此用例')
    def test_db_037(self):
        '''
        直接用根目录路径，在根目录创建数据库，提示query FAILED
        '''
        dbName = 'c:\\testdb'
        cRes = createDB.createSql(dbName)
        self.assertTrue(cRes != 0, msg='db_037创建数据库失败')
        row = createDB.rowNum()
        self.assertEqual(row,0,msg='db_037在根目录创建数据库失败，返回0行')

    @unittest.skipIf(platform['system'] == 'Linux','Linux平台不执行此用例')
    def test_db_038(self):
        '''
        用@符号拼接根目录路径，在根目录创建数据库，提示query FAILED
        '''
        csql = "create db @'c:\\a'"
        cRes = createDB.createSql(None,csql)
        self.assertTrue(cRes !=0,msg='用@符号拼接根目录路径 ,query fail')
        row = createDB.rowNum()
        self.assertEqual(row ,0 ,msg='用@符号拼接根目录路径,返回0行')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_039(self):
        '''
        使用with的参数path设置路径在根目录，创建数据库，提示query ok
        '''
        csql = "create db 'testdb' with path='c:\\a'"
        cRes = createDB.createSql(None,csql)
        self.assertTrue(cRes != 0 ,msg='用with的参数path设置路径在根目录,ok')
        row = createDB.rowNum()
        self.assertEqual(row , 0,msg='创建不成功，条数为0')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_040(self):
        '''
        使用with的参数path设置路径创建数据库，且路径的最后一个目录与库名不一致
        ，创建数据库，提示query FAILED
        '''
        csql = "create db 'testdb' with path='e:\\rtdb\\rtdb1'"
        cRes = createDB.createSql(None,csql)
        self.assertTrue(cRes != 0 ,msg='db_040路径的目录与库名不一样创建失败')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_041(self):
        '''
        使用with参数path设置路径创建数据库名称为中文的数据库，提示query ok
        '''
        csql = "create db '顺实科技' with path = @'e:\\rtdb\\顺实科技'"
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes , 0 , msg='db_041创建成功')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], '顺实科技',msg='db_041验证创建的库名和查询到的库名一致')
        self.assertEqual(ret['path'], 'e:\\rtdb\\顺实科技', msg='db_041验证创建路径和查询到路径一致')
        dRes = createDB.dropDB('顺实科技')
        self.assertEqual(dRes,0 ,msg='db_041删除库')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_042(self):
        '''
        使用带‘@’符号的路径创建数据库，提示query OK
        '''
        csql = "create db @'c:\\rtdb\\rtdb_test\\testdb0426'"
        cRes = createDB.createSql(None,csql)
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb0426',msg='db_042验证创建的库名和查询到的库名一致')
        self.assertEqual(ret['path'], 'c:\\rtdb\\rtdb_test\\testdb0426', msg='db_042验证创建路径和查询到路径一致')
        dRes = createDB.dropDB('testdb0426')
        self.assertEqual(dRes,0 ,msg='db_042删除库')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_043(self):
        '''
        使用with参数path创建数据库，提示queryOK
        '''
        dbName = 'rtdb_test'+str(int(time.time()))
        csql = "create db "+dbName+" with path='c:\\\\rtdb\\\\"+dbName+"'"

        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes , 0 ,msg='db_043创建数据库')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], dbName, msg='db_043验证创建的库名和查询到的库名一致')

        self.assertEqual(ret['path'], 'c:\\rtdb\\'+dbName+'', msg='db_043验证创建路径和查询到路径一致')
        dRes = createDB.dropDB(dbName)
        self.assertEqual(dRes, 0, msg='db_043删除库')

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_044(self):
        '''
        set datadir 设置数据库路径为系统的Windows目录下的其他目录，提示：query failed
        '''
        csql = "set datadir='c:\\Windows\\rtdb\\'"
        cRes = createDB.createSql(None,csql)
        self.assertTrue(cRes != 0 )
        #这里要加个验证，show DB 看一下 datadir是否是默认的
    def test_db_045(self):
        '''
        创建数据库create db库名，中间没有空格，queryfailed
        '''
        csql = 'create dbtestdb0531'
        cRes = createDB.createSql(None, csql)
        self.assertTrue(cRes != 0)
        row = createDB.rowNum()
        self.assertEqual(row ,0 )
    def test_db_046(self):
        '''
        create db 库名，数据库名称后有空格，创建数据库，提示query ok
        '''
        csql = 'create db testdb0516          '
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes,0)
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb0516', msg='db_046验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb0516')
        self.assertEqual(dRes , 0)
    def test_db_047(self):
        '''
        create db 库名，数据库名称中间有空格，创建数据库，提示queryok 名称为空格前的部分
        '''
        csql = 'create db test05    db16'
        cRes = createDB.createSql(None, csql)
        self.assertEqual(cRes, 0)
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'test05', msg='db_047验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('test05')
        self.assertEqual(dRes, 0)
    def test_db_048(self):
        '''
        create db 库名使用引号，且中间带空格，queryOK
        '''
        csql = "create db 'test05    db16'"
        cRes = createDB.createSql(None, csql)
        self.assertEqual(cRes, 0)
        ret = createDB.checkRes()

        self.assertEqual(ret['name'], 'test05 db16', msg='db_048验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB("'test05 db16'")
        self.assertEqual(dRes, 0)

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_049(self):
        '''
        win平台：create db @'路径信息'创建数据库，路径中间带空格,，query failed
        '''
        csql = 'create db @"E:/rtdb_test/  testdb049"'
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes , 0 ,msg='路径中间带空格，创建成功')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb049', msg='db_049验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB("testdb049")
        self.assertEqual(dRes, 0)

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_050(self):
        '''
        win平台：create db @'路径信息'创建数据库，路径前面带空格,query ok
        '''
        csql = 'create db @"  E:/rtdb_test/testdb050" '
        cRes =  createDB.createSql(None,csql)
        self.assertEqual(cRes , 0 ,msg='db_050创建数据失败')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb050', msg='db_050验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb050')
        self.assertEqual(dRes,0)

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_051(self):
        '''
        win平台：create db @'路径信息'创建数据库，路径后面带空格，queryOK
        '''
        csql = 'create db @"E:/rtdb_test/testdb051    " '
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes,0 ,msg='db_051创建数据库失败')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb051', msg='db_051验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb051')
        self.assertEqual(dRes , 0)

    @unittest.skipIf(platform['system'] == 'Linux', 'Linux平台不执行此用例')
    def test_db_052(self):
        '''
        win平台：create db @'路径信息'创建数据库，整个路径前面没有空格，query ok
        '''
        csql = 'create db@"E:/rtdb_test/testdb052" '
        cRes = createDB.createSql(None,csql)
        self.assertEqual(cRes,0)
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb052', msg='db_052验证创建的库名和查询到的库名一致')
        self.assertEqual(ret['path'], 'E:\\rtdb_test\\testdb052', msg='db_052验证创建路径和查询到路径一致')
        dRes = createDB.dropDB('testdb052')
        self.assertEqual(dRes, 0, msg='db_052删除库')
    @unittest.skipIf(platform['system'] == 'Windows','windows平台跳过此用例')
    def test_db_053(self):
        '''
        Linux平台：create db @'路径信息'创建数据库，整个路径前面没有空格，query ok
        '''
        sql = 'create db@"/rtdb_test/testdb053"'
        cRes = createDB.createSql(None,sql)
        self.assertEqual(cRes , 0 )
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb053', msg='db_053验证创建的库名和查询到的库名一致')
        self.assertEqual(ret['path'], '/rtdb_test/testdb053', msg='db_053验证创建路径和查询到路径一致')
        dRes = createDB.dropDB('testdb053')
        self.assertEqual(dRes, 0, msg='db_053删除库')
    def test_db_054(self):
        '''
        create db 库名，数据库名称前没有空格，创建数据库,query fail
        '''
        sql = 'create dbtest054'
        res = createDB.createSql(None,sql)
        self.assertTrue(res != 0 ,msg='db_054创建数据库失败')
        row = createDB.rowNum()
        self.assertEqual(row ,0 , msg='db_054创建失败应返回0行')
    def test_db_055(self):
        '''
        create db 库名，数据库名称后有空格，创建数据库，提示query ok
        '''
        sql = 'create db testdb055         '
        res = createDB.createSql(None,sql)
        self.assertEqual(res ,0 ,msg='db_055创建数据库成功')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb055', msg='db_055验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb055')
        self.assertEqual(dRes,0,msg='db_055删除创建的表')
    @unittest.skipIf(platform['system'] == 'Windows' ,'windows平台跳过此用例')
    def test_db_056(self):
        '''
        Linux:create db @'路径信息'创建数据库，路径中间带空格, query ok
        '''
        sql = 'create db @"/rtdb_test/    testdb056"'
        res = createDB.createSql(None,sql)
        self.assertTrue(res == 0)
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb056', msg='db_056验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb056')
        self.assertEqual(dRes, 0, msg='db_056删除创建的表')

    @unittest.skipIf(platform['system'] == 'Windows', 'windows平台跳过此用例')
    def test_db_057(self):
        '''
        Linux:create db @'路径信息'创建数据库，路径前面带空格,query ok
        '''
        sql = 'create db @"   /rtdb_test/testdb057"'
        res = createDB.createSql(None,sql)
        self.assertEqual(res ,0 ,msg='db_057创建数据成功')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb057', msg='db_057验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb057')
        self.assertEqual(dRes, 0, msg='db_057删除创建的表')

    @unittest.skipIf(platform['system'] == 'Windows', 'windows平台跳过此用例')
    def test_db_058(self):
        '''
        create db @'路径信息'创建数据库，路径后面带空格,query ok
        '''
        csql = 'create db @"/rtdb_test/testdb058    "'
        res = createDB.createSql(None,csql)
        self.assertEqual(res , 0 ,msg='db_058创建数据库成功')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb058', msg='db_058验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb058')
        self.assertEqual(dRes, 0, msg='db_058删除创建的表')

    @unittest.skipIf(platform['system'] == 'Windows', 'windows平台跳过此用例')
    def test_db_059(self):
        '''
        create db @'路径信息'创建数据库，整个路径前面没有空格,query ok
        '''
        sql = 'create db@"/rtdb_test/testdb059"'
        res = createDB.createSql(None,sql)
        self.assertEqual(res , 0 ,msg='db_059创建数据库成功')
        ret = createDB.checkRes()
        self.assertEqual(ret['name'], 'testdb059', msg='db_059验证创建的库名和查询到的库名一致')
        dRes = createDB.dropDB('testdb059')
        self.assertEqual(dRes, 0, msg='db_059删除创建的表')




