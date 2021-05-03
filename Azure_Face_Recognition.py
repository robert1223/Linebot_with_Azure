import sys
import time
from io import BytesIO
from PIL import Image, ImageDraw
import json
import requests
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType
import os
from imgur_python import Imgur



def My_Recognition(filename):

	KEY = os.getenv('Azure_Face_Key')
	ENDPOINT = os.getenv('Azure_Face_Endpoint')
	FACE_CLIENT = FaceClient(
	  ENDPOINT, CognitiveServicesCredentials(KEY))


	# 人臉辨識
	img = open(filename, "r+b")
	detected_face = FACE_CLIENT.face.detect_with_stream(
	    img, detection_model="detection_01"
	)

	# 指定要在哪個group做比對
	PERSON_GROUP_ID = "ceb102"

	# 臉部服務會給每一張偵測到的臉一個face ID,若照片沒有比對到人臉,則不會出現face ID
	try:
	    results = FACE_CLIENT.face.identify(
	      [detected_face[0].face_id], PERSON_GROUP_ID)
	    result = results[0].as_dict()

	    # 先判斷信心水準是否大於5成
	    try:
	        confidence = result["candidates"][0]['confidence']
	        if confidence > 0.5:
	            # 如果在資料庫中有找到相像的人，會給予person ID
	            # 再拿此person ID去查詢名字
	            Indentified_Result = FACE_CLIENT.person_group_person.get(
	                                PERSON_GROUP_ID, result["candidates"][0]["person_id"]
	                                ).name
	            
	            return Indentified_Result
	        else:
	            Indentified_Result = "Maybe he/she is {}, but I'm not sure."
	            
	            return Indentified_Result

	    except IndexError:
	        Indentified_Result = 'I know he/she is a person, but I dont know him/her.'
	        
	        return Indentified_Result

	except IndexError:
	    Indentified_Result = ''
		

	    return Indentified_Result


if __name__=="__main__":


    filename = 'cat.jpg'

    result = My_Recognition(filename)

    print(result)