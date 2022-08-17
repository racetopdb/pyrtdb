# pyrtdb - the python connector for rtdb

----

## Project Directory
> {ProjectDirPath}是Python客户端连接器的项目根目录

## Fetaures
* 支持DB API 2.0(PEP 249)，详情可见resources/DB API 2.0
* 使用c扩展，内部使用标准库ctypes(Python外部函数库)来调用c语言动态链接库的函数
* 调用的C语言动态链接库libtsdb.so(或者tsdb.dll)是rtdb数据库官方对外的纯c语言接口动态链接库，rtdbcli的python连接器通过
调用该动态链接库来完成对rtdb数据库的操作。因为依赖于c扩展，所以在跨平台上必须依赖于具体操作系统的动态链接库

## Requirements
* Cpython: 3.6以上版本(32位或者64位)
* 支持Linux操作系统、Windows操作系统(64位)、Windows操作系统(32位)；依赖于具体操作系统下的动态链接库
* rtdb的动态连接库libtsdb.so;目前rtdb包会根据当前Cpython解释器的版本(32位或者64位)来选择动态链接库
    * Linux操作系统的动态连接库路径位于{PluginDirPath}/python/dynamiclib/linux/win32/libtsdb.so
    * Windows32位操作系统的动态连接库路径位于{PluginDirPath}/python/dynamiclib/windows/win32/tsdb.dll
    * Windows64位操作系统的动态连接库路径位于{PluginDirPath}/python/dynamiclib/windows/x64/tsdb.dll

## Installation

* 配置rtdbcli包的导入路径，以下三种方式任意选择一种即可
    * 通过代码将rtdbcli的包导入路径配置到系统路径
  ```Python
  import sys

  # 在导入rtdbcli之前需要将rtdbcli的包路径写入到系统路径
  sys.path.append(str(Path.cwd().parent))

  import pyrtdb
  ```
    * 配置Windows系统路径
    在Windows系统框中，键入"高级系统设置"，打开高级系统设置窗口。按下环境变量按钮，系统变量部分中，找到并选择 PATH 环境变量。单击编辑。如果 PATH 环境变量不存在，请单击新建。在编辑系统变量（或新建系统变量）窗口中，指定 PATH 环境变量的值为上文{ProjectDirPath}/rtdbcli的绝对路径。单击确定。通过单击确定关闭所有剩余窗口。
    * 配置Linux系统路径(bash path)
    通过修改用户目录下的~/.bashrc文件进行配置
    ```shell
    # 在最后一行加上
    export PATH=$PATH:{ProjectDirPath}/pyrtdb
    ```


> 目前rtdb包尚未上传到PyPI(Python官方第三方包索引)，所以无需通过PyPI进行下载安装。目前支持的用户使用方式是将rtdbcli的包路径配置到系统路径之后，可见如下示例
(代码示例位于{ProjectDirPath}/pyrtdb/examples/simple_example.py)。

```Python
import sys
from pathlib import Path

# 必须确保{ProjectDirPath}/rtdbcli的路径已经配置到系统路径，否则会抛出异常ModuleNotFoundError
try:
    import pyrtdb
except ModuleNotFoundError:
    import sys
    # 导入包路径
    sys.path.append(str(Path.cwd().parent))
    import pyrtdb

DB = pyrtdb.connect(pyrtdb.RTDB_HOST, pyrtdb.RTDB_PORT,
                     pyrtdb.RTDB_USER_NAME, pyrtdb.RTDB_PASSWORD)

with DB:
    with DB.cursor() as cursor:
        cursor.execute("create database test_db if not exists;")
        cursor.execute("use test_db;")
        cursor.execute(
            "create table users if not exists users(id bigint, email varchar(255), password varchar(255));")
    with DB.cursor() as cursor:
        sql = "select last * from users;"
        cursor.execute(sql)
        # 获取一条记录
        result = cursor.fetchone()
        print(result)
```


## Documentation

* connect(host: str, port: int, user: str, password: str, **kwargs) 
connect是一个用于创建数据库连接的构造函数。该函数返回一个Connection对象。kwargs是可选的参数选项。该函数定义位于{ProjectDirPath}/pyrtdb/__init__.py
    * host 需要连接的主机IP，必填，默认值是127.0.0.1
    * port 需要连接的主机端口，必填, 默认值是9000
    * user 用户名，必填
    * password 用户密码，必填
    * timeout(可选, 通过kwargs传递) 连接超时时间，默认值为30
    * charset(可选) 表示数据库编码，数据库编码的默认值是CHARSET_WIN1
        选项位于rtdbcli.constant.py
        * CHARSET_UNKNOWN
        * CHARSET_GBK
        * CHARSET_UTF8
        * CHARSET_UCS2LE
        * CHARSET_UCS2BE
        * CHARSET_BIG5
        * CHARSET_EUCJP
        * CHARSET_SJIS
        * CHARSET_EUCKR
        * CHARSET_ISO1
        * CHARSET_WIN1
        * CHARSET_WIN2
    * dbname(可选) 需要连接的数据库名称，默认值为""

* apilevel
    一个字符串常量，表示模块支持的DB API版本。目前只允许使用字符串"1.0"和字符串"2.0"来进行表示。该值默认是"2.0。该常量定义位于{ProjectDirPath}/pyrtdb/__init__.py
* threadsafety
    用于表示本模块接口所支持的线程安全级别。该常量定义位于{ProjectDirPath}/pyrtdb/__init__.py。默认值为1

    * 值为0，线程间不可“共享”模块
    * 值为1，含义表示线程间可以共享该模块，但是不可以共享连接
    * 值为2，模块及数据库连接均可以在"线程间"共享
    * 值为3，模块、数据库连接以及游标（cursors）均可以在线程间“共享”

* paramstyle
    一个字符串常量，用于说明模块间接口所期望的参数标记。可选值如下。该常量定义位于{ProjectDirPath}/pyrtdb/__init__.py
    * qmark 问号风格
    * numeric 数字配合位置参数风格
    * named 命名参数风格
    * format ANSI C printf代码风格
    * pyformat Python的扩展格式化风格
    ```python
    // qmark
    CURSOR.execute("select * from students where name = ?", ("Michael", ))
    
    // numeric
    CURSOR.execute("select * from students where name = :1", ("Michael", ))
    
    // named
    CURSOR.execute("select * from students where name = :name", {'name': 'Michael'})
    
    // format
    CURSOR.execute("select * from students where name = %s", ("Michael", ))
    
    // pyformat
    CURSOR.execute("select * from students where name = %(name)s", ("Michael", ))
    CURSOR.execute("select * from students where name = %(name)s", {'name': 'Michael'})
    ```
    目前paramstyle仅支持format格式


## Usage
1. 连接数据库并创建游标
```
import pyrtdb

from pyrtdb.constant import RTDB_HOST, RTDB_PORT, RTDB_USER_NAME, RTDB_PASSWORD


DB = pyrtdb.connect(pyrtdb.RTDB_HOST, pyrtdb.RTDB_PORT, pyrtdb.RTDB_USER_NAME, pyrtdb.RTDB_PASSWORD)

CURSOR = DB.cursor()
```
2. 创建数据库
```Python
CURSOR.execute("create database test_db if not exists;")
CURSOR.execute("use test_db;")
```
2. 创建表
```Python
 CURSOR.execute(
        "create table if not exists test_table(is_working boolean, age int, name char(100));")
```

3. 插入数据
```Python
CURSOR.execute(
    "insert into test_table(is_working, age, name) values(false, 12, 'Michael');")
CURSOR.execute(
    "insert into test_table(is_working, age, name) values(true, 18, 'Jane');")
CURSOR.execute("insert into test_table(is_working, age, name) values(false, 12, 'Liming');")
```

4. 查询数据
```Python
sql1 = "select last * from test_table;"
CURSOR.execute(sql1)
print("Fetch all tuple rows: {}".format(CURSOR.fetchall()))

dictcur = DictCursor(DB)
dictcur.execute(sql1)
print("Fetch all dict rows: {}".format(dictcur.fetchall()))
dictcur.close()

sql2 = "select * from test_table where time between %s and %s"
start = datetime.datetime.now() - datetime.timedelta(days=3)
end = datetime.datetime.now() + datetime.timedelta(days=3)
CURSOR.execute(sql2, (start, end, ))
print("Fetch all tuple rows: {}".format(CURSOR.fetchall()))

sql3 = "select * from test_table where time between %s and %s and name = %s"
CURSOR.execute(sql3, (start, end, "Michael", ))
sql3_rows = CURSOR.fetchall()
print("Fetch all tuple rows: {}".format(sql3_rows))
for row in sql3_rows:
    assert(len(row) == 4)
    assert(row[len(row)-1] == 'Michael')
```

## Resources

* DB-API 2.0(PEP 249) https://www.python.org/dev/peps/pep-0249/

## License

GNU Lesser General Public License version 3