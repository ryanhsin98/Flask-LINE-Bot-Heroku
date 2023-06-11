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
parser  = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['X-Line-Signature']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return abort(400)

 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
 
                if event.message.text == "我想離婚了，老公在大陸遲遲不回家":
 
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='相似判決結果出爐',
                                text='請選擇想了解的',
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
                    result = process_user_input(event.message.text)
 
                    line_bot_api.reply_message(  # 回應前五間最高人氣且營業中的餐廳訊息文字
                        event.reply_token,
                        TextSendMessage(text=result)
                    )
