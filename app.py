from flask import Flask
from flask import render_template
from flask import request
from bandwidth_sdk import Client
from bandwidth_sdk import Message
from bandwidth_sdk import Call
import random
import os

app = Flask(__name__)

#Client(os.environ['BANDWIDTH_USER_ID'], os.environ['BANDWIDTH_API_TOKEN'], os.environ['BANDWIDTH_API_SECRET'])
#fromNumber = os.environ['PHONE_NUMBER']

code = random.randint(1000, 9999)


@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')


@app.route('/verify', methods=['GET'])
def verify_page():
    global code
    num = request.args.get('number')
    if num[:2] != '+1':
        num = '+1' + num
    code = random.randint(1000, 9999)
    sendCode(num, request.args.get('action'), code)
    return render_template('verify.html')


@app.route('/result', methods=['GET'])
def result_page():
    success = verifyCode(request.args.get('input'))
    return render_template('result.html', success=success)


@app.route('/callEvents', methods=['GET'])
def speakCode():
    if request.args.get('eventType') == 'answer':
        return '<Response>' + '<SpeakSentence voice="kate" locale="en_US" gender="female">' + str(
            request.args.get('tag')) + '</SpeakSentence>' + '<Hangup></Hangup>' + '</Response>'


def sendCode(number, method, code):
    if method == 'Call':
        host = 'https://' + request.headers.get('Host') + '/callEvents'
        Call.create(fromNumber, number, callback_url=host, callbackHttpMethod='GET', tag=code)
    else:
        Message.send(sender=fromNumber, receiver=number, text=code, tag='verify Code')


def verifyCode(input):
    global code
    return int(input) == code


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
