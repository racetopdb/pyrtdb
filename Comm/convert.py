# -*- coding: utf-8 -*-
import time
import datetime



class Convert:

    '''
    时间戳转换成日期格式
    返回格式：年-月-日 时:分:秒.毫秒(3位)
    '''
    def get_date_stamp(self,timestamp=None):
        if timestamp is not None:
            k = len(str(timestamp)) - 10
            times = datetime.datetime.fromtimestamp(timestamp / (1 * 10 ** k))
            date_stamp = times.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        else:
            ct = time.time()
            local_time = time.localtime(ct)
            data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            data_secs = (ct - int(ct)) * 1000
            date_stamp = "%s.%03d" % (data_head, data_secs)
        #date_stamp是： 2022-07-07 11:16:13.120
        return date_stamp

    '''
    把日期（年-月-日 时：分：秒）转成时间戳
    返回格式：1483434550000
    '''
    def get_times_stamp(self,dates =None):
        if dates is None:
            dates = datetime.datetime.now()
        times = time.mktime(time.strptime(str(dates), '%Y-%m-%d %H:%M:%S'))
        return times * 1000

convert = Convert()