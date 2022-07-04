# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *


class createDB:
    def __init__(self):
        self.cSql = 'create db if not exist'
    def createSql(self,dbName=None,sql=None):

        if sql is not None :
            print(sql)
            cRes = conn.query(sql)
        else:
            # if dbName is None : return 'dbname is null'
            print(''+self.cSql+' '+dbName+'')
            cRes = conn.query(''+self.cSql+' '+dbName+'')
        return cRes
    def currentDB(self):
        db = conn.get_db_current()
        return db
    def checkRes(self):
        retDict = {}
        show = conn.query_reader('show db')
        while show.cursor_next() == 0:
            name = show.get_string(0)
            path = show.get_string(6)
            retDict['name'] = name
            retDict['path'] = path
        return retDict
    def useDB(self,dbName):
        ret = conn.query('use '+dbName+';')
        return ret

    def rowNum(self):
        show = conn.query_reader('show db')
        rows = show.get_row_count()
        return rows
    def dropDB(self,dbName):
        dRes = 'dbName is null'
        if dbName is not None:
            print('drop db '+dbName+'')
            dRes = conn.query_reader('drop db '+dbName+'')
        return dRes
    # def rtdbSer(self,opt='start'):
    #     conn.query('')

createDB = createDB()
