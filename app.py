from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return '刘晨旭是个老哈皮'


@app.route('/main', methods=['GET', 'POST'])
def main():
    pass


if __name__ == '__main__':
    app.run()
