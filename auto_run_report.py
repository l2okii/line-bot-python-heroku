import os
import requests
from threading import *
import time
import data_getter
import coin_price

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('nZCWA89uFKpYTnklDBwXUm6qYE7OgprVM/GJKQ5BPoGxvCDtNzhkERtzOieiVybu74w1y/J8IlnXQTPL4ruCzcQU/atrrhTYLadhYkYxGUBh0dQhpaqJ6rVeRpJtinzwPJAML6jwX2GS05OXYXvnDQdB04t89/1O/w1cDnyilFU=')

t_flag = local()
t_flag.is_run = 0
def auto_report(line_id, wallet_id,time_interval=30,t_stop_flag=0):
    print time_interval, ' ', line_id, ' ', wallet_id
    print '1111current thread = ', current_thread().getName(), ' -- all thread --' , enumerate()
    t_flag.is_run = 0

    t_stop = Event()
    if t_stop_flag == 1:
        t_stop.set()
        t_flag.is_run = 0

    elif t_stop_flag == 0:
        # t_flag.run = 1
        for x in enumerate():
            if x.getName() == (line_id+'_thread'):
                t_stop.clear()
                t = Thread(target=run, args=(time_interval, line_id, wallet_id, t_stop), name=line_id+'_thread').start()
                t_flag.is_run = 1
        if t_stop.is_set():
            t_stop.clear()
        t = Thread(target=run, args=(time_interval, line_id, wallet_id, t_stop), name=line_id+'_thread').start()
        t_flag.is_run = 1


    print '2222current thread = ', current_thread().getName(), ' -- all thread --' , enumerate()


def run(time_interval, line_id, wallet_id, t_stop):
    get_short = 1
    while (not t_stop.is_set()):
        print '==============================='
        print 'in thread - ', time_interval, '- name -', current_thread().getName(), '-- enumerate --', enumerate()
        print t_flag.is_run, 'thread name = ', current_thread().getName()
        print '==============================='

        #
        # price = coin_price.get_data()
        # data = data_getter.get_data_now(wallet_id,0)
        # if data == -1:
        #     continue
        # p_data = data_getter.process_data(data)
        # if p_data == -1:
        #     continue
        #
        # sending_text = '===================\n'
        # sending_text += 'Net Balance : \n' + str(p_data[len(p_data)-1]) + ' BTC\n'
        # sending_text += str(p_data[len(p_data)-1]*price['BTC']) + ' THB\n'
        # sending_text += '===================\n'
        #
        # is_running = False
        # # print 'len p data = ', len(p_data[:-1]) , 'p data = ', p_data
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
        # if is_running == False:
        #     sending_text += 'Miner Offline !!!\n'
        #     sending_text += 'Please Check.\n'
        #     sending_text += '===================\n'
        #
        # send_line_notify(sending_text, line_id)
        time.sleep(time_interval)



def send_line_notify(sending_text, line_id):
    try:
        line_bot_api.push_message(line_id, TextSendMessage(
            text='l2ig-Auto-Alert ! \n{}'.format(sending_text)))
    except LineBotApiError as e:
        print('botting error {}'.format(e))
        return -1
    return 0

if __name__ == "__main__":
    auto_report('line_id', 'wallet_id', 2, 0)
