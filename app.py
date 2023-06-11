import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,  ButtonsTemplate, MessageTemplateAction

#引入model.py
from model import process_user_input

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text #獲取使用者輸入的文字

    if get_message.find('T') == -1:           
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='相似判決結果出爐',
                    text='請選擇想看的',
                    actions=[
                        MessageTemplateAction(
                            label='TCDV,109,婚,363,20200827,1',
                            text='TCDV,109,婚,363,20200827,1'
                        ),
                        MessageTemplateAction(
                            label='TPDV,107,婚,347,20190321,1',
                            text='TPDV,107,婚,347,20190321,1'
                        ),
                        MessageTemplateAction(
                            label='TPDV,108,婚,338,20200602,1',
                            text='TPDV,108,婚,338,20200602,1'
                        )
                    ]
                )
            )
        )
    else:     
        reply = process_user_input(get_message)

        # Send To Line
        line_bot_api.reply_message(  
            event.reply_token,
            TextSendMessage(text = f"{reply}")
        )
