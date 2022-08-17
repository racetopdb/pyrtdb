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
            cRes = conn.query(sql)
        else:
            cRes = conn.query(''+self.cSql+' '+dbName+'')
        return cRes
    def currentDB(self):
        db = conn.get_db_current()
        return db
    def checkRes(self,key=0):
        retDict = {}
        show = conn.query_reader('show db')
        i = 0
        while show.cursor_next() == 0:
            name = show.get_string(0)
            path = show.get_string(7)
            if key !=0:
                retDict[i] ={'name':name,'path':path}

            else:
                retDict['name'] = name
                retDict['path'] = path
            i +=1

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
            dRes = conn.query('drop db '+dbName+'')
        return dRes
    def showVar(self,sql=None):
        if sql is not None:
            res = conn.query_reader(sql)
        else:
            res = conn.query_reader('show variables')
        # rc = res.get_row_count()
        i = 0
        ret = {}
        while 0 == res.cursor_next():
            name = res.get_string(0)
            value = res.get_string(1)
            readonly = res.get_bool(2)
            ret[i] ={
                'name':name,
                'value':value,
                'readonly':readonly
            }
            i += 1
        return  ret

createDB = createDB()
