from templates.config import conn

cur = conn.cursor()


def is_null(username, password, tno):
    if username == '' or password == '' or tno == '':
        return True
    else:
        return False


def is_existed(tno, username, password):
    sql = "SELECT * FROM U WHERE Tno='%s' and username  ='%s' and password ='%s'" % (tno, username, password)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def exist_user(tno):
    sql = "SELECT * FROM U WHERE Tno ='%s'" % tno
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    if len(result) == 0:
        return False
    else:
        return True


def adm(tno):
    sql = "SELECT rig FROM U WHERE tno ='%s'" % tno
    conn.ping(reconnect=True)
    cur.execute(sql)
    rig = cur.fetchall()
    conn.commit()
    if rig == ((1,),):
        return False
    else:
        return True
