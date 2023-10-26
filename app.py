import flask
import pickle
import time
from flask import request

app = flask.Flask(__name__)

def access_counter():
    try:
        with open('counter.pkl', 'rb') as f:
            counter = pickle.load(f)
    except:
        counter = 0
    return counter

def increment_counter():
    counter = access_counter()
    counter += 1
    with open('counter.pkl', 'wb') as f:
        pickle.dump(counter, f)
    return counter

def get_messages():
    try:
        with open('messages.pkl', 'rb') as f:
            messages = pickle.load(f)
    except:
        messages = []
    return messages

def add_message(message, nickname):
    messages = get_messages()
    tm = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime())
    messages.append({'message': message, 'nickname': nickname, 'time': tm})
    with open('messages.pkl', 'wb') as f:
        pickle.dump(messages, f)
    return messages

@app.route('/')
def index():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = flask.request.remote_addr
    counter = increment_counter()
    messages = get_messages()
    messages.reverse()
    return flask.render_template('index.html', ip=ip, counter=counter, messages=messages), 200

@app.route('/new-message', methods=['POST'])
def new_message():
    message = flask.request.form['message']
    nickname = flask.request.form['nickname']
    add_message(message, nickname)
    return flask.redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50135)