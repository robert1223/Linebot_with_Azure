from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
from io import BytesIO
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

def My_Description(url):


    SUBSCRIPTION_KEY = os.getenv('OCR_SUBSCRIPTION_KEY')
    ENDPOINT = os.getenv('OCR_ENDPOINT')
    CV_CLIENT = ComputerVisionClient(
        ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    )

    description_results = CV_CLIENT.describe_image(url)
    output = ""

    for caption in description_results.captions:
        output += "'{}' with confidence {:.2f}% \n".format(
            caption.text, caption.confidence * 100
        )

    return output 



if __name__=="__main__":


    url = "http://s2.foyuan.news/imgs/201810/23/4/15402836187765.jpeg"

    result = My_Description(url)

    print(result)