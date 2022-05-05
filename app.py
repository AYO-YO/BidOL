from flask import Flask, render_template, request, url_for, redirect
import sqlite3

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
    cnt = cur.rowcount
    cur.close()
    return cnt


@app.route('/')
def hello():  # put application's code here
    return redirect(url_for('login'))


user = {}
user['role'] = -1
user['name'] = ''


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
        return render_template('index.html', role=role)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
