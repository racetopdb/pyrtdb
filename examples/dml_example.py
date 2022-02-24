from pyrtdb.cursor import DictCursor
import pyrtdb
import sys
from pathlib import Path
import random
from typing import List
import datetime

sys.path.append(str(Path.cwd().parent))


DB = pyrtdb.connect(pyrtdb.RTDB_HOST, pyrtdb.RTDB_PORT,
                    pyrtdb.RTDB_USER_NAME, pyrtdb.RTDB_PASSWORD)
CURSOR = DB.cursor()
NAMES = [
    "Michael Jordan",
    "Lebron James",
    "James Harden",
    "Kyrie Irving",
    "Kevin Durant",
]
BOOLS = [
    True,
    False
]


def create_db():
    CURSOR.execute("create database test_db if not exists;")
    CURSOR.execute("use test_db;")


def create_table():
    CURSOR.execute(
        "create table if not exists test_table(is_working boolean, age int, name char(100));")


def random_values(count: int) -> List:
    values = []
    for _ in range(count):
        row = (random.choice(BOOLS), random.randint(
            1, 100), random.choice(NAMES), )
        values.append(row)
    return values


def insert_values():
    CURSOR.execute(
        "insert into test_table(is_working, age, name) values(false, 12, 'Michael');")
    CURSOR.execute(
        "insert into test_table(is_working, age, name) values(true, 18, 'Jane');")
    CURSOR.execute(
        "insert into test_table(is_working, age, name) values(false, 12, 'Liming');")


def insert_random_values():
    count = 100
    rows = random_values(count)
    print(rows)
    for row in rows:
        CURSOR.execute(
            "insert into test_table(is_working, age, name) values(%s, %s, %s);", row)


def query():
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


def main():
    """
    1 - 创建数据库
    2 - 创建数据库表
    3 - 插入构建好的3条数据，然后再随机插入100条数据
    4 - 进行查询
    """
    with CURSOR:
        create_db()
        create_table()
        insert_values()
        insert_random_values()
        query()
    DB.close()


if __name__ == "__main__":
    main()
