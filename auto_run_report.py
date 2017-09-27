import os
import requests
from threading import *
import time
import data_getter

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

def auto_report(line_id, wallet_id,time_interval=30):
    print time_interval, ' ', line_id, ' ', wallet_id
    t = Thread(target=run, args=(time_interval, line_id, wallet_id)).start()


def run(time_interval, line_id, wallet_id):
    while True:
        price = coin_price.get_data()
        data = data_getter.get_data_now(wallet_id,0)
        if data == -1:
            continue
        data = data_getter.process_data(data)
        if data == -1:
            continue

        sending_text = '===================\n'
        sending_text += 'Net Balance : \n' + str(p_data[len(p_data)-1]) + ' BTC\n'
        sending_text += str(p_data[len(p_data)-1]*price['BTC']) + ' THB\n'
        sending_text += '===================\n'

        is_running = False
        # print 'len p data = ', len(p_data[:-1]) , 'p data = ', p_data
        for x in p_data[:-1]:
            if get_short == 1 and float(x['speed'][:-3]) == 0:
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

        send_line_notify(sending_text, line_id)
        time.sleep(time_interval)



def send_line_notify(sending_text, line_id):
    try:
        line_bot_api.push_message(line_id, TextSendMessage(
            text='l2ig-Auto-Alert ! \n{}'.format(sending_text)))
    except LineBotApiError as e:
        print('botting error {}'.format(e))
        return -1
    return 0
