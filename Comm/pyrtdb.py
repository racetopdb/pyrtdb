from pathlib import Path

def getConn():
    try:
        import pyrtdb
    except ModuleNotFoundError:
        import sys
        # 导入包路径
        sys.path.append(str(Path.cwd().parent))
        import pyrtdb

    pool = pyrtdb.NewPool(pyrtdb.RTDB_HOST, pyrtdb.RTDB_PORT,
                    pyrtdb.RTDB_USER_NAME, pyrtdb.RTDB_PASSWORD, charset=pyrtdb.CHARSET_UTF8)
    db = pool.newDB()
    conn = db.newConn()

    return conn
conn = getConn()
