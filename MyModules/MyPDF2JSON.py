import requests
import json
import os
import time
from PyPDF2 import PdfFileWriter,PdfFileReader
from pathlib import Path
PROCESSING_DIRECTORY = os.path.dirname(__file__)[:-9]+"/Processing"

COMPUTER_VISION_ENDPOINT="https://i10x-aria-ocr-web-prd.cognitiveservices.azure.com/"
COMPUTER_VISION_SUBSCRIPTION_KEY="04d7161e703342b2a87a52c230e89229"

FORM_RECOGNIZER_ENDPOINT="https://cg-aria-fr-dev.cognitiveservices.azure.com/"
FORM_RECOGNIZER_SUBSCRIPTION_KEY="5c21a998d2ea4a6392b9a194153d3d77"
MODEL_ID="00a7a4ac-cbad-45d1-b454-366cc364e2c2"

def printt():
    print("hellp")

def GetFirst2Pages(file):
    part1 = PdfFileWriter()
    part1.addPage(file.getPage(0))
    part1.addPage(file.getPage(1))
    with open(PROCESSING_DIRECTORY+"/"+file.stream.filename[:-4] + "Part1.pdf", "wb") as output_file:
        part1.write(output_file)
def GetFRResult(file,filename):
    post_url = FORM_RECOGNIZER_ENDPOINT + "/formrecognizer/v2.1-preview.1/custom/models/%s/analyze" % MODEL_ID
    params = {
        "includeTextDetails": True
    }
    headers = {'Ocp-Apim-Subscription-Key': FORM_RECOGNIZER_SUBSCRIPTION_KEY,
               'Content-Type': 'application/pdf'}
    try:
        resp = requests.post(url=post_url, data=file, headers=headers, params=params)
        if resp.status_code != 202:
            print("POST analyze failed:\n%s" % json.dumps(resp.json()))
            quit()
        print("POST analyze succeeded:\n%s" % resp.headers)
        get_url = resp.headers["operation-location"]
    except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        quit()
    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    if (1 < 2):
        while n_try < n_tries:
            try:
                resp = requests.get(url=get_url,
                                    headers={"Ocp-Apim-Subscription-Key": FORM_RECOGNIZER_SUBSCRIPTION_KEY})
                resp_json = resp.json()
                if resp.status_code != 200:
                    print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                status = resp_json["status"]
                if status == "succeeded":
                    print("Analysis succeeded:\n%s" % json.dumps(resp_json))  # can be avoided
                    f = open(PROCESSING_DIRECTORY + "/" + filename[:-4] + "FRResult.json", "w+")
                    f.write(json.dumps(resp_json, indent=4))
                    f.close()
                    return resp_json
                if status == "failed":
                    print("Analysis failed:\n%s" % json.dumps(resp_json))
                # Analysis still running. Wait and retry.
                time.sleep(wait_sec)
                n_try += 1
                wait_sec = min(2 * wait_sec, max_wait_sec)
            except Exception as e:
                msg = "GET analyze results failed:\n%s" % str(e)
                print(msg)
                quit()
        print("Analyze operation did not complete within the allocated time.")
    if (resp_json != {}):
        return resp_json
def GetCGResult(file):
    text_recognition_url = COMPUTER_VISION_ENDPOINT + "/vision/v3.0/read/analyze"
    image_data = open(PROCESSING_DIRECTORY + "/" + file.filename, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': COMPUTER_VISION_SUBSCRIPTION_KEY,
               'Content-Type': file.content_type}
    response = requests.post(
        text_recognition_url, headers=headers, data=image_data)
    response.raise_for_status()
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
            print("Successfull ! goto JSON file for output")
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False
    if (analysis != {}):
        f = open(PROCESSING_DIRECTORY + "/" + file.filename[:-4] + "CGResult.json", "w+")
        f.write(json.dumps(analysis, indent=4))
        f.close()
        return analysis

def GetPDF2JSON(file,filename):
    CGResult=""
    PDFFile = PdfFileReader(file)
    if PDFFile.getNumPages()<=2:
        pdffile=open(PROCESSING_DIRECTORY+"/"+filename, "rb").read()
        FRResult=GetFRResult(pdffile,file.filename)
    else:
        GetFirst2Pages(PDFFile)
        filePart1 = open(PROCESSING_DIRECTORY+"/"+file.filename[:-4] + "Part1.pdf", "rb").read()
        FRResult=GetFRResult(filePart1,file.filename)
        CGResult=GetCGResult(file)
    return FRResult,CGResult
