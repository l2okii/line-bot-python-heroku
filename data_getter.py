import os
import requests
from threading import *
import json
import db_adapter
import coin_price

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

api_link = 'https://api.nicehash.com/api?method=stats.provider&addr='

def get_data_now(wallet_id,get_short=0):
    r = requests.get(api_link+wallet_id)
    if r.status_code != 200 or r.text.find('error') != -1:
        print('error = ' + str(r.status_code) + ' \n ' + str(r.text.find('error')))
        return -1
    data = r.text
    return data


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
