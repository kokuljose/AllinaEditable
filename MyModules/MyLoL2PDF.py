from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger
def getTabFromList(list):
    tab=[]
    row=[]
    k=0
    l=len(list)/5
    f=""
    for i in range(0,int(len(list)/5)):
        for j in range(0,5):
            row.append(list[k])
            k=k+1
        tab.append(row)
        row=[]
    return tab
def getSumofList(myList,colNum):
    sum=0
    for row in myList:
        val=row[colNum]
        if ',' in val:
            val=val.replace(',','')
        if val.count(".")>1:
            val=val.strip(".")
        val=val.replace("(","")
        val = val.replace(")", "")
        val = val.replace("$", "")
        if val!= '':
            sum=sum+float(val)
    return round(sum,2)
def append2Cols(table):
    tab=[]
    for row in table:
        newRow=row
        newRow.extend(["", ""])
        tab.append(newRow)
    return tab
def getGeneralDetails(tab):
    return [[tab[3][1][0],"","","","","",""],["Invoice "+tab[4][1][0],"","","","","",""],[tab[1][1][0],"","","","","",""],[tab[6][1][0],"","","","","",""]]

def getTabDetails(allTables):
    table=[]
    generalDetails=getGeneralDetails(allTables[:-10])
    rebateTab=getTabFromList(allTables[12][1])
    rebateTotal=getSumofList(rebateTab,4)
    rebateHead=["Deposit/Credits", '', '', '', '',rebateTotal , rebateTotal]
    roomTab=getTabFromList(allTables[14][1])
    roomTotal=getSumofList(roomTab,4)
    roomHead = ["Room & Tax", '', '', '', '', roomTotal, roomTotal]
    foodTab=getTabFromList(allTables[16][1])
    foodTotal=getSumofList(foodTab,4)
    foodHead = ["Food & Beverage", '', '', '', '', foodTotal, foodTotal]
    avTab = getTabFromList(allTables[18][1])
    avTotal=getSumofList(avTab,4)
    avHead = ["Audio Visual", '', '', '', '', avTotal, avTotal]
    miscTab = getTabFromList(allTables[20][1])
    miscTotal=getSumofList(miscTab,4)
    miscHead = ["Miscellaneous", '', '', '', '', miscTotal, miscTotal]
    # table.extend(generalDetails)
    # table.append(rebateHead)
    # table.extend(append2Cols(rebateTab))
    # table.append(roomHead)
    # table.extend(append2Cols(roomTab))
    # table.append(foodHead)
    # table.extend(append2Cols(foodTab))
    # table.append(avHead)
    # table.extend(append2Cols(avTab))
    # table.append(miscHead)
    # table.extend(append2Cols(miscTab))
    rebateTab.insert(0,rebateHead)
    roomTab.insert(0,roomHead)
    foodTab.insert(0,foodHead)
    avTab.insert(0,avHead)
    miscTab.insert(0,miscHead)
    return generalDetails,rebateTab,roomTab,foodTab,avTab,miscTab
def splitPDF(filename,page_number):
    pdf_reader = PdfFileReader(open("Processing/"+filename+".pdf", "rb"))
    try:
        assert page_number < pdf_reader.numPages
        pdf_writer1 = PdfFileWriter()
        pdf_writer2 = PdfFileWriter()

        for page in range(page_number):
            pdf_writer1.addPage(pdf_reader.getPage(page))

        for page in range(page_number,pdf_reader.getNumPages()):
            pdf_writer2.addPage(pdf_reader.getPage(page))

        with open("Output/"+filename+"part1.pdf", 'wb') as file1:
            pdf_writer1.write(file1)

        with open("Output/"+filename+"part2.pdf", 'wb') as file2:
            pdf_writer2.write(file2)

    except AssertionError as e:
        print("Error: The PDF you are cutting has less pages than you want to cut!")
def getPDFLoL(allTables,filename):
    generalDetails,rebateTab,roomTab,foodTab,avTab,miscTab = getTabDetails(allTables)
    fileName="Output/"+filename+"Reconciled.pdf"
    pdf=SimpleDocTemplate(
        fileName,pagesize=A4
    )
    GenTab=Table(generalDetails,[140*mm,10*mm, 10*mm, 10*mm, 10*mm, 10*mm, 10*mm])
    RebateTable=Table(rebateTab,colWidths=(36*mm,36*mm, 18*mm, 28*mm, 28*mm, 25*mm, 25*mm))
    RoomTable=Table(roomTab,colWidths=(36*mm,36*mm, 18*mm, 28*mm, 28*mm, 25*mm, 25*mm))
    FoodTable=Table(foodTab,colWidths=(36*mm,36*mm, 18*mm, 28*mm, 28*mm, 25*mm, 25*mm))
    AVTable=Table(avTab,colWidths=(36*mm,36*mm, 28*mm, 18*mm, 28*mm, 25*mm, 25*mm))
    MiscTable=Table(miscTab,colWidths=(36*mm,36*mm, 18*mm, 28*mm, 28*mm, 25*mm, 25*mm))
    style=TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)
    ])
    RebateTable.setStyle(style)
    RoomTable.setStyle(style)
    FoodTable.setStyle(style)
    AVTable.setStyle(style)
    MiscTable.setStyle(style)
    elems=[]
    elems.append(GenTab)
    elems.append(RebateTable)
    elems.append(RoomTable)
    elems.append(FoodTable)
    elems.append(AVTable)
    elems.append(MiscTable)
    pdf.build(elems)
    splitPDF(filename,2)
    pdf_merger = PdfFileMerger()
    pdf_merger.append("Output/"+filename+"part1.pdf")
    pdf_merger.append("Output/" + filename + "Reconciled.pdf")
    pdf_merger.append("Output/"+filename+"part2.pdf")
    with open("Output/"+filename+"Final.pdf", 'wb') as output_file:
        pdf_merger.write(output_file)
    return filename