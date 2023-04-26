from templates.config import conn

cur = conn.cursor()


def update(anna, anpa, aninformation, anti):
    sql = "INSERT INTO anno(anna, anpa, aninformation, anti) VALUES ('%s','%s','%s','%s')" % (anna, anpa, aninformation,
                                                                                              anti)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()
