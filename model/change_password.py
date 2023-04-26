from templates.config import conn

cur = conn.cursor()


def ch_password(password, tno):
    sql = "UPDATE U set password ='%s' WHERE Tno ='%s'" % (password, tno)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def is_null2(password):
    if password == '':
        return True
    else:
        return False
