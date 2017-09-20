# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os


app = Flask(__name__)

line_bot_api = LineBotApi('nZCWA89uFKpYTnklDBwXUm6qYE7OgprVM/GJKQ5BPoGxvCDtNzhkERtzOieiVybu74w1y/J8IlnXQTPL4ruCzcQU/atrrhTYLadhYkYxGUBh0dQhpaqJ6rVeRpJtinzwPJAML6jwX2GS05OXYXvnDQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ea522a6ca14dfe8c11571cf33d8ffe12') #Your Channel Secret


@app.route('/', methods=['GET'])
def get():
    return 'get'

@app.route("/callback/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print('host ================== '+ request.host)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    user_id = event.source.user_id
    ack_text = text

    if  text.lower() == 'start':
        pass

    if text.lower() == 'kuy':
        ack_text = 'fuck you kuy \n' + str(event.source.user_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ack_text)) #reply the same message from user



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


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
