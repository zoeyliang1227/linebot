import datetime
import json
import os
import re
import sys
import time

import gspread
import pandas as pd
import pygsheets
import requests
from bs4 import BeautifulSoup as bs
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
    signature = request.headers['X-Line-Signature']     # get X-Line-Signature header value
    body = request.get_data(as_text=True)       # get request body as text
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)     # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text != "":    #event.message.text 取得使用者輸入的文字
        account_type = line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f"收到 {event.message.text}，請問種類?"))
        pass
    
        while True:
            try:
                scope = ['https://spreadsheets.google.com/feeds']
                gc = gspread.service_account(filename=settings.GDriveJSON)
                print('132')
                worksheet = gc.open_by_url(settings.sheet_url).worksheet(settings.GSpreadSheet)
                
            except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)
            textt=""
            textt+=event.message.text
            textt = textt.split(",")
            Name = textt[0]
            Price = textt[1]
            if textt!="":
                json_str = json.dumps({datetime.date.today()}, default=str)
                worksheet.append_row((str(datetime.date.today()), textt))
                print('新增一列資料到試算表' ,str(datetime.date.today()), account_type, textt)
                return textt


if __name__ == "__main__":
    app.run(debug=True,port=8000)