from flask import Flask, request, render_template
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

app = Flask(__name__)

line_bot_api = LineBotApi('nZCWA89uFKpYTnklDBwXUm6qYE7OgprVM/GJKQ5BPoGxvCDtNzhkERtzOieiVybu74w1y/J8IlnXQTPL4ruCzcQU/atrrhTYLadhYkYxGUBh0dQhpaqJ6rVeRpJtinzwPJAML6jwX2GS05OXYXvnDQdB04t89/1O/w1cDnyilFU=')


@app.route("/")
def hello():
    return render_template('html_demo.html', name=None)


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


@app.route('/bot/', methods=['POST'])
def bot_reply():
    if request.method == 'POST':
        print(request.data)


if __name__ == '__main__':
    app.run(port='5002')
