import requests
from threading import *

host = 'http://127.0.0.1'
port = '4000'

def get_data(time_interval=10):
    t = Timer(time_interval, get_data)
    t.start()

    r = requests.get(host + ':' + port)
    if r.status_code != 200:
        print('error can not get data!! = ' + str(r.status_code))
        return
    data = r.text
    # print(data)
    h_res = get_hashrate(data)
    t_res = get_temp(data)

    r = requests.post('http://127.0.0.1:5002/post/', h_res + ' ' + t_res)
    if r.status_code != 200:
        print('error can not post data!! = ' + str(r.status_code))
        return
    print(str(r.status_code) + ' ' + r.text)


def get_temp(data=None):
    """
    #ff00ff : HW stat
    :return:
    """
    s_str = '"#ff00ff">'
    e_str = '</font>'
    index1 = data.rfind(s_str)
    index2 = data.find(e_str, index1)

    print(data[index1+9:index2])
    return data[index1+10:index2]


def get_hashrate(data=None):
    """
    #00ffff : hash rate
    """

    s_str = '"#00ffff">ETH'

    res = []
    index1 = data.rfind(s_str)
    index2 = 0
    len_str = len(data)

    # while index1 >= 0:

    # print('index1 = ' + str(index1))
    index2 = data.find('</font>', index1)
    # print('index2 = ' + str(index2))

    print(data[index1+10:index2])

    index1 = data[:index1].rfind(s_str)
    # print('index1 = ' + str(index1))

    index2 = data.find('</font>', index1)
    # print('index2 = ' + str(index2))
    print(data[index1+10:index2])
    return data[index1+10:index2]


if __name__ == '__main__':
    get_data()
