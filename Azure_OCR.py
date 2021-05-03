from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
import time
import os
import re


def My_OCR(url):

    SUBSCRIPTION_KEY = os.getenv('OCR_SUBSCRIPTION_KEY')
    ENDPOINT = os.getenv('OCR_ENDPOINT')
    CV_CLIENT = ComputerVisionClient(
        ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    )

    ocr_results = CV_CLIENT.read(url, raw=True)
    operation_location_remote = ocr_results.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]


    status = ["notStarted", "running"]
    while True:
        get_handw_text_results = CV_CLIENT.get_read_result(operation_id)
        if get_handw_text_results.status not in status:
            break
        time.sleep(1)


    succeeded = OperationStatusCodes.succeeded

    text=[]
    if get_handw_text_results.status == succeeded:
        res = get_handw_text_results.analyze_result.read_results
        for text_result in res:
            for line in text_result.lines:
                if len(line.text) <= 8:
                    text.append(line.text)

    r = re.compile("[0-9A-Z]{2,4}[.-]{1}[0-9A-Z]{2,4}")
    text = list(filter(r.match, text))      


    return text[0].replace('.', '-') if len(text) > 0 else ""


if __name__=="__main__":


    url = "http://s2.foyuan.news/imgs/201810/23/4/15402836187765.jpeg"

    result = My_OCR(url)

    print(result)