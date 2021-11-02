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
    def line_user_upload_video(cls,event):

        ## CameraAction
        cameraQuickReplyButton = QuickReplyButton(action=CameraAction(label="拍照"))

        ## 點擊後，切換至照片相簿選擇
        cameraRollQRB = QuickReplyButton(action=CameraRollAction(label="選擇照片"))

        ## 設計QuickReplyButton的List
        quickReplyList = QuickReply(
            items = [cameraQuickReplyButton, cameraRollQRB]
        )
        quick_reply_pic = TextSendMessage(text='請選擇照片上傳方式', quick_reply=quickReplyList)
        
        template_message_dict = {
          "＠發現走失犬":quick_reply_pic,
        }

        # 回覆消息
        if(event.message.text.find('@')!= -1):
            cls.line_bot_api.reply_message(
                event.reply_token,
                template_message_dict.get(event.message.text)
            )
    