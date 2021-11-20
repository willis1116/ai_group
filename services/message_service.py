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
import pygsheets

# 圖片下載與上傳專用
import urllib.request
from google.cloud import storage

# 查詢表單
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from tabulate import tabulate

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
        reply_arr = []
        reply_arr.append(TextSendMessage(text = '請提示訊息依序填入資訊'))
        reply_arr.append(TextSendMessage(text = '請問狗狗的品種(開頭請加上"#")'))
        reply_arr.append(TextSendMessage(text = '品種輸入範例: #柴犬'))


        # 回覆消息
        if event.message.text == "@發現走失犬":
            cls.line_bot_api.reply_message(
                event.reply_token,
                quick_reply_pic
            )

        elif event.message.text == '@登記走失愛犬' :
            cls.line_bot_api.reply_message(
                event.reply_token,
                reply_arr
            )

        elif event.message.text == '@查詢':
            cls.line_bot_api.reply_message(
                event.reply_token,
                reply_arr
            )
        elif event.message.text.find('#') == 0:
            #開啟sheet
            auth_json_path = 'ai-group-33566.json' #由剛剛建立出的憑證，放置相同目錄以供引入
            gss_scopes = ['https://spreadsheets.google.com/feeds'] #我們想要取用的範圍
            credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path, gss_scopes)
            gss_client = gspread.authorize(credentials)
            
            #從剛剛建立的sheet，把網址中 https://docs.google.com/spreadsheets/d/〔key〕/edit 的 〔key〕的值代入 
            spreadsheet_key_path = '188vbt-Dj2M_JlIOHD4ffQfORckPu6BVdQpie2GQGYhI'
            
            #透過open_by_key這個method來開啟sheet
            sheet = gss_client.open_by_key(spreadsheet_key_path).sheet1
            df = pd.DataFrame(sheet.get_all_records())
            #搜尋名字
            breed = event.message.text.lstrip('#')
            filt_value = ['寵物名字', '寵物性別', '寵物品種']
            filt = (df['寵物品種'] == breed)
            df_output = df.loc[filt, filt_value].set_index('寵物品種')
            reply_text = str(tabulate(df_output,headers='keys', tablefmt='psql'))
            cls.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(reply_text)
            )
        else:
            text = "請點選選單"
            cls.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )

      
