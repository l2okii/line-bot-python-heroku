# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import requests
from threading import *
import json
import db_adapter
import coin_price
import auto_run_report
import data_getter

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
thread_obj = {}

def get_data_now(wallet_id,get_short=0):

    price = coin_price.get_data()
    data = data_getter.get_data_now(wallet_id)
    if data == -1:
        # print 'data = -1'
        return -1
    p_data = data_getter.process_data(data)
    if p_data == -1:
        # print 'p_data = -1'
        return -1

    sending_text = '===================\n'
    sending_text += 'Net Balance : \n' + str(p_data[len(p_data)-1]) + ' BTC\n'
    sending_text += str(p_data[len(p_data)-1]*price['BTC']) + ' THB\n'
    sending_text += '===================\n'

    # print 'len p data = ', len(p_data[:-1]) , 'p data = ', p_data
    is_running = False
    for x in p_data[:-1]:
        if get_short == 1 and float(x['speed'][:-3]) == 0:
            # print 'get short return = -1'
            continue
        else:
            is_running = True
            sending_text += 'algo : ' + x['algo'] +'\n'
            sending_text += 'speed : ' + x['speed'] + '\n'
            sending_text += 'balance : ' + x['balance'] + '\n'
            sending_text += '===================\n'

    if is_running == False:
        sending_text += 'Miner Offline !!!\n'
        sending_text += 'Please Check.\n'
        sending_text += '===================\n'

    sending_text += 'BX Coin Price\n'
    sending_text += '===================\n'
    sending_text += 'BTC : ' + str(price['BTC']) + ' THB\n'
    sending_text += 'ETH : ' + str(price['ETH']) + ' THB\n'
    sending_text += '===================\n'

    return sending_text



    #
    # r = requests.get(api_link+wallet_id)
    # if r.status_code != 200 or r.text.find('error') != -1:
    #     print('error = ' + str(r.status_code) + ' \n ' + str(r.text.find('error')))
    #     return -1
    # data = r.text
    # # print(data)
    # p_data = process_data(data)
    # # print p_data[:-1]
    # price = coin_price.get_data()
    #
    # sending_text = '===================\n'
    # sending_text += 'Net Balance : \n' + str(p_data[len(p_data)-1]) + ' BTC\n'
    # sending_text += str(p_data[len(p_data)-1]*price['BTC']) + ' THB\n'
    # sending_text += '===================\n'
    #
    # # print 'len p data = ', len(p_data[:-1]) , 'p data = ', p_data
    # is_running = False
    # for x in p_data[:-1]:
    #     if get_short == 1 and float(x['speed'][:-3]) == 0:
    #         continue
    #     else:
    #         is_running = True
    #         sending_text += 'algo : ' + x['algo'] +'\n'
    #         sending_text += 'speed : ' + x['speed'] + '\n'
    #         sending_text += 'balance : ' + x['balance'] + '\n'
    #         sending_text += '===================\n'
    #
    #
    #
    # if is_running == False:
    #     sending_text += 'Miner Offline !!!\n'
    #     sending_text += 'Please Check.\n'
    #     sending_text += '===================\n'
    #
    #
    # sending_text += 'BX Coin Price\n'
    # sending_text += '===================\n'
    # sending_text += 'BTC : ' + str(price['BTC']) + ' THB\n'
    # sending_text += 'ETH : ' + str(price['ETH']) + ' THB\n'
    # sending_text += '===================\n'

    # if sending_text.find('speed') == -1:
    #     sending_text += 'Can not get hashing rate,\n May be Miner offline please check'
    # return sending_text


# def get_and_send(is_get_short):
#     data = get_data_now(is_get_short)
#     is_complete = send_line_notify(data)
#
# def get_data(time_interval=1800):
#     t = Timer(time_interval, get_data)
#     t.start()
#
#     # a = db_adapter.select_test()
#
#     data = get_data_now()
#     is_complete = send_line_notify(data)
#     if(is_complete != 0):
#         pass



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
    print '=================================='
    print '===========KEEP ALIVE============='
    print '=================================='
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
    line_id = event.source.user_id
    ack_text = text

    wallet = db_adapter.select_by_line(line_id)
    # print wallet
    if wallet != []:
        wallet_id = wallet[0][0]

    print '======= command ========/n'
    print text
    print '======= command ========/n'

    if wallet == [] and text.find('register_') == -1:
        ack_text = 'Please register first!! \n'
        ack_text += 'Ex. "register_YOURNICEHASHWALLET"'
    elif text == 'hashing rate':
        ack_text = get_data_now(wallet_id,1)
        # ack_text = 'hassssssh'
    elif text == 'all status':
        ack_text = get_data_now(wallet_id,0)
        # ack_text = 'hwwwwww s'
    elif text == 'coin price':
        price = coin_price.get_data()
        res = ''
        res += '===================\n'
        res += 'BX Coin Price\n'
        res += '===================\n'
        res += 'BTC : ' + str(price['BTC']) + ' THB\n'
        res += 'ETH : ' + str(price['ETH']) + ' THB\n'
        res += '===================\n'
        # print res
        ack_text = res
    elif text.lower() == 'hw status':
        ack_text = 'fuck you kuy \n' + str(event.source.user_id)

    elif text.find('register_') != -1:
        wallet_id = text.split('_')[-1:][0]
        res = db_adapter.select_by_line(line_id)

        # print res, ' ', len(res)

        if len(res) > 0:
            # print res[0]
            db_adapter.update_wallet(line_id,wallet_id)
            ack_text = 'This line account has been updated from wallet: \n' + res[0][0] + '\n to new wallet: \n' + wallet_id
        else:
            # print 'in else'
            db_adapter.register_new_line(line_id,wallet_id)
            ack_text = 'This line account has been register with wallet: '+ wallet_id
        # db_adapter.insert_test(user_id,wallet_id)

        # print user_id, '===', wallet_id
        # ack_text = user_id+'==='+wallet_id
        # wallet_id
    elif text == 'Register':
        ack_text = 'send me text = register_YOURNHWALLET'
    elif text.lower() == 'start auto report':
        print thread_obj
        if line_id not in thread_obj:
            obj = auto_run_report.auto_report(line_id, wallet_id)
            thread_obj.update({line_id:obj})
            obj.start()
            db_adapter.update_auto_state(line_id,True)
        # else:
        #     obj = thread_obj[line_id]
        #     obj.start()

        ack_text = 'auto report is activated'
    elif text.lower() == 'stop auto report':
        print thread_obj
        if line_id in thread_obj:
            obj = thread_obj[line_id]
            obj.set_val(False)
            del thread_obj[line_id]
            db_adapter.update_auto_state(line_id,False)
            print 'thread_obj = ', thread_obj
            # obj = auto_run_report.auto_report(line_id, wallet_id)
            # thread_obj.update({line_id:obj})
            # obj.start()
        # else:
        #     print thread_obj[line_id].isAlive()
        # auto_run_report.auto_report(line_id, wallet_id)
        ack_text = 'auto report is deactivated'
    else:
        ack_text = 'Wrong command!!!'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ack_text)) #reply the same message from user

def send_line(sending_text):
    Authorization = 'Bearer muwIp0la2JJzkUdnZM8u2xOxFhXx45Hna68DVbSIRh6'
    # headers = {'Content-Type': 'application/json; charset=UTF-8','Authorization':Authorization}
    ACCESS_TOKEN = 'muwIp0la2JJzkUdnZM8u2xOxFhXx45Hna68DVbSIRh6'
    LINE_HEADERS = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    URL = 'https://notify-api.line.me/api/notify'

    message = {'message': sending_text}
    r = requests.post(URL,headers=LINE_HEADERS,data=message)


    # curl -X POST -H 'Authorization: Bearer <access_token>' -F 'message=foobar' https://notify-api.line.me/api/notify
    print(r.text)
    return r


@app.route("/post/", methods=['GET', 'POST'])
def post_to_line():
    if request.method == 'POST':
        print(request.data)
        r = send_line(request.data)
        while r.status_code != 200:
            r = send_line(request.data)
            time.sleep(5)

        return 'post complete'
    #     try:
    #         line_bot_api.push_message('U124c9126948c40733c94109087411726', TextSendMessage(
    #             text='l2ig-Alert ! \n{}'.format(request.data)))
    #     except LineBotApiError as e:
    #         print('botting error {}'.format(e))
    #
    #     return 'post'
    # else:
    #     return "get"


def server_restart():

    rows = db_adapter.select_all()
    print rows
    print '0000000000000'
    thread_count = 0
    for row in rows:
        line_id = row[0]
        wallet_id = row[1]
        is_auto = row[2]
        if is_auto:
            thread_count += 1
            obj = auto_run_report.auto_report(line_id, wallet_id)
            thread_obj.update({line_id:obj})
            obj.start()
            db_adapter.update_auto_state(line_id,True)
    try:
        line_bot_api.push_message('U124c9126948c40733c94109087411726', TextSendMessage(
            text='l2ig-Alert ! \n{}'.format('Server just restarted'+ '_' + str(thread_count))))
    except LineBotApiError as e:
        print('botting error {}'.format(e))


if __name__ == "__main__":
    server_restart()
    app.run(host='0.0.0.0',port=os.environ['PORT'])
