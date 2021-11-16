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
    TextSendMessage,QuickReply, QuickReplyButton, 
    CameraAction, CameraRollAction, RichMenu, RichMenuArea,
    RichMenuSize, RichMenuBounds, URIAction
)
from linebot.models.actions import RichMenuSwitchAction
from linebot.models.rich_menu import RichMenuAlias

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


        # 回覆消息
        if event.message.text == "@發現走失犬":
            cls.line_bot_api.reply_message(
                event.reply_token,
                #template_message_dict.get(event.message.text)
                TextSendMessage(text='請選擇照片上傳方式', quick_reply=quickReplyList)
            )

        elif event.message.text == "@名冊":
            cls.line_bot_api.reply_message(
                event.reply_token,
                #template_message_dict.get(event.message.text)
                TextSendMessage(text='請點選名冊')
            )
        else:
            text = "請點選選單"
            cls.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
    
    
        # # Action 的 Rich Menu 樣板 A
        # areas.action.type: "richmenuswitch"
        # areas.action.richMenuAliasId: "richmenu-b"
        # areas.action.data: "richmenu=b"
        # # Action 的 Rich Menu 樣板 B
        # areas.action.type: "richmenuswitch"
        # areas.action.richMenuAliasId: "richmenu-a"
        # areas.action.data: "richmenu=a"


        # ## 名冊-全部
        # ListQuickReplyAll = QuickReplyButton(
        #     action=RichMenuSwitchAction(
        #         label="全部",
        #         rich_menu_alias_id= "richmenu-a",
        #         # data="richmenu-changed-to-b"
        #     )
        # )

        # ## 名冊-品種
        # ListQuickReplyVariety = QuickReplyButton(
        #     action=RichMenuSwitchAction(
        #         label="品種",
        #         rich_menu_alias_id= "richmenu-a",
        #         # data="richmenu-changed-to-b"
        #         )
        # )
        # ## 名冊-性別
        # ListQuickReplySex = QuickReplyButton(
        #     action=RichMenuSwitchAction(
        #         label="性別",
        #         rich_menu_alias_id= "richmenu-a",
        #         # data="richmenu-changed-to-b")
        # )

        # quickReplyList3 = QuickReply(
        #     items = [ListQuickReplyAll, ListQuickReplyVariety, ListQuickReplySex]
        # )

        #template_message_dict = {
        #  "@reply":quick_reply_pic,
        #}


class RichMenuSwitchAction:
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])


    @classmethod
        def rich_menu_object_a_json():
            return {
                "size": {
                    "width": 2500,
                    "height": 1686
                },
                "selected": False,
                "name": "richmenu-a",
                "chatBarText": "Tap to open",
                "areas": [
                    {
                        "bounds": {
                            "x": 0,
                            "y": 0,
                            "width": 1250,
                            "height": 1686
                        },
                        "action": {
                            "type": "uri",
                            "uri": "https://www.line-community.me/"
                        }
                    },
                    {
                        "bounds": {
                            "x": 1251,
                            "y": 0,
                            "width": 1250,
                            "height": 1686
                        },
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-alias-b",
                            "data": "richmenu-changed-to-b"
                        }
                    }
                ]
            }


        def rich_menu_object_b_json():
            return {
                "size": {
                    "width": 2500,
                    "height": 1686
                },
                "selected": False,
                "name": "richmenu-b",
                "chatBarText": "Tap to open",
                "areas": [
                    {
                        "bounds": {
                            "x": 0,
                            "y": 0,
                            "width": 1250,
                            "height": 1686
                        },
                        "action": {
                            "type": "richmenuswitch",
                            "richMenuAliasId": "richmenu-alias-a",
                            "data": "richmenu-changed-to-a"
                        }
                    },
                    {
                        "bounds": {
                            "x": 1251,
                            "y": 0,
                            "width": 1250,
                            "height": 1686
                        },
                        "action": {
                            "type": "uri",
                            "uri": "https://www.line-community.me/"
                        }
                    }
                ]
            }


        def create_action(action):
            if action['type'] == 'uri':
                return URIAction(type=action['type'], uri=action.get('uri'))
            else:
                return RichMenuSwitchAction(
                    type=action['type'],
                    rich_menu_alias_id=action.get('richMenuAliasId'),
                    data=action.get('data')
                )


        def main():
            # 2. Create rich menu A (richmenu-a)
            rich_menu_object_a = rich_menu_object_a_json()
            areas = [
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=info['bounds']['x'],
                        y=info['bounds']['y'],
                        width=info['bounds']['width'],
                        height=info['bounds']['height']
                    ),
                    action=create_action(info['action'])
                ) for info in rich_menu_object_a['areas']
            ]

            rich_menu_to_a_create = RichMenu(
                size=RichMenuSize(width=rich_menu_object_a['size']['width'], height=rich_menu_object_a['size']['height']),
                selected=rich_menu_object_a['selected'],
                name=rich_menu_object_a['name'],
                chat_bar_text=rich_menu_object_a['name'],
                areas=areas
            )

            rich_menu_a_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_a_create)

            # 3. Upload image to rich menu A
            with open('./public/richmenu-a.png', 'rb') as f:
                line_bot_api.set_rich_menu_image(rich_menu_a_id, 'image/png', f)

            # 4. Create rich menu B (richmenu-b)
            rich_menu_object_b = rich_menu_object_b_json()
            areas = [
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=info['bounds']['x'],
                        y=info['bounds']['y'],
                        width=info['bounds']['width'],
                        height=info['bounds']['height']
                    ),
                    action=create_action(info['action'])
                ) for info in rich_menu_object_b['areas']
            ]

            rich_menu_to_b_create = RichMenu(
                size=RichMenuSize(width=rich_menu_object_b['size']['width'], height=rich_menu_object_b['size']['height']),
                selected=rich_menu_object_b['selected'],
                name=rich_menu_object_b['name'],
                chat_bar_text=rich_menu_object_b['name'],
                areas=areas
            )

            rich_menu_b_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_b_create)

            # 5. Upload image to rich menu B
            with open('./public/richmenu-b.png', 'rb') as f:
                line_bot_api.set_rich_menu_image(rich_menu_b_id, 'image/png', f)

            # 6. Set rich menu A as the default rich menu
            line_bot_api.set_default_rich_menu(rich_menu_b_id)

            # 7. Create rich menu alias A
            alias_a = RichMenuAlias(
                rich_menu_alias_id='richmenu-alias-a',
                rich_menu_id=rich_menu_a_id
            )
            line_bot_api.create_rich_menu_alias(alias_a)

            # 8. Create rich menu alias B
            alias_b = RichMenuAlias(
                rich_menu_alias_id='richmenu-alias-b',
                rich_menu_id=rich_menu_b_id
            )
            line_bot_api.create_rich_menu_alias(alias_b)
            print('success')


        main()