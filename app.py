from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('login.html')


@app.route('/footer', methods=['GET', 'POST'])
def footer():
    return render_template('footer.html')


@app.route('/header', methods=['GET', 'POST'])
def header():
    return render_template('header.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    pass


if __name__ == '__main__':
    app.run()
