import datetime
import json
import os
import sys

import gspread
import requests
from flask import Flask, abort, request
from google.oauth2.service_account import credentials
from oauth2client.service_account import ServiceAccountCredentials as SAC

import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(settings.ACCOUNTBALANCE_ACCESS_TOKEN)
handler = WebhookHandler(settings.ACCOUNTBALANCE_SECRET)

@ app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text != "":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
        pass
    
        while True:
            try:
                scope = ['https://spreadsheets.google.com/feeds']
                gc = gspread.service_account(filename=settings.GDriveJSON)
                worksheet = gc.open_by_url(settings.sheet_url).worksheet('AccountBalance')
            except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)
            textt=""
            textt+=event.message.text
            if textt!="":
                json_str = json.dumps({datetime.date.today()}, default=str)
                worksheet.append_row((str(datetime.date.today()), textt))
                print('新增一列資料到試算表' ,settings.sheet_url)
                return textt

if __name__ == "__main__":
    app.run(debug=True,port=8000)