import requests
import time

api_link = 'https://l2ig-alert-line-bot.herokuapp.com/'

def keep_alive():
    while True:
        r = requests.get(api_link)
        if r.status_code != 200 or r.text.find('error') != -1:
            print('error = ' + str(r.status_code) + ' \n ' + str(r.text.find('error')))
            return -1

        time.sleep(300)


if __name__ == '__main__':
    keep_alive()
