import os
import requests
import threading
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


def auto_report(line_id, wallet_id):

    obj = Worker(line_id, wallet_id, True)
    obj.set_name(line_id+'_thread')
    return obj

    #
    # def run(time_interval, line_id, wallet_id, t_stop, t_flag):
    #     get_short = 1
    #     while (not t_stop.is_set()):
    #         print '==============================='
    #         print 'in thread - ', time_interval, '- name -', current_thread().getName(), '-- enumerate --', enumerate()
    #         print dir(t_flag), 'thread name = ', current_thread().getName()
    #         print '==============================='
    #
    #         #
    #         # price = coin_price.get_data()
    #         # data = data_getter.get_data_now(wallet_id,0)
    #         # if data == -1:
    #         #     continue
    #         # p_data = data_getter.process_data(data)
    #         # if p_data == -1:
    #         #     continue
    #         #
    #         # sending_text = '===================\n'
    #         # sending_text += 'Net Balance : \n' + str(p_data[len(p_data)-1]) + ' BTC\n'
    #         # sending_text += str(p_data[len(p_data)-1]*price['BTC']) + ' THB\n'
    #         # sending_text += '===================\n'
    #         #
    #         # is_running = False
    #         # # print 'len p data = ', len(p_data[:-1]) , 'p data = ', p_data
    #         # for x in p_data[:-1]:
    #         #     if get_short == 1 and float(x['speed'][:-3]) == 0:
    #         #         continue
    #         #     else:
    #         #         is_running = True
    #         #         sending_text += 'algo : ' + x['algo'] +'\n'
    #         #         sending_text += 'speed : ' + x['speed'] + '\n'
    #         #         sending_text += 'balance : ' + x['balance'] + '\n'
    #         #         sending_text += '===================\n'
    #         #
    #         # if is_running == False:
    #         #     sending_text += 'Miner Offline !!!\n'
    #         #     sending_text += 'Please Check.\n'
    #         #     sending_text += '===================\n'
    #         #
    #         # send_line_notify(sending_text, line_id)
    #         time.sleep(time_interval)

    # print time_interval, ' ', line_id, ' ', wallet_id
    # print '\n1111current thread = ', current_thread().getName(), ' -- all thread --' , enumerate()
    # print dir(t_flag), '1111111', current_thread().getName()

    # t_flag.is_run = 0
    #
    # t_stop = Event()
    # if t_stop_flag == 1:
    #     t_stop.set()
    #     # t_flag.is_run = 0
    #
    # elif t_stop_flag == 0:
    #     # t_flag.run = 1
    #     for x in enumerate():
    #         if x.getName() == (line_id+'_thread'):
    #             t_stop.clear()
    #             t_flag.is_run = 1
    #             t = Thread(target=run, args=(time_interval, line_id, wallet_id, t_stop, t_flag), name=line_id+'_thread')
    #             t.start()
    #     if t_stop.is_set():
    #         t_stop.clear()
    #     # t_flag.is_run = 1
    #     t = Thread(target=run, args=(time_interval, line_id, wallet_id, t_stop, t_flag), name=line_id+'_thread')
    #     t.start()

        # print dir(t_flag), '2222222'

    # print '\n2222current thread = ', current_thread().getName(), ' -- all thread --' , enumerate(), 't_flag = ', t_flag.is_run, '=====', dir(t_flag)

class Worker(threading.Thread):
    ns = threading.local()
    interval = 1800
    def __init__(self, line_id, wallet_id, val):
        threading.Thread.__init__(self)
        self.val = val
        self.line_id = line_id
        self.wallet_id = wallet_id

    def run(self):

        # # self.ns.val = self.val
        # for i in range(5):
        #     self.ns.val = self.val+1
        #     print("Thread:", self.name, "value:", self.ns.val)
        #     time.sleep(2)

        while (self.val):
            print '\n==============================='
            print '\nin thread - ', '- name -', threading.current_thread().getName(), '-- enumerate --', threading.enumerate()
            print '\nthread name = ', threading.current_thread().getName()
            print '\n==============================='


            price = coin_price.get_data()
            data = data_getter.get_data_now(self.wallet_id,0)
            if data == -1:
                continue
            p_data = data_getter.process_data(data)
            if p_data == -1:
                continue

            sending_text = '===================\n'
            sending_text += 'Net Balance : \n' + str(p_data[len(p_data)-1]) + ' BTC\n'
            sending_text += str(p_data[len(p_data)-1]*price['BTC']) + ' THB\n'
            sending_text += '===================\n'

            # print 'len p data = ', len(p_data[:-1]) , 'p data = ', p_data
            is_running = False
            get_short = 1
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

            send_line_notify(self.sending_text, self.line_id)
            time.sleep(self.interval)


    def set_name(self, new_name):
        self.setName(new_name)

    def set_val(self, new_val):
        self.val = new_val




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
