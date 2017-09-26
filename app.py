# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import requests
from threading import *
import json
import db_adapter

app = Flask(__name__)

algo_list = [
'Scrypt'
,'SHA256'
,'ScryptNf'
,'X11'
,'X13'
,'Keccak'
,'X15'
,'Nist5'
,'NeoScrypt'
,'Lyra2RE'
,'WhirlpoolX'
,'Qubit'
,'Quark'
,'Axiom'
,'Lyra2REv2'
,'ScryptJaneNf16'
,'Blake256r8'
,'Blake256r14'
,'Blake256r8vnl'
,'Hodl'
,'DaggerHashimoto'
,'Decred'
,'CryptoNight'
,'Lbry'
,'Equihash'
,'Pascal'
,'X11Gost'
,'Sia'
,'Blake2s'
,'Skunk'
]

line_bot_api = LineBotApi('nZCWA89uFKpYTnklDBwXUm6qYE7OgprVM/GJKQ5BPoGxvCDtNzhkERtzOieiVybu74w1y/J8IlnXQTPL4ruCzcQU/atrrhTYLadhYkYxGUBh0dQhpaqJ6rVeRpJtinzwPJAML6jwX2GS05OXYXvnDQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ea522a6ca14dfe8c11571cf33d8ffe12') #Your Channel Secret

btc_wallet = '3BBNyPvUJHqKuH1ptipEVj9NPugMD2ig9S'

api_link = 'https://api.nicehash.com/api?method=stats.provider&addr='
# port = '4000'

def get_data_now(btc_wallet,get_short=0):
    r = requests.get(api_link+btc_wallet)
    if r.status_code != 200 or r.text.find('error') != -1:
        print('error = ' + str(r.status_code) + ' \n ' + str(r.text.find('error')))
        return -1
    data = r.text
    # print(data)
    p_data = process_data(data)
    # print p_data[:-1]

    sending_text = '===================\n'
    sending_text += 'Net Balance : \n' + str(p_data[len(p_data)-1]) + ' BTC\n'
    sending_text += '===================\n'

    for x in p_data[:-1]:
        if get_short == 1 and float(x['speed'][:-3]) == 0:
            continue
        else:
            sending_text += 'algo : ' + x['algo'] +'\n'
            sending_text += 'speed : ' + x['speed'] + '\n'
            sending_text += 'balance : ' + x['balance'] + '\n'
            sending_text += '===================\n'


    return sending_text

def send_line_notify(sending_text):
    try:
        line_bot_api.push_message('U124c9126948c40733c94109087411726', TextSendMessage(
            text='l2ig-Alert ! \n{}'.format(sending_text)))
    except LineBotApiError as e:
        print('botting error {}'.format(e))
        return -1
    return 0

def get_and_send(is_get_short):
    data = get_data_now(is_get_short)
    is_complete = send_line_notify(data)

def get_data(time_interval=1800):
    t = Timer(time_interval, get_data)
    t.start()

    # a = db_adapter.select_test()

    data = get_data_now()
    is_complete = send_line_notify(data)
    if(is_complete != 0):
        pass



def process_data(data):
    list = []
    json_data = json.loads(data)
    json_data = json_data['result']['stats']
    sum_balance = 0
    for x in json_data:
        sum_balance += float(x['balance'])
        # if float(x['accepted_speed']) > 0:
            # print 'algo', algo_list[x['algo']], 'speed', x['accepted_speed'], 'GHz', 'balance', x['balance'], 'BTC'
        dic =  {'algo':algo_list[x['algo']], 'speed':x['accepted_speed']+'GHz', 'balance':x['balance']+'BTC'}
        list.append(dic)

            # print dic
    list.append(sum_balance)
    # print list
    return list


@app.route('/', methods=['GET'])
def get():
    return 'get'


@app.route("/callback/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    user_id = event.source.user_id
    ack_text = text

    wallet = db_adapter.select_by_line(user_id)
    print wallet

    if wallet == []:
        ack_text = 'Please register first!!'

    elif text == 'hashing rate':
        ack_text = get_data_now(wallet,1)
        # ack_text = 'hassssssh'
    elif text == 'all status':
        ack_text = get_data_now(wallet,0)
        # ack_text = 'hwwwwww s'
    elif text == 'coin price':
        ack_text = 'kuy price'
    elif text.lower() == 'hw status':
        ack_text = 'fuck you kuy \n' + str(event.source.user_id)
    elif text.find('register_') != -1:
        wallet_id = text.split('_')[-1:][0]
        res = db_adapter.select_by_line(user_id)

        print res, ' ', len(res)

        if len(res) > 0:
            print res[0]
            db_adapter.update_with_line(user_id,wallet_id)
            ack_text = 'This line account has been updated from wallet: \n' + res[0][0] + '\n to new wallet: \n' + wallet_id
        else:
            print 'in else'
            db_adapter.insert_test(user_id,wallet_id)
            ack_text = 'This line account has been register with wallet: '+ wallet_id
        # db_adapter.insert_test(user_id,wallet_id)

        print user_id, '===', wallet_id
        # ack_text = user_id+'==='+wallet_id
        # wallet_id
    else:
        ack_text = 'fuck!!! wrong command'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ack_text)) #reply the same message from user


@app.route("/post/", methods=['GET', 'POST'])
def post_to_line():
    if request.method == 'POST':
        print(request.data)
        try:
            line_bot_api.push_message('U124c9126948c40733c94109087411726', TextSendMessage(
                text='l2ig-Alert ! \n{}'.format(request.data)))
        except LineBotApiError as e:
            print('botting error {}'.format(e))

        return 'post'
    else:
        return "get"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    # get_data()
