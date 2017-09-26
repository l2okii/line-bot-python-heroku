import os
import requests
import json

data = '{"1":{"pairing_id":1,"primary_currency":"THB","secondary_currency":"BTC","change":1.94,"last_price":127300,"volume_24hours":357.34989644,"orderbook":{"bids":{"total":901,"volume":1667.81617972,"highbid":127300},"asks":{"total":2062,"volume":457.69414839,"highbid":127400}}},"21":{"pairing_id":21,"primary_currency":"THB","secondary_currency":"ETH","change":0.53,"last_price":9550,"volume_24hours":1534.66649055,"orderbook":{"bids":{"total":594,"volume":3423.47048579,"highbid":9521},"asks":{"total":1774,"volume":4624.73158971,"highbid":9569}}},"22":{"pairing_id":22,"primary_currency":"THB","secondary_currency":"DAS","change":-0.71,"last_price":11200,"volume_24hours":95.42681222,"orderbook":{"bids":{"total":110,"volume":816.52760385,"highbid":11200},"asks":{"total":192,"volume":176.36545294,"highbid":11319.99}}},"23":{"pairing_id":23,"primary_currency":"THB","secondary_currency":"REP","change":0,"last_price":608.99,"volume_24hours":26.71705498,"orderbook":{"bids":{"total":21,"volume":5657.19558638,"highbid":569.47},"asks":{"total":201,"volume":1763.30541379,"highbid":608.99}}},"20":{"pairing_id":20,"primary_currency":"BTC","secondary_currency":"ETH","change":-1.64,"last_price":0.0746,"volume_24hours":50.62754599,"orderbook":{"bids":{"total":48,"volume":146.80573081,"highbid":0.0746},"asks":{"total":91,"volume":74.03540124,"highbid":0.07510635}}},"27":{"pairing_id":27,"primary_currency":"THB","secondary_currency":"BCH","change":6.67,"last_price":15000,"volume_24hours":194.53130242,"orderbook":{"bids":{"total":132,"volume":596.15935757,"highbid":14700},"asks":{"total":331,"volume":244.89464233,"highbid":15000}}},"4":{"pairing_id":4,"primary_currency":"BTC","secondary_currency":"DOG","change":20.83,"last_price":2.9e-7,"volume_24hours":15652883.842766,"orderbook":{"bids":{"total":84,"volume":11481316.959543,"highbid":2.9e-7},"asks":{"total":366,"volume":22260702.681053,"highbid":3.0e-7}}},"6":{"pairing_id":6,"primary_currency":"BTC","secondary_currency":"FTC","change":1.89,"last_price":1.08e-5,"volume_24hours":522.63458273,"orderbook":{"bids":{"total":18,"volume":670324.04162545,"highbid":1.043e-5},"asks":{"total":70,"volume":94184.37277777,"highbid":1.08e-5}}},"24":{"pairing_id":24,"primary_currency":"THB","secondary_currency":"GNO","change":-1.09,"last_price":3165,"volume_24hours":67.84537746,"orderbook":{"bids":{"total":30,"volume":7137.29048477,"highbid":3085.01},"asks":{"total":355,"volume":465.6202277,"highbid":3159.65}}},"13":{"pairing_id":13,"primary_currency":"BTC","secondary_currency":"HYP","change":2.5,"last_price":4.1e-7,"volume_24hours":136658.71920794,"orderbook":{"bids":{"total":14,"volume":1583389.2655827,"highbid":3.4e-7},"asks":{"total":57,"volume":2673971.669501,"highbid":4.3e-7}}},"2":{"pairing_id":2,"primary_currency":"BTC","secondary_currency":"LTC","change":3.45,"last_price":0.0132,"volume_24hours":432.02822355,"orderbook":{"bids":{"total":46,"volume":3843.7381163,"highbid":0.0132},"asks":{"total":120,"volume":1426.70897144,"highbid":0.013329}}},"3":{"pairing_id":3,"primary_currency":"BTC","secondary_currency":"NMC","change":-28.34,"last_price":0.0002675,"volume_24hours":34.00212417,"orderbook":{"bids":{"total":15,"volume":7062.14942973,"highbid":0.00026751},"asks":{"total":59,"volume":483.01205541,"highbid":0.00037329}}},"26":{"pairing_id":26,"primary_currency":"THB","secondary_currency":"OMG","change":8.2,"last_price":320.5,"volume_24hours":309420.93545688,"orderbook":{"bids":{"total":1649,"volume":182294.48207482,"highbid":319.13},"asks":{"total":6216,"volume":469446.6559765,"highbid":320.5}}},"14":{"pairing_id":14,"primary_currency":"BTC","secondary_currency":"PND","change":0,"last_price":1.0e-8,"volume_24hours":327783.4875,"orderbook":{"bids":{"total":0,"volume":0,"highbid":1.0e-8},"asks":{"total":161,"volume":614436331.25836,"highbid":1.0e-8}}},"5":{"pairing_id":5,"primary_currency":"BTC","secondary_currency":"PPC","change":0,"last_price":0.00033427,"volume_24hours":0,"orderbook":{"bids":{"total":5,"volume":5176.75039036,"highbid":0.00013021},"asks":{"total":60,"volume":1051.14550025,"highbid":0.0003329}}},"19":{"pairing_id":19,"primary_currency":"BTC","secondary_currency":"QRK","change":0,"last_price":8.8e-7,"volume_24hours":257.345025,"orderbook":{"bids":{"total":9,"volume":180318.35789904,"highbid":9.1e-7},"asks":{"total":58,"volume":86264.93359059,"highbid":1.66e-6}}},"15":{"pairing_id":15,"primary_currency":"BTC","secondary_currency":"XCN","change":-7.94,"last_price":5.8e-7,"volume_24hours":23784.26129032,"orderbook":{"bids":{"total":11,"volume":760333.32813525,"highbid":3.1e-7},"asks":{"total":131,"volume":1023018.1793707,"highbid":6.0e-7}}},"7":{"pairing_id":7,"primary_currency":"BTC","secondary_currency":"XPM","change":0,"last_price":3.9e-5,"volume_24hours":0,"orderbook":{"bids":{"total":8,"volume":5623.26764057,"highbid":2.883e-5},"asks":{"total":57,"volume":5616.15080213,"highbid":3.899e-5}}},"17":{"pairing_id":17,"primary_currency":"BTC","secondary_currency":"XPY","change":0,"last_price":3.8e-6,"volume_24hours":1328.112436,"orderbook":{"bids":{"total":9,"volume":129297.70517486,"highbid":3.8e-6},"asks":{"total":29,"volume":35996.67382776,"highbid":4.18e-6}}},"25":{"pairing_id":25,"primary_currency":"THB","secondary_currency":"XRP","change":0.17,"last_price":5.93,"volume_24hours":1403602.310354,"orderbook":{"bids":{"total":271,"volume":2005530.652682,"highbid":5.94},"asks":{"total":2382,"volume":5837027.469393,"highbid":5.98999999}}},"8":{"pairing_id":8,"primary_currency":"BTC","secondary_currency":"ZEC","change":-0.69,"last_price":0.0573,"volume_24hours":137.17568402,"orderbook":{"bids":{"total":26,"volume":94.36745702,"highbid":0.055724},"asks":{"total":345,"volume":264.94019935,"highbid":0.0581}}}}'

api_link = 'https://bx.in.th/api/'



def get_data(coin_index=1):
    r = requests.get(api_link)
    if r.status_code != 200 or r.text.find('error') != -1:
        print('error = ' + str(r.status_code) + ' \n ' + str(r.text.find('error')))
        return -1
    data = r.text
    p_data = get_btc_eth_price(data)
    # print(data)
    # p_data = process_data(data,coin_index)
    print p_data
    return p_data

def get_btc_eth_price(data):
    res = ''
    res += '===================\n'
    res += 'BX Coin Price\n'
    res += '===================\n'
    json_data = json.loads(data)
    res += 'BTC : ' + str(json_data['1']['last_price']) + ' THB\n'
    res += 'ETH : ' + str(json_data['21']['last_price']) + ' THB\n'
    res += '===================\n'
    return res

def process_data(data,coin_index):
    json_data = json.loads(data)
    return json_data[str(coin_index)]['last_price']

if __name__ == "__main__":
    process_data(data,21)
