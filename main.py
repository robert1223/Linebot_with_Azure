from flask import Flask, request, abort
import json

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from azure.cognitiveservices.vision.face import FaceClient

import sys
import time
import os
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
import time
import re

from imgur_python import Imgur


# import my package
import Azure_OCR
import Azure_Face_Recognition
import Azure_Object_Detection
import Azure_Description




# 取得imgur相關資訊
IMGUR_CONFIG = {
  "client_id": os.getenv('IMGUR_Client_ID'),
  "client_secret": os.getenv('IMGUR_Client_Secret'),
  "access_token": os.getenv('Postman_Access_Token'),
  "refresh_token": os.getenv('Postman_Refresh_token')
}
IMGUR_CLIENT = Imgur(config=IMGUR_CONFIG)




# 建立Flask
app = Flask(__name__)

# 讀取linebot資訊
# secretFile = json.load(open('./secretFile.txt', 'r'))

# 讀取Flex_Message 所需資料
flex_data = json.load(open('./flex_data.txt', 'r'))


# 讀取LineBot驗證資訊
line_bot_api = LineBotApi(os.getenv('Line_token')) # linebot token
handler = WebhookHandler(os.getenv('Line_secret')) # linebot secret



# Linebot接收訊息
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value: 驗證訊息來源
    signature = request.headers['X-Line-Signature']

    # get request body as text: 讀取訊息內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# linebot處理照片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):

    # 使用者傳送的照片
    Img_message_content = line_bot_api.get_message_content(event.message.id)
    
    
    # 照片儲存名稱
    ImageName = './image/'+ event.message.id + '.jpg'

    # 儲存照片
    with open(ImageName, 'wb')as f:
        for chunk in Img_message_content.iter_content(): # 用迴圈將linebot.models取出
            f.write(chunk)

    # 將圖片上傳到imgur
    image = IMGUR_CLIENT.image_upload(
    ImageName, "title", "description")
    Img_Url = image["response"]["data"]["link"]

    name = Azure_Face_Recognition.My_Recognition(filename)

    if name != "":
        now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
        output = "{0}, {1}".format(name, now)

    else:
        plate = Azure_OCR.My_OCR(Img_Url)
        link_ob = Azure_Object_Detection.My_Object_Detection(Img_Url, filename)
        if len(plate) > 0:
            output = "License Plate: {}".format(plate)
        else:
            output = Azure_Description.My_Description(link)
        link = link_ob

        # 讀取Flex_Message 所需資料
        flex_data = json.load(open('./flex_data.txt', 'r'))

        # 將flex meaasge內的url及text做更改
        flex_data['hero']['url']=link
        flex_data['body']['contents'][0]['text']=output

        LINE_BOT.reply_message(
        event.reply_token, [FlexSendMessage(alt_text="Report", contents=flex_data)]
    )


if __name__=="__main__":
    app.run()













