import sys
from pathlib import Path

# 必须确保{ProjectDir}/rtdbcli的路径已经配置到系统路径，否则会抛出异常ModuleNotFoundError
try:
    import pyrtdb
except ModuleNotFoundError:
    import sys
    # 导入包路径
    sys.path.append(str(Path.cwd().parent))
    import pyrtdb

DB = pyrtdb.connect(pyrtdb.RTDB_HOST, pyrtdb.RTDB_PORT,
                    pyrtdb.RTDB_USER_NAME, pyrtdb.RTDB_PASSWORD, charset=pyrtdb.CHARSET_UTF8)

with DB:
    with DB.cursor() as cursor:
        cursor.execute("create database 'test_db' if not exists;")
        cursor.execute("use test_db;")
        cursor.execute(
            "create table if not exists users(id int, email varchar(254), password varchar(254));")
    with DB.cursor() as cursor:
        sql = "select last * from users;"
        cursor.execute(sql)
        # 获取一条记录
        result = cursor.fetchone()
        print(result)
