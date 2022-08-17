# -*- coding: utf-8 -*-

from TestCases.dbManage.setupModule import *

logger = logging.getLogger('main.Test_db3')

@unittest.skip('执行大批量时，跳过此用例')
class Test_db_sample(unittest.TestCase):
    def test_db_sample(self):
        res = conn.query('show db')
        print(res)


