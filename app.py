import os
import json
import pandas as pd
# from io import StringIO
# import csv
# from numpy import random
# import numpy as np
from flask import Flask, render_template, send_from_directory, redirect, flash, request, jsonify,make_response
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader
from MyModules import MyPDF2JSON,MyJSON2LoLTables,MyLoL2CSVConcurr,MyTable,MyLoL2PDF

INPUT_ALLOWED_EXTENSIONS={ 'pdf'}# 'png', 'jpg', 'jpeg' also supported but want to change in GetPDF2JSON
OUTPUT_DIRECTORY = os.path.dirname(__file__)+"/Output"
PROCESSING_DIRECTORY = os.path.dirname(__file__)+"/Processing"
generalDetails={}
allTables={}
def ProcessFile(file):
    CGResult=''
    if (not os.path.isdir(OUTPUT_DIRECTORY)):
        os.makedirs(OUTPUT_DIRECTORY)
    filename = secure_filename(file.filename)
    file.save(os.path.join(PROCESSING_DIRECTORY, filename))
    if os.path.exists(PROCESSING_DIRECTORY + '/' + file.filename[:-4] + 'FRResult.json'):
        PDFFile = PdfFileReader(file)
        with open(PROCESSING_DIRECTORY + '/' + file.filename[:-4] + 'FRResult.json') as f:
            FRResult = json.load(f)
        if PDFFile.getNumPages()>2:
            with open(PROCESSING_DIRECTORY + '/' + file.filename[:-4] + 'CGResult.json') as f:
                CGResult = json.load(f)
    else:
        FRResult,CGResult=MyPDF2JSON.GetPDF2JSON(file,filename)
    global generalDetails
    global allTables
    generalDetailsJSON,overviewJSON,allTables=MyJSON2LoLTables.GetTableFromJSON(CGResult,FRResult,filename)
    generalDetails=generalDetailsJSON
    file.save(os.path.join(OUTPUT_DIRECTORY, filename))
    return filename

app = Flask(__name__)
@app.route('/reconcile/<filename>')
def reconcile(filename):
    # df=pd.read_csv(OUTPUT_DIRECTORY+"/"+filename+"Reconciled.csv")
    # tab=df.style.format('<input name="df" value="{}" />').hide_index().render()
    return render_template('reconcile.html',generalDetails=generalDetails,allTables=allTables,filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("Processing",
                               filename)
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory("Output",
                               filename)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allowedfile', methods=['GET', 'POST'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in INPUT_ALLOWED_EXTENSIONS
@app.route('/downloadPDF/<filename>', methods=['GET', 'POST'])
def download_pdf(filename):
    if request.method == 'POST':
        df = pd.DataFrame(request.values.lists())
        allTables=df.values.tolist()
        fileName=MyLoL2PDF.getPDFLoL(allTables,filename)
        return fileName+"Final.pdf"
    return "MYerrorPDF"
@app.route('/downloadCSV/<filename>', methods=['GET', 'POST'])
def download_csv(filename):
    if request.method == 'POST':
        df = pd.DataFrame(request.values.lists())
        allTables=df.values.tolist()
        csvLoL=MyLoL2CSVConcurr.getCSVLoL(allTables)
        MyTable.saveToCSV(csvLoL,filename+"Concurr")
        # si = StringIO()
        # cw = csv.writer(si)
        # cw.writerows(csvLoL)
        # output = make_response(si.getvalue())
        # output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        # output.headers["Content-type"] = "application/csv"
        # return output
        return filename+"Concurr.csv"
    return "MyerrorCSV"
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename=ProcessFile(file)
            #filename="G1341_IV31905.pdf"
            return jsonify(filename=filename[:-4])
    return ''


if __name__ == '__main__':
    app.run()
    app.debug=True
