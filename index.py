from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import os
import json


from apps.randomNumber import randomNumberMain


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)


# domain root
@app.route('/')
def home():
    return 'Hello, World!'


@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得「使用者」訊息
    user_message = event.message.text

    if user_message == '文字':
        # 設定「機器人」回覆訊息
        bot_message = "文字"
        # 發送訊息
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=bot_message))

    if user_message == '圖片':
        # 設定「機器人」回覆訊息
        bot_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/pu2S8SA.png',
            preview_image_url='https://i.imgur.com/pu2S8SA.png'
        )
        # 發送訊息
        line_bot_api.reply_message(event.reply_token, bot_message)

    if user_message == '亂數':
        # 設定「機器人」回覆訊息
        bot_message = randomNumberMain(0, 100)
        # 發送訊息
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=bot_message))

    if user_message == '讀取':
        # 讀取 JSON 檔案
        filename = '/tmp/data.json'
        data = read_JSON_data(filename)
        # 發送訊息
        replyLineMessage = TextSendMessage(str(data))
        line_bot_api.reply_message(event.reply_token, replyLineMessage)

    if user_message == '寫入':
        # 讀取 JSON 檔案
        filename = '/tmp/data.json'
        data = read_JSON_data(filename)
        # 寫入新資料
        newData = {"number": randomNumberMain(0, 100)}
        data.append(newData)
        write_JSON_data(filename, data)
        # 發送訊息
        replyLineMessage = TextSendMessage(str(data))
        line_bot_api.reply_message(event.reply_token, replyLineMessage)

    if user_message == '清除':
        # 寫入空白
        filename = '/tmp/data.json'
        data = []
        write_JSON_data(filename, data)
        # 發送訊息
        replyLineMessage = TextSendMessage(str(data))
        line_bot_api.reply_message(event.reply_token, replyLineMessage)

    else:
        # 設定「機器人」回覆訊息
        bot_message = "回傳文字：" + user_message
        # 發送訊息
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=bot_message))


if __name__ == "__main__":
    app.run()


# 讀取JSON資料
def read_JSON_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data


# 寫入JSON資料
def write_JSON_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)
