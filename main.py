import os
from flask import Flask, abort, request
from linebot.v3.webhook import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)


app = Flask(__name__)

handler = WebhookHandler('7a3925e8912d4270678e1f9f4523e1d5')
configuration = Configuration(access_token='CS1Ne2sz1cKWnpQMFn0ZKsgJa70r/1wdBOQgCCnI0I+j+2cugXO6fsVqLF6wZTIWXtQNjNWyx1UVh6k9hZ3Kv09ZzPwPwJn0ssf+TDxM17ma91WzMi43ZxCD0M1flRzkTwTyMQeL2NhLUkIcVcEmIgdB04t89/1O/w1cDnyilFU=')


@app.route("/callback", methods=['POST'])
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        #相手の送信した内容で条件分岐して回答を変数に代入
        if event.message.text == 'グー':
          msg = 'パー'
        elif event.message.text == 'チョキ':
          msg = 'グー'
        elif event.message.text == 'パー':
          msg = 'チョキ'
        elif event.message.text == '食事登録':
          msg = "食事の画像を送ってください"
        elif event.message.text == '運動投稿':
          msg = "運動を評価してください"
        else:
          msg = 'ごめんね。\nまだ他のメッセージには対応してないよ'

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
          ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=msg)]
            )
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
