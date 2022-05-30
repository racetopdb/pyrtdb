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

pool = pyrtdb.NewPool(pyrtdb.RTDB_HOST, pyrtdb.RTDB_PORT,
                    pyrtdb.RTDB_USER_NAME, pyrtdb.RTDB_PASSWORD, charset=pyrtdb.CHARSET_UTF8)

def insert_data():
    db = pool.newDB()
    conn = db.newConn()
    if not conn:
        return
    conn.query("drop db 'test_db';")
    r = conn.query("create database 'test_db' if not exists;")
    if 0 != r :
        return
    r = conn.query("use test_db;")
    if 0 != r:
        return

    r = conn.query("create table if not exists users(id int, email varchar(254), password varchar(254));")
    if 0 != r:
        return

    r = conn.query("insert into users(id, email, password) values(1, 'uzi@sina.com', '123456');")
    if 0 != r:
        return
    r = conn.query("insert into users(id, email, password) values(2, 'uzi2@sina.com', '223456');")
    if 0 != r:
        return
    r = conn.query("insert into users(id, email, password) values(3, 'uzi3@sina.com', '323456');")
    if 0 != r:
        return

    reader = conn.query_reader("select * from users where time between '2020-01-02 00:00:00.000' and '2023-01-02 23:59:59.000';")
    if not reader:
        return
    while 0 == reader.cursor_next():
        id = reader.get_int(1)
        email = reader.get_string(2)
        password = reader.get_string(3)
        print("one row data",id,email,password)

insert_data()