'''

用戶上傳文字訊息時，控制LineBot 進行功能回覆

'''

from models.user import User
from flask import Request
from linebot import (
    LineBotApi
)

import os
from daos.user_dao import UserDAO
from linebot.models import (
    TextSendMessage,QuickReply, QuickReplyButton, CameraAction, CameraRollAction
)


# 圖片下載與上傳專用
import urllib.request
from google.cloud import storage


class MessageService:
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    '''
    用戶上傳照片
    將照片取回
    將照片存入CloudStorage內
    '''
    @classmethod
    def line_user_message(cls,event):

        ## CameraAction
        cameraQuickReplyButton = QuickReplyButton(
            action=CameraAction(label="拍照")
        )

        ## 點擊後，切換至照片相簿選擇
        cameraRollQRB = QuickReplyButton(
            action=CameraRollAction(label="選擇照片")
        )

        ## 設計QuickReplyButton的List
        quickReplyList = QuickReply(
            items = [cameraQuickReplyButton, cameraRollQRB]
        )
        quick_reply_pic = TextSendMessage(text='請選擇照片上傳方式', quick_reply=quickReplyList)
        
        #template_message_dict = {
        #  "@reply":quick_reply_pic,
        #}

        # 回覆消息
        if event.message.text == "@發現走失犬":
            cls.line_bot_api.reply_message(
                event.reply_token,
                #template_message_dict.get(event.message.text)
                TextSendMessage(text='請選擇照片上傳方式', quick_reply=quickReplyList)
            )
        else:
            text = "請點選選單"
            cls.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
    
    

    '''
    用戶點選快速選單
    選擇需要的品種
    顯示近10筆走失犬資料
    '''
    @classmethod
    def line_user_message(cls,event):

        ## 全部
        ListQuickReplyAll = QuickReplyButton(
            action=richmenuAction(label="全部")
        )

        ## 品種
        ListQuickReplyVariety = QuickReplyButton(
            action=richmenuAction(label="品種")
        #     {
        #       "size": {
        #         "width": 2500,
        #         "height": 1686
        #       },
        #       "selected": true,
        #       "name": "品種",
        #       "chatBarText": "查看更多資訊",
        #       "areas": [
        #         {
        #           "bounds": {
        #             "x": 53,
        #             "y": 34,
        #             "width": 431,
        #             "height": 325
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "法鬥"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 528,
        #             "y": 19,
        #             "width": 441,
        #             "height": 340
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "吉娃娃"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 1008,
        #             "y": 19,
        #             "width": 426,
        #             "height": 330
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "臘腸"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 1502,
        #             "y": 29,
        #             "width": 446,
        #             "height": 359
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "馬爾濟斯"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 2064,
        #             "y": 34,
        #             "width": 388,
        #             "height": 412
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "哈士奇"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 58,
        #             "y": 388,
        #             "width": 412,
        #             "height": 465
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "柯基"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 509,
        #             "y": 383,
        #             "width": 412,
        #             "height": 479
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "博美"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 988,
        #             "y": 397,
        #             "width": 446,
        #             "height": 465
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "貴賓"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 1483,
        #             "y": 417,
        #             "width": 416,
        #             "height": 474
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "柴犬"
        #           }
        #         },
        #         {
        #           "bounds": {
        #             "x": 1953,
        #             "y": 494,
        #             "width": 513,
        #             "height": 412
        #           },
        #           "action": {
        #             "type": "message",
        #             "text": "返回選單"
        #           }
        #         }
        #       ]
        #     }
        # )

        ## 性別
        ListQuickReplySex = QuickReplyButton(
            action=richmenuAction(label="性別")
        )

        quickReplyList3 = QuickReply(
            items = [ListQuickReplyAll, ListQuickReplyVariety, ListQuickReplySex]
        )

        # 回覆消息
        if event.message.text == "@名冊":
            cls.line_bot_api.reply_message(
                event.reply_token,
                #template_message_dict.get(event.message.text)
                TextSendMessage(text='請點選名冊', quick_reply=quickReplyList3)
            )
        else:
            text = "請點選選單"
            cls.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
    
