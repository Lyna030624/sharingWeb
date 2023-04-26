# -*- coding: utf-8 -*-
import os
import time
import pymysql
from flask import Flask, render_template, jsonify
from flask import redirect
from flask import request
from flask import send_from_directory
from flask import url_for
from flask import session
from model.change_password import ch_password, is_null2
from model.check_login import is_existed, exist_user, is_null, adm
from model.check_regist import add_user
from model.an_update import update

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'


@app.route('/')
def index():
    return redirect(url_for('user_login'))


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        tno = request.form['tno']
        username = request.form['username']
        password = request.form['password']
        session['tno'] = tno
        print(tno)
        session['username'] = username
        if is_null(username, password, tno):
            login_massage = "温馨提示：工号、账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif is_existed(tno, username, password):
            if adm(tno):
                return render_template('index.html', username=username)
            else:
                return render_template('index1.html', username=username)
        elif exist_user(tno):
            login_massage = "温馨提示：密码或工号错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')


@app.route("/usercenter")
def usercenter():
    tno = session.get("tno")
    username = session.get("username")
    print(tno)
    if adm(tno):
        return render_template('index.html', username=username)
    else:
        return render_template('index1.html', username=username)


@app.route('/cha_password', methods=['GET', 'POST'])
def cha_password():
    if request.method == 'POST':
        tno = request.form['tno']
        password = request.form['password']
        if is_null2(password):
            login_massage = "温馨提示：密码不能为空"
            return render_template('change_password.html', message=login_massage)
        elif ch_password(password, tno):
            login_massage = "修改密码成功！"
            return render_template('change_password.html', message=login_massage)
    return render_template('change_password.html')


@app.route("/register_html")
def register_html():
    return render_template('register.html')


@app.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        tno = request.form['tno']
        username = request.form['username']
        password = request.form['password']
        # rig = request.form['rig']
        if is_null(username, password, tno):
            login_massage = "温馨提示：工号是必填"
            return render_template('register.html', message=login_massage)
        elif exist_user(tno):
            login_massage = "温馨提示：用户已存在"
            # return redirect(url_for('user_login'))
            return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['tno'], request.form['username'], request.form['password'], request.form['password'])
    return render_template('register.html', username=request.form['username'])


@app.route('/annco_html', methods=['GET', 'POST'])
def annco_html():
    return render_template('create_annco.html')


@app.route('/create_annco', methods=['GET', 'POST'])
def create_annco():
    if request.method == 'POST':
        update(request.form['anna'], request.form['anpa'], request.form['aninformation'], request.form['anti'])
    return render_template('create_annco.html')


# @app.route('/show_an')
# def show_an():
#     conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
#     cur = conn.cursor()
#     sql = "SELECT * FROM anno"
#     cur.execute(sql)
#     An = cur.fetchall()
#     conn.close()
#     return render_template('announcement.html', an=An)

@app.route("/course")
def course():
    return render_template('course.html')


@app.route("/announcement")
def announcement():
    conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
    cur = conn.cursor()
    sql = "SELECT * FROM anno"
    cur.execute(sql)
    An = cur.fetchall()
    conn.close()
    return render_template('announcement.html', an=An)

def model(sql):
    # 1.链接mysql数据库
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='LOVE3690',
                         database='python_test',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        # 2.创建游标对象
        cursor = db.cursor()
        # 3.执行sql语句
        res = cursor.execute(sql)
        db.commit()  # 在执行sql语句时，注意进行提交
        # 4.提取结果
        data = cursor.fetchall()
        if data:
            return data
        else:
            return res
    except:
        db.rollback()  # 当代码出现错误时，进行回滚
    finally:
        # 6.关闭数据库连接
        db.close()
# 留言板列表 显示留言信息
@app.route("/hello")
def hello():
    conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
    cur = conn.cursor()
    sql = "SELECT * FROM forum"
    cur.execute(sql)
    date = cur.fetchall()
    conn.close()
    return render_template('forum.html', date=date)


# 定义视图 显示留言添加的页面
@app.route('/add')
def add():
    return render_template('forum_add.html')


# 定义视图函数 接收表单数据，完成数据的入库
@app.route('/insert', methods=['POST'])
def insert():
    # 1.接收表单数据
    data = request.form.to_dict()
    data['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
    print(data)
    # 2.把数据添加到数据库
    sql = f'insert into forum values(null,"{data["username"]}","{data["info"]}","{data["date"]}")'
    res = model(sql)
    print(res)
    # 3.成功后页面跳转到 留言列表界面
    if res:
        return '<script>alert("留言成功！");location.href="/"</script>'
    else:
        return '<script>alert("留言发布失败！");location.href="/add"</script>'


# 删除 一行留言
@app.route("/delete")
def delete():
    tno = session.get("tno")
    sql = f'delete from forum where tno={tno}'
    res = model(sql)
    if res:
        return '<script>alert("删除成功！");location.href="/"</script>'
    else:
        return '<script>alert("删除失败！");location.href="/"</script>'


# 修改留言视图界面  不能修改id 即使在text文本框中修改了也没用
@app.route("/forum_update")
def forum_update():
    tno = session.get("tno")
    sql = f'select * from forum where Tno={tno}'
    res = model(sql)
    return render_template('forum_update.html', data=res)


# 修改留言视图函数 在数据库中修改留言内容
@app.route('/modify', methods=['POST'])
def modify():
    # 1.接收表单数据
    data = request.form.to_dict()
    data['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
    # 2.把数据添加到数据库
    sql = f'update forum set username="{data["username"]}",info="{data["info"]}",date="{data["date"]}" where Tno={int(data["tno"])}'
    res = model(sql)
    # 3.成功后页面跳转到 留言列表界面
    if res:
        return '<script>alert("修改成功！");location.href="/"</script>'
    else:
        return '<script>alert("留言修改失败！");location.href="/"</script>'


@app.route('/coursecontent/<cid>', methods=['GET'])
def coursecontent(cid):
    session['cid'] = cid
    print(cid)
    # cuid = session.get("cuid")
    print("coursecontent success")
    conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
    cur = conn.cursor()
    conn.ping(reconnect=True)
    sql1 = "SELECT * FROM course2 WHERE cid='%s'" % cid
    # sql1 = "SELECT cuname,ccname FROM course2 INNER JOIN course3 ON course2.cuid = course3.cuid WHERE cid = '%s'" % cid
    cur.execute(sql1)
    units = cur.fetchall()
    # sql2 = "SELECT * FROM course2 WHERE cid = '%s'" % cid
    print("sql success")
    # cur.execute(sql2)
    print("execute success")
    conn.commit()
    # cc = cur.fetchall()
    print("units1")
    conn.close()
    return render_template('coursecontent.html', units=units, status="error")
    # return render_template('coursecontent.html')


@app.route("/coursecreated")
def coursecreated():
    tno = session.get("tno")
    print("coursecreated")
    conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
    cur = conn.cursor()
    sql = "SELECT * FROM course1 WHERE Tno = ('%s')" % tno
    print("sql")
    conn.ping(reconnect=True)
    cur.execute(sql)
    print("execute")
    conn.commit()
    u = cur.fetchall()
    print("u")
    conn.close()
    return render_template('coursecreated.html', u=u)


@app.route("/coursejoincontent/<cid>", methods=['GET'])
def coursejoincontent(cid):
    session['cid'] = cid
    # cid = session.get("cid")
    print("coursecontent success")
    conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
    cur = conn.cursor()
    sql = "SELECT * FROM course2 WHERE cid = '%s'" % cid
    print("sql success")
    conn.ping(reconnect=True)
    cur.execute(sql)
    print("execute success")
    conn.commit()
    j = cur.fetchall()
    print("units")
    conn.close()
    return render_template('coursejoincontent.html', j=j)


@app.route("/coursejoined")
def coursejoined():
    par = session.get("tno")
    print("coursejoined")
    conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
    cur = conn.cursor()
    sql = "SELECT * FROM course1 WHERE participator = '%s'" % par
    print("sql")
    conn.ping(reconnect=True)
    cur.execute(sql)
    print("execute")
    conn.commit()
    p = cur.fetchall()
    print("join")
    conn.close()
    return render_template('coursejoined.html', p=p)


@app.route("/forum")
def forum():
    return render_template('forum.html')


@app.route("/material", methods=['GET'])
def material():
    # print(url_for('material', cuid=2))
    session['cuid'] = cuid
    entries = os.listdir('./uploads')
    print("get material")
    return render_template('material.html', entries=entries)


@app.route("/templates/<name>")
def ccontent(name):
    return 'templates %s!' % name


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # 渲染文件
    return render_template('material.html')


# 文件保存的目录，根据实际情况的文件结构做调整；
# 若不指定目录，可以写成f.save(f.filename)，可以默认保存到当前文件夹下的根目录
# 设置上传文件保存路径 可以是指定绝对路径，也可以是相对路径（测试过）
app.config['UPLOAD_FOLDER'] = 'uploads'  # 该目录需要自行创建
# 将地址赋值给变量
file_dir = app.config['UPLOAD_FOLDER']


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    """  文件上传  """
    if request.method == 'POST':
        cuid = session.get("cuid")
        # input标签中的name的属性值
        f = request.files['file']

        # 拼接地址，上传地址，f.filename：直接获取文件名
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        # 输出上传的文件名
        print(request.files, f.filename)
        filenames = []
        filenames.append(f.filename)
        conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
        cur = conn.cursor()
        sql = "INSERT INTO files(fno,filename) VALUES ('%s','%s')" % (f.filename, f.filename)
        cur.execute(sql)
        conn.commit()
        conn.close()
        print("file")
        entries = os.listdir('./uploads')
        print("shangchuanduqufile")
        return render_template('material.html', entries=entries)
    else:
        return render_template('material.html')


# @app.route("/showfile")
# def showfile():
#     entries = os.listdir('./uploads')
#     print("duqu")
#     return render_template('material.html', entries=entries)

@app.route('/files/<filename>')
def files(filename):
    return send_from_directory('./uploads', filename, as_attachment=True)


@app.route('/getcourseinform', methods=['GET', 'POST'])
def getcourseinform():
    if request.method == 'GET':
        return render_template('coursecreated.html')
    if request.method == 'POST':
        cid = request.form.get("cid")
        # cid = request.form['cid']
        cname = request.form['coursename']
        creater = request.form['teachername']
        tno = session.get("tno")
        print(tno)
        try:
            conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
            cur = conn.cursor()
            # sql1 = "INSERT INTO course1 (cid,cname,creater) VALUES ('%s','%s','%s')" % (cid, cname, creater)
            sql1 = "INSERT INTO course1 (cid,cname,creater,Tno) VALUES ('%s','%s','%s','%s')" % (cid, cname, creater, tno)
            # sql2 = "INSERT INTO course2 (cid) VALUES ('%s')" % cid
            try:
                conn.ping(reconnect=True)
                cur.execute(sql1)
                print("sql1")
                # cur.execute(sql2)
                conn.commit()
                print("sql2")
                conn.close()
            except:
                conn.rollback()
                print("false1")
            return render_template('coursecreated.html')
        except:
            print("flase2")
            return render_template('coursecreated.html', message='input false!')


global cuid
cuid = 0


@app.route('/createunit', methods=['GET', 'POST'])
def createunit():
    if request.method == 'GET':
        return render_template('coursecontent.html')
    if request.method == 'POST':
        cuname = request.form['cuname']
        cid = session.get("cid")
        global cuid
        cuid = cuid + 1

        session['cuid'] = cuid
        print(cid)
        print(cuname)
        try:
            conn = pymysql.Connect(host='localhost', user='root', password='LOVE3690', database='python_test')
            cur = conn.cursor()
            sql = "SELECT cuid FROM course2"
            cur.execute(sql)
            print(sql)
            uu = cur.fetchall()
            print(uu)
            for i in uu:
                print(i[0])
                if cuid == i[0]:
                    cuid = cuid + 1
                    print(cuid)
            sql1 = "INSERT INTO course2(cid, cuname, cuid) VALUES ('%s', '%s', '%s')" % (cid, cuname, cuid)
            print(sql1)
            # sql2 = "INSERT INTO course3(cuid) VALUES('%s')" % cuid
            # sql2 = "CREATE TABLE '%s' ('%s' int, ccname varchar(20)," \
            #        "ccid int not null, primary key(ccid))engine=innodb default charset=utf8" % (cuid, cuid)
            try:
                conn.ping(reconnect=True)
                print("ping")
                cur.execute(sql1)
                print("sql1")

                # cur.execute(sql2)
                # print("sql2")
                conn.commit()
                print(conn)
                conn.close()
            except:
                conn.rollback()
                print("false unit1")
            return render_template('coursecontent.html')
        except:
            print("false unit2")
            return render_template('coursecontent.html', message='input false!')


# @app.route('/bianli')
# def bianli():
#     print("098")
#     conn = pymysql.Connect(host='localhost', user='root', password='123456', database='course')
#     cur = conn.cursor()
#     sql = "SELECT * FROM course1"
#     print("000")
#     conn.ping(reconnect=True)
#     cur.execute(sql)
#     print("111")
#     conn.commit()
#     u = cur.fetchall()
#     print("222")
#     conn.close()
#     return render_template('coursecreated.html', u=u, status="error")


app.debug = True
