import requests
import threading
import json

host = 'http://127.0.0.1'
port = '4000'

key = ['version', 'running_time', 'eth_hashing_rate', 'eth_each_hashing_rate', 'other_hashing_rate', 'other_each_hashing_rate', 'temp_fan_detail', 'pool', 'invalid']


data = '''
<html><body bgcolor="#000000" style="font-family: monospace;">
{"result": ["10.0 - ETH", "99", "145125;334;1", "23539;26668;24270;17235;25998;27413", "417233;966;9", "67674;76672;69776;49552;74745;78814", "50;52;39;54;51;56;39;54;51;53;50;51", "daggerhashimoto.hk.nicehash.com:3353;lbry.hk.nicehash.com:3356", "0;0;0;0"]}<br><br><font color="#00ff00">ETH: Share accepted (265 ms)!
'''

def start():
    w = Worker('U124c9126948c40733c94109087411726')

def get_data():

    r = requests.get(host + ':' + port)
    if r.status_code != 200:
        print('error can not get data!! = ' + str(r.status_code))
        return 'Can not get data\n Please check Miner !!'

    data = r.text
    p_data = process_data(data)
    print p_data

    # h_res = get_hashrate(data)
    # t_res = get_temp(data)
    #
    # r = requests.post('http://127.0.0.1:5002/post/', h_res + ' ' + t_res)
    # if r.status_code != 200:
    #     print('error can not post data!! = ' + str(r.status_code))
    #     return
    # print(str(r.status_code) + ' ' + r.text)


def process_data(data):

    s_str = '{"result":'
    e_str = '<br><br>'
    dic = {}
    index1 = data.find(s_str)
    index2 = data.find(e_str, index1)
    # print index1, index2
    json_data = json.loads(data[index1:index2])
    json_data = json_data['result']


    for x in range(0,8):
        dic.update({key[x]:json_data[x]})

    # dic = {key[0]:json_data[0], key[1]: json_data[1], 'eth_hashing_rate': json_data[2], 'eth_each_hashing_rate': json_data[3], 'other_hashing_rate': json_data[4], 'other_each_hashing_rate': json_data[5], 'temp_fan_detail': json_data[6], 'pool': json_data[7], 'invalid': json_data[8]}

    sending_text = ''
    sending_text += '===================\n'
    sending_text += 'Total Speed\n'
    sending_text += '===================\n'

    a,b,c = dic['eth_hashing_rate'].split(';')
    sending_text += 'Eth : ' + str(float(a)/1000) + ' MH/s \n'
    a,b,c = dic['other_hashing_rate'].split(';')
    sending_text += 'Other : ' + str(float(a)/1000) + ' MH/s \n'
    sending_text += '===================\n'
    sending_text += 'Each GPU Speed \n'
    sending_text += '===================\n'
    a = dic['eth_each_hashing_rate'].split(';')
    b = dic['other_each_hashing_rate'].split(';')
    for x in range(0,len(a)):
        sending_text += 'GPU#' + str(x) + ' : ' + str(float(a[x])/1000) + ' MH/s - ' + str(float(b[x])/1000) + ' MH/s \n'

    sending_text += '===================\n'
    sending_text += 'Temp & Fan Speed \n'
    sending_text += '===================\n'
    c = dic['temp_fan_detail'].split(';')
    for x in range(0,len(c)-1,2):
        sending_text += 'GPU#' + str(x/2) + ' : ' + c[x] + u'\N{DEGREE SIGN}' + 'C - ' + c[x+1] + ' % \n'
    sending_text += '===================\n'

    return sending_text
# key = ['version', 'running_time', 'eth_hashing_rate', 'eth_each_hashing_rate', 'other_hashing_rate', 'other_each_hashing_rate', 'temp_fan_detail', 'pool', 'invalid']


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


class Worker(threading.Thread):
    ns = threading.local()
    interval = 1800
    def __init__(self, line_id):
        threading.Thread.__init__(self)
        self.line_id = line_id


    def run(self):

        # # self.ns.val = self.val
        # for i in range(5):
        #     self.ns.val = self.val+1
        #     print("Thread:", self.name, "value:", self.ns.val)
        #     time.sleep(2)

        while (True):

            return_text = get_data()
            send_line_notify(sending_text, self.line_id)
            time.sleep(self.interval)


    def set_name(self, new_name):
        self.setName(new_name)

    def set_val(self, new_val):
        self.val = new_val


    def get_data():

        r = requests.get(host + ':' + port)
        if r.status_code != 200:
            print('error can not get data!! = ' + str(r.status_code))
            return 'Can not get data\n Please check Miner !!'

        data = r.text
        p_data = process_data(data)

        return p_data


    def process_data(data):

        s_str = '{"result":'
        e_str = '<br><br>'
        dic = {}
        index1 = data.find(s_str)
        index2 = data.find(e_str, index1)
        # print index1, index2
        json_data = json.loads(data[index1:index2])
        json_data = json_data['result']


        for x in range(0,8):
            dic.update({key[x]:json_data[x]})

        # dic = {key[0]:json_data[0], key[1]: json_data[1], 'eth_hashing_rate': json_data[2], 'eth_each_hashing_rate': json_data[3], 'other_hashing_rate': json_data[4], 'other_each_hashing_rate': json_data[5], 'temp_fan_detail': json_data[6], 'pool': json_data[7], 'invalid': json_data[8]}

        sending_text = ''
        sending_text += '===================\n'
        sending_text += 'Total Speed\n'
        sending_text += '===================\n'

        a,b,c = dic['eth_hashing_rate'].split(';')
        sending_text += 'Eth : ' + str(float(a)/1000) + ' MH/s \n'
        a,b,c = dic['other_hashing_rate'].split(';')
        sending_text += 'Other : ' + str(float(a)/1000) + ' MH/s \n'
        sending_text += '===================\n'
        sending_text += 'Each GPU Speed \n'
        sending_text += '===================\n'
        a = dic['eth_each_hashing_rate'].split(';')
        b = dic['other_each_hashing_rate'].split(';')
        for x in range(0,len(a)):
            sending_text += 'GPU#' + str(x) + ' : ' + str(float(a[x])/1000) + ' MH/s - ' + str(float(b[x])/1000) + ' MH/s \n'

        sending_text += '===================\n'
        sending_text += 'Temp & Fan Speed \n'
        sending_text += '===================\n'
        c = dic['temp_fan_detail'].split(';')
        for x in range(0,len(c)-1,2):
            sending_text += 'GPU#' + str(x/2) + ' : ' + c[x] + u'\N{DEGREE SIGN}' + 'C - ' + c[x+1] + ' % \n'
        sending_text += '===================\n'

        return sending_text



if __name__ == '__main__':
    start()
