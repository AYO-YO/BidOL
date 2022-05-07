import random
import smtplib
import sqlite3
from email.mime.text import MIMEText

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

conn = sqlite3.connect('data', check_same_thread=False)


def query_sql(sql_str, args=tuple()):
    cur = conn.cursor()
    if len(args) > 0:
        cur.execute(sql_str, args)
    else:
        cur.execute(sql_str)
    res = cur.fetchall()
    cur.close()
    return res


def execute_sql(sql_str, args=tuple()):
    cur = conn.cursor()
    if len(args) > 0:
        cur.execute(sql_str, args)
    else:
        cur.execute(sql_str)
    conn.commit()
    cnt = cur.rowcount
    cur.close()
    return cnt


user = {}
user['role'] = -1
user['name'] = ''


@app.route('/')
def hello():  # put application's code here
    user['role'] = -1
    user['name'] = ''
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            return render_template('login.html')
        case 'POST':
            user_name = request.values.get('user_name')
            user_pwd = request.values.get('user_pwd')
            flag = query_sql('select role from user where name=? and pwd=?', (user_name, user_pwd))
            if len(flag) > 0:
                user['name'] = user_name
                role = flag[0][0]
                user['role'] = role
                return redirect(url_for('main'))
            else:
                return render_template('alert.html', m='登录失败！请检查用户名及密码！')


@app.route('/footer', methods=['GET', 'POST'])
def footer():
    return render_template('footer.html')


@app.route('/header', methods=['GET', 'POST'])
def header():
    return render_template('header.html', user=user)


@app.route('/main', methods=['GET', 'POST'])
def main():
    role = user['role']
    if role != -1:
        content = query_sql(
            'select _id, title, date, duration, read_num, abstract from bid where active = true order by date DESC ')
        return render_template('index.html', role=role, content=content)
    else:
        return redirect(url_for('login'))


@app.route('/content', methods=['GET', 'POST'])
def content():
    match request.method:
        case 'GET':
            c_id = request.values.get('article_id')
            if c_id is None:
                return redirect(url_for('main'))
            read_num = query_sql('select read_num from bid where _id=?', (c_id,))[0][0] + 1
            execute_sql('update bid set read_num=? where _id=?', (read_num, c_id))
            content = query_sql('select * from bid where _id=?', (c_id,))[0]
            return render_template('content.html', content=content)


def send_mail(receivers: list, content: str):
    """
    发送邮件给指定邮箱
    :param receivers 接收者列表
    :param content 邮件内容
    """
    # 邮箱服务器及对应用户信息
    mail_host = 'smtp.qq.com'
    mail_port = 465
    mail_user = '958973633@qq.com'
    mail_password = 'iryqvrrwgcwfbeji'

    # 发送者和接收者，此处注意QQ邮箱不能直接群发
    sender = '958973633@qq.com'
    for receiver in receivers:
        receivers = [receiver]

        # 设置邮件内容格式
        message = MIMEText(content)
        message['Subject'] = '注册验证码'
        message['From'] = sender
        message['To'] = receivers[0]
        try:
            # 建立与邮件服务器的连接
            smtp_obj = smtplib.SMTP_SSL(mail_host, mail_port)
            smtp_obj.login(mail_user, mail_password)
            # 发送邮件
            smtp_obj.sendmail(sender, receivers, message.as_string())
            # 关闭连接
            smtp_obj.quit()
            print(f'向{receiver}发送邮件成功！')
        except smtplib.SMTPException as e:
            print(e)
            return False
    return True


@app.route('/register', methods=['GET', 'POST'])
def register():
    match request.method:
        case 'GET':
            return render_template('register.html')
        case 'POST':
            mail = request.values.get('email')
            user_name = request.values.get('user_name')
            pwd = request.values.get('pwd')
            check_code = request.values.get('check_code')
            if user['code'] != check_code:
                return render_template('alert.html', m="验证码输入错误！")
            sql = 'select * from user where email=?'
            flag = len(query_sql(sql, (mail,))) > 0
            if flag:
                return render_template('alert.html', m='该邮箱已注册！')
            sql = 'insert into user(name, pwd, role, email) VALUES (?,?,?,?)'
            flag = execute_sql(sql, (user_name, pwd, 0, mail))
            if flag:
                return render_template('alert.html', m='注册成功！')
            else:
                return render_template('alert.html', m='注册失败，请联系管理员！')


@app.route('/send_code', methods=['POST'])
def send_code():
    mail = request.values.get('email')
    code = random.randint(1000, 9999)
    print(mail)
    print(code)
    text = f"""【高校采购门户网站】您的注册验证码为：{code}"""
    user['mail'] = mail
    user['code'] = str(code)
    return str(send_mail([mail], text))


@app.route('/create', methods=['GET', 'POST'])
def create():
    match request.method:
        case 'GET':
            return render_template('create.html')
        case 'POST':
            title = request.values.get('title')
            abstract = request.values.get('abstract')
            duration = request.values.get('duration')
            is_active = 1 if request.values.get('is_active') == 'on' else 0
            content = request.values.get('content')
            sql = 'insert into bid(title, content, duration, active, abstract) values (?,?,?,?,?)'
            flag = execute_sql(sql, (title, content, duration, is_active, abstract))
            return render_template('alert.html', m='发布成功！' if flag else '发布失败。请联系管理员。。')


if __name__ == '__main__':
    app.run()
