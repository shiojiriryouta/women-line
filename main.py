import config 
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,FlexSendMessage
)
import json


app = Flask(__name__)

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)    
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)    


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return
    
    if event.message.text == "食事投稿":
        reply = TextSendMessage(text="食事の画像を送ってくださいにゃん")
    elif event.message.text == "運動報告":
        container_obj = FlexSendMessage(alt_text = "運動報告をしてください",contents = sport_post)
        reply = container_obj
    elif event.message.text == "運動評価完了":
        reply = TextSendMessage(text="運動おつかれにゃん")
    elif event.message.text == "健康クイズ":
        reply = FlexSendMessage(alt_text = "健康クイズ",contents = quiz_test)
    elif event.message.text == "[2]":
        reply = FlexSendMessage(alt_text = "正解",contents = quiz_true)
    elif event.message.text == "[1]" or event.message.text == "[3]":
        reply = FlexSendMessage(alt_text = "不正解",contents = quiz_false)
    elif event.message.text == "ペットを見る":
        reply = FlexSendMessage(alt_text = "ペットの状態",contents = check_pet)
    else:
        reply = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        reply
    )

# 画像メッセージのハンドラ
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    reply = TextSendMessage(text="美味しそうな料理ですね")
    line_bot_api.reply_message(
        event.reply_token,
        reply
    )

check_pet = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://i.imgur.com/UDU7MpH.png",
        "size": "3xl",
        "aspectRatio": "13:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://line.me/"
        },
        "margin": "xl"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "ワイはまあまあ元気",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "text",
            "text": "Health Level",
            "margin": "sm",
            "size": "lg",
            "decoration": "none",
            "weight": "bold"
        },
        {
            "type": "box",
            "layout": "baseline",
            "contents": [
            {
                "type": "icon",
                "url": "https://icons.iconarchive.com/icons/designbolts/free-valentine-heart/48/Heart-icon.png",
                "margin": "sm"
            },
            {
                "type": "icon",
                "url": "https://icons.iconarchive.com/icons/designbolts/free-valentine-heart/48/Heart-icon.png",
                "margin": "sm"
            },
            {
                "type": "icon",
                "url": "https://icons.iconarchive.com/icons/designbolts/free-valentine-heart/48/Heart-icon.png",
                "margin": "sm"
            },
            {
                "type": "icon",
                "url": "https://cdn-icons-png.flaticon.com/256/1077/1077035.png",
                "margin": "sm"
            },
            {
                "type": "icon",
                "url": "https://cdn-icons-png.flaticon.com/256/1077/1077035.png",
                "margin": "sm"
            },
            {
                "type": "icon",
                "url": "https://cdn-icons-png.flaticon.com/256/1077/1077035.png",
                "margin": "sm"
            }
            ]
        },
        {
            "type": "separator"
        },
        {
            "type": "text",
            "text": "あさごはんが食べられて調子がいいにゃああああああああああああああああああああああああああああああああああああああああん",
            "wrap": True,
            "weight": "regular",
            "style": "normal",
            "decoration": "none",
            "align": "start",
            "scaling": True,
            "margin": "md"
        },
        {
            "type": "text",
            "text": "\nけどもっと食べたり運動したりしたいにゃあああああああああああああああああああああああああああああああああああああああああああああああん",
            "wrap": True
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "食事を投稿する",
            "text": "食事投稿"
            },
            "style": "primary",
            "height": "sm",
            "offsetTop": "none",
            "color": "#4374b9"
        },
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "運動を報告する",
            "text": "運動報告"
            },
            "style": "primary",
            "height": "sm",
            "offsetTop": "none",
            "color": "#4374b9"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        },
        {
            "type": "filler",
            "flex": 0
        }
        ],
        "flex": 0
    }
}
quiz_false = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://tyoudoii-illust.com/wp-content/uploads/2021/01/NG_woman_color.png",
        "size": "3xl",
        "aspectRatio": "10:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://line.me/"
        },
        "margin": "xl"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "text",
                "text": "✗",
                "weight": "bold",
                "size": "xl",
                "color": "#4374b9"
            },
            {
                "type": "text",
                "text": "不正解！",
                "weight": "bold",
                "size": "xl",
                "flex": 8
            }
            ]
        },
        {
            "type": "text",
            "text": "正解は[2] 運動器の障害です。\n\n運動器の障害のために移動機能の低下をきたした状態を 「ロコモティブシンドローム」＝ロコモといいます。",
            "wrap": True,
            "weight": "regular",
            "style": "normal",
            "decoration": "none",
            "align": "start",
            "scaling": True,
            "margin": "md"
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "uri",
            "label": "ロコモについて知る",
            "uri": "https://locomo-joa.jp/locomo"
            },
            "style": "primary",
            "height": "sm",
            "offsetTop": "none",
            "color": "#e84f16"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        },
        {
            "type": "filler",
            "flex": 0
        }
        ],
        "flex": 0
    }
}

quiz_true = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://tyoudoii-illust.com/wp-content/uploads/2024/07/oksign_woman_color.png",
        "size": "4xl",
        "aspectRatio": "12:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://line.me/"
        },
        "margin": "xl"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "text",
                "text": "○",
                "weight": "bold",
                "size": "xl",
                "color": "#4374b9"
            },
            {
                "type": "text",
                "text": "正解！",
                "weight": "bold",
                "size": "xl",
                "flex": 8
            }
            ]
        },
        {
            "type": "text",
            "text": "要支援、要介護になる原因のトップは転倒、骨折や関節の病気など運動器の故障です。\n\n運動器の障害のために移動機能の低下をきたした状態を 「ロコモティブシンドローム」＝ロコモといいます。厚生労働省2019年国民生活基礎調査では要介護・要支援のとなった人の24.8%の原因が運動器の障害となっています。",
            "wrap": True,
            "weight": "regular",
            "style": "normal",
            "decoration": "none",
            "align": "start",
            "scaling": True,
            "margin": "md"
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "action": {
            "type": "uri",
            "label": "ロコモについて知る",
            "uri": "https://locomo-joa.jp/locomo"
            },
            "style": "primary",
            "height": "sm",
            "offsetTop": "none",
            "color": "#e84f16"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        },
        {
            "type": "filler",
            "flex": 0
        }
        ],
        "flex": 0
    }
}

quiz_test = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://soco-st.com/wp-content/uploads/2022/04/settled_senior_13166_color.png?modified=1659869088",
        "size": "full",
        "aspectRatio": "22:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://line.me/"
        },
        "margin": "xl"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "健康クイズ",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "text",
            "text": "高齢者が要支援・要介護になる原因で最も多いのは次のうちどれ？",
            "wrap": True,
            "weight": "regular",
            "style": "normal",
            "decoration": "none",
            "align": "start",
            "scaling": True,
            "margin": "md"
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "[1] 高齢による衰弱",
            "text": "[1]"
            },
            "color": "#4374b9"
        },
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "[2] 運動器の障害",
            "text": "[2]"
            },
            "color": "#4374b9"
        },
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "[3]認知症",
            "text": "[3]"
            },
            "style": "primary",
            "height": "sm",
            "offsetTop": "none",
            "color": "#4374b9"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        },
        {
            "type": "filler",
            "flex": 0
        }
        ],
        "flex": 0
    }
}

sport_post = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://tyoudoii-illust.com/wp-content/uploads/2021/03/preparatorymovement_woman_%E3%82%B5%E3%83%A0%E3%83%8D.png",
        "size": "full",
        "aspectRatio": "13:13",
        "aspectMode": "cover",
        "action": {
        "type": "uri",
        "uri": "https://line.me/"
        },
        "margin": "xl"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "運動の評価",
            "weight": "bold",
            "size": "xl"
        },
        {
            "type": "text",
            "text": "本日行った運動を運動量に応じて評価してください",
            "wrap": True,
            "weight": "regular",
            "style": "normal",
            "decoration": "none",
            "align": "start",
            "scaling": True,
            "margin": "md"
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "text",
                "text": "3~4時間のランニング程度",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
            ]
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "text",
                "text": "1~2時間のランニング程度",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
            ]
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "text",
                "text": "数十分のランニング程度",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
            ]
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "text",
                "text": "数十分のウォーキング程度",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
            ]
        },
        {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            },
            {
                "type": "text",
                "text": "家の中で歩き回った程度",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
            ]
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "★★★★★",
            "text": "運動評価完了"
            }
        },
        {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "★★★★☆",
            "text": "運動評価完了"
            }
        },
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "★★★☆☆",
            "text": "運動評価完了"
            },
            "style": "primary",
            "height": "sm",
            "offsetTop": "none"
        },
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "★★☆☆☆",
            "text": "運動評価完了"
            },
            "position": "relative",
            "style": "primary",
            "height": "sm"
        },
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "★☆☆☆☆",
            "text": "運動評価完了"
            },
            "style": "primary",
            "height": "sm"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        },
        {
            "type": "filler",
            "flex": 0
        }
        ],
        "flex": 0
    }
}
if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)

