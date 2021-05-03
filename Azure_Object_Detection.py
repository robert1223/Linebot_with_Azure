from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import os
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont

from imgur_python import Imgur

def My_Object_Detection(url, filename):

    SUBSCRIPTION_KEY = os.getenv('Object_Detection_KEY')            
    ENDPOINT = os.getenv('Object_Detection_ENDPOINT')
    CV_CLIENT = ComputerVisionClient(
        ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY)
        )


    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    font_size = int(5e-2 * img.size[1])
    fnt = ImageFont.truetype(
      "./font/TaipeiSansTCBeta-Regular.ttf",  
      size=font_size)

    object_detection = CV_CLIENT.detect_objects(url) # create detection_object
    if len(object_detection.objects) > 0:
        for obj in object_detection.objects:
            left = obj.rectangle.x
            top = obj.rectangle.y
            right = obj.rectangle.x + obj.rectangle.w
            bot = obj.rectangle.y + obj.rectangle.h

            name = obj.object_property   # prediction of object

            confidence = obj.confidence  

            draw.rectangle(
              [left, top, right, bot],
              outline=(255, 0, 0), width=3)
            draw.text(
                [left, top + font_size],
                "{0} {1:0.1f}".format(name, confidence * 100),
                fill=(255, 0, 0),
                font=fnt,
            )

    img.save(filename)

    image = IMGUR_CLIENT.image_upload(filename, "title", "description")
    link = image["response"]["data"]["link"]

    os.remove(filename)
    return link


if __name__=="__main__":
	
	# 爬取網站圖片,並儲存於本地端 
    uri ='https://anntw-prod.s3.amazonaws.com/assets/images/000/020/997/big/crocodile-817680_640.jpg'
    res = requests.get(uri).content
    filename = './image/test.jpg'
    with open(filename,'wb') as f:
        f.write(res)
                       
    # 取得imgur相關資訊
    IMGUR_CONFIG = {
      "client_id": os.getenv('IMGUR_Client_ID'),
      "client_secret": os.getenv('IMGUR_Client_Secret'),
      "access_token": os.getenv('Postman_Access_Token'),
      "refresh_token": os.getenv('Postman_Refresh_token')
    }
    IMGUR_CLIENT = Imgur(config=IMGUR_CONFIG)

    image = IMGUR_CLIENT.image_upload(
      filename, "title", "description")
    url = image["response"]["data"]["link"]

    result = My_Object_Detection(url, filename)

    print(result)
