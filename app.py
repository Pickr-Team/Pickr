from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/topic_list')
def topic_list():
    return render_template('topic_list.html')


if __name__ == '__main__':
    app.run()
