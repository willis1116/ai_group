'''

用戶上傳照片時，將照片從Line取回，放入CloudStorage

瀏覽用戶目前擁有多少張照片（未）

'''

from models.user import User
from flask import Request
from linebot import (
    LineBotApi
)

import os
from daos.user_dao import UserDAO
from linebot.models import (
    TextSendMessage
)


# 圖片下載與上傳專用
import urllib.request
from google.cloud import storage

# 圖像辨識
import tensorflow.keras
import cv2
from PIL import Image, ImageOps
import numpy as np
import time

import os

from utils.reply_send_message import detect_json_array_to_new_message_array

#model = tensorflow.keras.models.load_model('converted_savedmodel/model.savedmodel')

class ImageService:
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    '''
    用戶上傳照片
    將照片取回
    將照片存入CloudStorage內
    '''
    @classmethod
    def line_user_upload_image(cls,event):

        # 取出照片
        image_blob = cls.line_bot_api.get_message_content(event.message.id)
        temp_file_path=f"""{event.message.id}.png"""

        #
        with open(temp_file_path, 'wb') as fd:
            for chunk in image_blob.iter_content():
                fd.write(chunk)

        # 上傳至bucket
        storage_client = storage.Client()
        bucket_name = os.environ['USER_INFO_GS_BUCKET_NAME']
        destination_blob_name = f'{event.source.user_id}/image/{event.message.id}.png'
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(temp_file_path)

        # 載入模型Label
        '''
        載入類別列表
        '''
        class_names = []
        with open('converted_savedmodel/dogbreeds.names', "r") as f:
            class_names = [cname.strip() for cname in f.readlines()]

        #填入檔案名稱
        img = cv2.imread(temp_file_path)

        #載入模型
        net = cv2.dnn.readNet("converted_savedmodel/model.savedmodel/yolov4-tiny_best.weights", "converted_savedmodel/model.savedmodel/yolov4-tiny.cfg")
        
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1/255)
           
        
        classes, scores, boxes = model.detect(img, 0.1, 0.2)
        max_score = scores.max()
        max_num = np.argmax(scores)
        n = "\n"
        result_message = '圖片大小: '+ str(img.shape) + n
        text = ""
        
        for (classid, score, box) in zip(classes, scores, boxes):
            label = f"{class_names[int(classid)]}"
            text = text + f'偵測結果:{label} 分數:{score} 位置"{box}{n}'

 
        if len(classes) !=  0:
            send_message = result_message + text
            cls.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(send_message)
            )
        else:
            cls.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(f"""圖片無法辨識出狗，圖片已存入圖庫，後續提供資訊給您""")
            )
            
        # 移除本地檔案
        os.remove(temp_file_path)