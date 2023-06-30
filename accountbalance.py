import os

from flask import Flask, abort, request

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
    if event.message.text =='a':
        msg = (TextSendMessage(text='這是測試'))
        line_bot_api.reply_message(event.reply_token, msg)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)