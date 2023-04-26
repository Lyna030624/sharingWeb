from templates.config import conn

cur = conn.cursor()


def add_user(tno, username, password, rig):
    if rig =="管理员":
        rig = 1
    else:
        rig = 0
    # sql commands
    sql = "INSERT INTO U(Tno, username, password, rig) VALUES ('%s','%s','%s','%s')" % (tno, username, password, rig)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()
