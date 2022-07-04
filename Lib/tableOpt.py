# -*- coding: utf-8 -*-
import unittest
from Comm.pyrtdb import conn
from time import sleep
from Conf.config import *

class tableOpt:
    #fieldType 是 {字段名：类型} 字典类型
    def createTb(self,tableName =None,fieldType ={},sql = None):
        res = ''
        if sql is None:
            sql = 'create table '+tableName+' ('
            for key,val in fieldType.items():
                sql +=key +' '
                sql +=val + ','
            sql = sql + ')'
        # print(sql)
        res = conn.query(sql)
        return res
    def insertTb(self,tbName=None,fields=[],vals=[],insertSql=None):
        # if tbName is None:
        #     return '表名不能为空'
        sql = 'insert into '+str(tbName)

        if insertSql is not None:
            # print(insertSql)
            res = conn.query(insertSql)
        else:
            if len(fields) ==0:
                sql +=' values('
                for val in vals:
                    val = str(val)
                    sql +='"'+val+'",'
                sql +=')'
            else :
                sql +='('
                for fd in fields:
                    fd =str(fd)
                    sql +=''+fd+','
                sql +=')'
                sql +=' values('
                for v in vals:
                    v = str(v)
                    sql +='"'+v+'",'
                sql +=')'

            # print(sql)
        res = conn.query(sql)
        return res
    def describeTb(self,tb):
        ret = {}
        nameList = []
        typeList = []
        lenList = []
        isList = []
        des = conn.query_reader('describe table ' +str(tb))

        while des.cursor_next() == 0:
            name = des.get_string(0)
            nameList.append(name)
            type = des.get_string(1)
            typeList.append(type)
            lens = des.get_int(2)
            lenList.append(lens)
            isnull = des.get_bool(3)
            isList.append(isnull)
        ret = {
                'name':nameList,
                'type':typeList,
                'lens':lenList,
                'isList':isList
               }
        return ret

    def showTable(self,ret=0):
        retDict = {}
        show = conn.query_reader('show tb')
        while show.cursor_next() == 0:
            id = show.get_int(0)
            name = show.get_string(1)
            field = show.get_int(2)
            row = show.get_int(3)
            first_time = show.get_datetime_ms(4)
            last_time = show.get_datetime_ms(5)
            if ret ==0:
                retDict = {
                        'name':name,
                        'field':field,
                        'row':row,
                        'first_time':first_time,
                        'last_time':last_time
                        }
            else:
                retDict[id] = {
                    'name': name,
                    'field': field,
                    'row': row,
                    'first_time': first_time,
                    'last_time': last_time
                }

        return retDict
    def dropTb(self,tb,sql=None):
        if sql is not None:
            dRes = conn.query_reader(sql)
        else:
            dRes = conn.query_reader('drop tb ' + tb + '')
        return dRes
    def tbRowNum(self):

        show = conn.query_reader('show tb')
        row = show.get_row_count()
        return row

tableOpt =  tableOpt()
# tableOpt.insertTb('test_001',[],['2022-06-27 10:00:01',1,2])  #如果不加time字段 ，必须得有time值
# tableOpt.insertTb('test_001',['time','f1','f2'],['2022-06-27 10:00:01',1,2])
# tableOpt.insertTb(None,[],[],"insert into test_001(f1,f2) values(2,3)")