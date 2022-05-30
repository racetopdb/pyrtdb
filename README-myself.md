# RtdbClient
提供rtdb的python语言的客户端实现

# 设计要求
返回第一行信息为字段信息，设计Field类型与数据库类型一一对应
可参照django的元编程类型设计
从第二行开始，返回的是字段的值的信息
根据需要返回的rows为元组或者dict类型
测试返回float *的值，是否可以解析成原来的值?
如何设计查询的结果集？ResultSet

接口设计
    获取字段
    1、一次性获取结果集合
    2、先获取第一行，然后继续往后获取。。。
    3、query执行sql


经验：
    使用python数据类型与c语言数据类型进行转换
    返回的c语言指针与python返回的指针值是一致的，也就是说python操作的是c语言开辟出来的内存，必须提供c语言接口进行垃圾回收
    使用ctypes.cast将void_p与其他类型的指针进行转换，如果传入参数无法进行或者很难进行python的转换，都可以将argtypes定位c_void_p
    对c语言的字符串进行转换时，使用ctypes.stringat对c_char_p转换为python字符串(decprecated)

bugs:
    tsdb_affected_rows.restypes = (ctypes.c_uint64, )
    tsdb_user_name.restype = ctypes.c_char_p
    为什么上面这两种用法可以混用，但是当c函数返回值是char *时，使用第一种方式会报段错误。。。

    gcc触发致命错误：No python.h。
    sudo yum install python-devel   # for python2.x installs
    sudo yum install python34-devel   # for python3.4 installs

    sudo apt-get install python-dev   # for python2.x installs
    sudo apt-get install python3-dev  # for python3.x installs
