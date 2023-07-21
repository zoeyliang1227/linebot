import datetime
import json
import sys

import pandas as pd
import psycopg2
import pygsheets
from flask import Flask, abort, request

import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(settings.ACCOUNTBALANCE_ACCESS_TOKEN)
handler = WebhookHandler(settings.ACCOUNTBALANCE_SECRET)
IncomeType = ['薪水']
ExpenditureType = ['午餐']

conn = psycopg2.connect(database=settings.DATEBASE, user=settings.USER, password=settings.PASSWORD, host=settings.HOST, port=settings.PORT)
cursor = conn.cursor()

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
                gc = pygsheets.authorize(service_file=settings.GDriveJSON)
                sht = gc.open_by_url(settings.sheet_url).worksheet('title', settings.GSpreadSheet)
                sht.frozen_rows = 1
                
                
            except Exception as ex:
                print('無法連線Google試算表', ex)
                sys.exit(1)
            textt = ""
            textt += event.message.text
            if textt == '加工作表':
                sht.add_worksheet('title')    #加sheet

            elif textt == '列出工作表':
                wks_list = sht.worksheets() #全部sheet
                print(wks_list)

            elif textt == '讀資料':
                A1 = sht.cell('A1')
                print(A1)
                print(A1.value)

            elif textt != "":
                textt = textt.split(" ")
                print(textt)
                if textt[0] in ExpenditureType:
                    textt[1] = '-'+ textt[1]
                json_str = json.dumps({datetime.date.today()}, default=str)
                values = [[str(datetime.date.today()), textt[0], textt[1]]]
                cursor.execute("INSERT INTO ACCOUNTBALANCE (DATETIME,COST,REVENUE,EXPENDITURE,SALARY) VALUES (%s, %s, %s, %s, %s);", ('2023/07/07', 120, 0, '午餐', 0 ))
                print('000')
                # insert_rows = 1 # add start from 2
                # sht.insert_rows(insert_rows, number=1, values=values) 
                # sht.append_table(values=values)
                # if (textt[0] not in IncomeType) or (textt[0] not in ExpenditureType):
                #     df1 = pd.DataFrame({'時間':str(datetime.date.today()), textt[0]: [textt[1]]})
                
                all_values = sht.get_all_values()
                print(sht.get_row(all_values, returnas='matrix', include_tailing_empty=True, **kwargs))
                if (textt[0] not in all_values[0]) or (textt[0] not in all_values[0]):
                    df1 = pd.DataFrame({'時間':str(datetime.date.today()), textt[0]: [textt[1]]})
                sht.set_dataframe(df1, 'A1', copy_index=False, nan='')
                print('新增一列資料到試算表' ,str(datetime.date.today()), account_type, textt)
                # worksheet.export(pygsheets.ExportType.CSV, 'accountbalance')        #output
                # sht.share(settings.email)   #send email
                return textt




if __name__ == "__main__":
    app.run(debug=True,port=8000)