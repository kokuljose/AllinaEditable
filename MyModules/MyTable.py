import csv
import os
import pandas as pd
import datetime

OUTPUT_DIRECTORY = os.path.dirname(__file__)[:-10] + "/output"
def html_input(c):
    return '<input name="{}" value="{{}}" />'.format(c)

def getDict(key,table):
    tab=[]
    for ele in table:
        tab.append(ele[:-2])
    df=pd.DataFrame(tab)
    htmltab=df.style.format({c: html_input(key) for c in df.columns}).hide_index().render()
    # htmltab=df.style.format('<input name="df" value="{}" />').hide_index().render()
    # htmltable=htmltab.replace("df",key)
    return {key:htmltab}

def saveToCSV(row, fileName):
    with open(OUTPUT_DIRECTORY + "/" + fileName + ".csv", 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row)


def saveToCSVWithHead(row, fileName, head):
    with open(OUTPUT_DIRECTORY + "/" + fileName + ".csv", 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(head)
        writer.writerows(row)


def formatDate(date):
    date=datetime.datetime.strptime(date, '%d-%b-%y')
    return date.strftime('%Y-%m-%d')


def getGeneralDetailsTable(DocResults):
    generalDetailsTable = []
    IsRevised = False
    Vendor=''
    InvNum=''
    InvDate=''
    InvTotal=''
    City=''
    Event=''
    if DocResults["fields"]["Company"] != None:
        company = DocResults["fields"]["Company"]["text"]
    else:
        company = str(DocResults["docType"]).split(':')
        company = company[len(company) - 1]
    if DocResults["fields"]["City"] != None:
        Vendor=company
        City=DocResults["fields"]["City"]["text"].replace(',', '')
        generalDetailsTable.append(
            [company + ", " + DocResults["fields"]["City"]["text"].replace(',', ''), '', '', '', '', '', ''])
    else:
        Vendor = company
        generalDetailsTable.append([company, '', '', '', '', '', ''])
    if DocResults["fields"]["Invoice Number"] != None:
        InvNum=DocResults["fields"]["Invoice Number"]["text"]
        generalDetailsTable.append(
            ['Invoice ' + DocResults["fields"]["Invoice Number"]["text"], '', '', '', '', '', ''])
    else:
        generalDetailsTable.append(['', '', '', '', '', '', ''])
    if DocResults["fields"]["In Payment For"] != None:
        Event=DocResults["fields"]["In Payment For"]["text"]
        generalDetailsTable.append([DocResults["fields"]["In Payment For"]["text"], '', '', '', '', '', ''])
    else:
        generalDetailsTable.append(['', '', '', '', '', '', ''])
    if DocResults["fields"]["Invoice Date"] != None:
        InvDate=DocResults["fields"]["Invoice Date"]["text"]
        generalDetailsTable.append([DocResults["fields"]["Invoice Date"]["text"], '', '', '', '', '', ''])
    else:
        generalDetailsTable.append(['', '', '', '', '', '', ''])
    if DocResults["fields"]["Room Total Final"] != None and DocResults["fields"]["Earned Comps Total Final"] != None and \
            DocResults["fields"]["Food Total Final"] != None:
        IsRevised = True
        InvTotal=DocResults["fields"]["Final Invoice Amount"]["text"]
        generalDetailsTable.append(
            ['', '', '', '', '', DocResults["fields"]["Final Invoice Amount"]["text"] + " Reconciled",
             DocResults["fields"]["Final Invoice Amount"]["text"] + " Billed"])
    elif DocResults["fields"]["Room Total"] != None and DocResults["fields"]["Earned Comps Total"] != None and \
            DocResults["fields"]["Food Total"] != None:
        IsRevised = False
        InvTotal = DocResults["fields"]["Invoice Amount"]["text"]
        generalDetailsTable.append(
            ['', '', '', '', '', DocResults["fields"]["Invoice Amount"]["text"] + " Reconciled",
             DocResults["fields"]["Invoice Amount"]["text"] + " Billed"])
    else:
        if DocResults["fields"]["Invoice Amount"] != None:
            InvTotal = DocResults["fields"]["Invoice Amount"]["text"]
            generalDetailsTable.append(
                ['', '', '', '', '', DocResults["fields"]["Invoice Amount"]["text"] + " Reconciled",
                 DocResults["fields"]["Invoice Amount"]["text"] + " Billed"])
        else:
            generalDetailsTable.append(['', '', '', '', '', '$ Reconciled', '$ Billed'])
    InvDate=formatDate(InvDate)
    genDetailsJSON={"Vendor":Vendor,"InvNum":InvNum,"InvDate":InvDate,"InvTotal":InvTotal,"City":City,"Event":Event}
    return generalDetailsTable, IsRevised,genDetailsJSON


def getOverviewTable(DocResults):
    overviewTable = []
    table = [[], []]
    if DocResults["fields"]["Room Total Final"] != None and DocResults["fields"]["Earned Comps Total Final"] != None and \
            DocResults["fields"]["Food Total Final"] != None:
        if DocResults["fields"]["Rebate Total Final"]["text"] != '$0.00':
            table[0].append("Rebate")
            table[1].append(DocResults["fields"]["Rebate Total Final"]["text"])
            overviewTable.append(
                ["Rebate To Master", '', '', '', '', DocResults["fields"]["Rebate Total Final"]["text"],
                 DocResults["fields"]["Rebate Total Final"]["text"]])
        if DocResults["fields"]["Room Total Final"]["text"] != '$0.00':
            table[0].append("Room")
            table[1].append(DocResults["fields"]["Room Total Final"]["text"])
            overviewTable.append(["Room & Tax", '', '', '', '', DocResults["fields"]["Room Total Final"]["text"],
                                  DocResults["fields"]["Room Total Final"]["text"]])
        if DocResults["fields"]["Food Total Final"]["text"] != '$0.00':
            table[0].append("Food")
            table[1].append(DocResults["fields"]["Food Total Final"]["text"])
            overviewTable.append(["Food & Beverage", '', '', '', '', DocResults["fields"]["Food Total Final"]["text"],
                                  DocResults["fields"]["Food Total Final"]["text"]])
        if DocResults["fields"]["AV Total Final"]["text"] != '$0.00':
            table[0].append("AV")
            table[1].append(DocResults["fields"]["AV Total Final"]["text"])
            overviewTable.append(["Audio Visual", '', '', '', '', DocResults["fields"]["AV Total Final"]["text"],
                                  DocResults["fields"]["AV Total Final"]["text"]])
        if DocResults["fields"]["Misc Total Final"]["text"] != '$0.00':
            table[0].append("Misc")
            table[1].append(DocResults["fields"]["Misc Total Final"]["text"])
            overviewTable.append(["Miscellaneous", '', '', '', '', DocResults["fields"]["Misc Total Final"]["text"],
                                  DocResults["fields"]["Misc Total Final"]["text"]])
        if DocResults["fields"]["Earned Comps Total Final"]["text"] != '$0.00':
            table[0].append("Comps")
            table[1].append(DocResults["fields"]["Earned Comps Total Final"]["text"])
            overviewTable.append(
                ["Earned Comps", '', '', '', '', DocResults["fields"]["Earned Comps Total Final"]["text"],
                 DocResults["fields"]["Earned Comps Total Final"]["text"]])
    else:
        if DocResults["fields"]["Rebate Total"]["text"] != '$0.00':
            table[0].append("Rebate")
            table[1].append(DocResults["fields"]["Rebate Total"]["text"])
            overviewTable.append(["Rebate To Master", '', '', '', '', DocResults["fields"]["Rebate Total"]["text"],
                                  DocResults["fields"]["Rebate Total"]["text"]])
        if DocResults["fields"]["Room Total"]["text"] != '$0.00':
            table[0].append("Room")
            table[1].append(DocResults["fields"]["Room Total"]["text"])
            overviewTable.append(["Room & Tax", '', '', '', '', DocResults["fields"]["Room Total"]["text"],
                                  DocResults["fields"]["Room Total"]["text"]])
        if DocResults["fields"]["Food Total"]["text"] != '$0.00':
            table[0].append("Food")
            table[1].append(DocResults["fields"]["Food Total"]["text"])
            overviewTable.append(["Food & Beverage", '', '', '', '', DocResults["fields"]["Food Total"]["text"],
                                  DocResults["fields"]["Food Total"]["text"]])
        if DocResults["fields"]["AV Total"]["text"] != '$0.00':
            table[0].append("AV")
            table[1].append(DocResults["fields"]["AV Total"]["text"])
            overviewTable.append(["Audio Visual", '', '', '', '', DocResults["fields"]["AV Total"]["text"],
                                  DocResults["fields"]["AV Total"]["text"]])
        if DocResults["fields"]["Misc Total"]["text"] != '$0.00':
            table[0].append("Misc")
            table[1].append(DocResults["fields"]["Misc Total"]["text"])
            overviewTable.append(["Miscellaneous", '', '', '', '', DocResults["fields"]["Misc Total"]["text"],
                                  DocResults["fields"]["Misc Total"]["text"]])
        if DocResults["fields"]["Earned Comps Total"]["text"] != '$0.00':
            table[0].append("Comps")
            table[1].append(DocResults["fields"]["Earned Comps Total"]["text"])
            overviewTable.append(["Earned Comps", '', '', '', '', DocResults["fields"]["Earned Comps Total"]["text"],
                                  DocResults["fields"]["Earned Comps Total"]["text"]])
    overviewJSON={}
    for key in table[0]:
        overviewJSON[key]=table[1][table[0].index(key)]
    return overviewTable, table,overviewJSON
def getCords(readResults,pageNum,lineNum,pgStrEndStrings,starting,ending,fixedValList,cordList,fixedAllign):
    if any(x in readResults[pageNum]["lines"][lineNum]['text'] for x in
           pgStrEndStrings[0]) and starting < float(
        readResults[pageNum]["lines"][lineNum]['boundingBox'][5]):
        starting = float(readResults[pageNum]["lines"][lineNum]['boundingBox'][5])
    elif any(x in readResults[pageNum]["lines"][lineNum]['text'] for x in
             pgStrEndStrings[1]) and ending > float(
        readResults[pageNum]["lines"][lineNum]['boundingBox'][1]) and starting != 0.00:
        ending = float(readResults[pageNum]["lines"][lineNum]['boundingBox'][1])
    for fixedVal in fixedValList:
        if fixedAllign[fixedValList.index(fixedVal)] == 'l':
            if any(x in readResults[pageNum]["lines"][lineNum]['text'] for x in fixedVal) and cordList[
                fixedValList.index(fixedVal)] < float(
                readResults[pageNum]["lines"][lineNum]['boundingBox'][0]):
                cordList[fixedValList.index(fixedVal)] = float(
                    readResults[pageNum]["lines"][lineNum]['boundingBox'][0])
        elif fixedAllign[fixedValList.index(fixedVal)] == 'r':
            if any(x in readResults[pageNum]["lines"][lineNum]['text'] for x in fixedVal) and cordList[
                fixedValList.index(fixedVal)] < float(
                readResults[pageNum]["lines"][lineNum]['boundingBox'][2]):
                cordList[fixedValList.index(fixedVal)] = float(
                    readResults[pageNum]["lines"][lineNum]['boundingBox'][2])
        elif fixedAllign[fixedValList.index(fixedVal)] == 'c':
            if any(x in readResults[pageNum]["lines"][lineNum]['text'] for x in fixedVal) and cordList[
                fixedValList.index(fixedVal)] < (
                    float(readResults[pageNum]["lines"][lineNum]['boundingBox'][0]) + float(
                readResults[pageNum]["lines"][lineNum]['boundingBox'][2]) / 2):
                cordList[fixedValList.index(fixedVal)] = float(
                    readResults[pageNum]["lines"][lineNum]['boundingBox'][0]) + float(
                    readResults[pageNum]["lines"][lineNum]['boundingBox'][2]) / 2
    return cordList,starting,ending

def getTableCords(readResults, startIdentifiers, endIdentifiers, pgStrEndStrings, fixedValList, fixedAllign):
    startPageNum = -1
    endPageNum = -1
    tableCords = []
    for pageNum in range(0, len(readResults)):
        starting = 0.00
        ending = float(readResults[pageNum]["height"])
        cordList = [-1] * len(fixedValList)
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            if any(x in readResults[pageNum]["lines"][lineNum]['text'] for x in startIdentifiers[0]):
                if any(x in readResults[pageNum]["lines"][lineNum + 1]['text'] for x in startIdentifiers[1]):
                    startPageNum = pageNum
                    tableCords = []
            if startPageNum != -1:  # Page Started
                cordList,starting,ending=getCords(readResults, pageNum, lineNum, pgStrEndStrings, starting, ending, fixedValList, cordList,
                         fixedAllign)
            if any(x in readResults[pageNum]["lines"][lineNum]['text'] for x in
                   endIdentifiers[0]) and startPageNum != -1:
                if any(x in readResults[pageNum]["lines"][lineNum + 1]['text'] for x in
                       endIdentifiers[1]):  # Page Ended
                    endPageNum = pageNum
                    tableCords.append({"PageNum": pageNum, "Starting": starting, "Ending": ending, "Cords": cordList})
                    return tableCords, startPageNum, endPageNum
        if startPageNum != -1:  # Page Started
            tableCords.append({"PageNum": pageNum, "Starting": starting, "Ending": ending, "Cords": cordList})
    return tableCords, startPageNum, endPageNum


def getTable(readResults, tableCords, startPageNum, endPageNum, bodyAllign):
    cost = float(tableCords[0]["Ending"]) * 0.05  # computed from %
    roomTab = []
    lastWrittenIndex = 0
    row = [''] * len(bodyAllign)
    pageCount = 0
    for pageNum in range(startPageNum, endPageNum + 1):
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            if float(readResults[pageNum]["lines"][lineNum]['boundingBox'][1]) > float(
                    tableCords[pageCount]["Starting"]):
                if float(readResults[pageNum]["lines"][lineNum]['boundingBox'][5]) > float(
                        tableCords[pageCount]["Ending"]):
                    break
                if "l" in bodyAllign:
                    leftCord = float(readResults[pageNum]["lines"][lineNum]['boundingBox'][0])
                if "r" in bodyAllign:
                    rightCord = float(readResults[pageNum]["lines"][lineNum]['boundingBox'][2])
                if "c" in bodyAllign:
                    centerCord = float(readResults[pageNum]["lines"][lineNum]['boundingBox'][0]) + float(
                        readResults[pageNum]["lines"][lineNum]['boundingBox'][2]) / 2
                for index in range(0, len(bodyAllign)):
                    if bodyAllign[index] == 'l' and abs(
                            (tableCords[pageCount]["Cords"][index] - leftCord)) < cost:
                        if lastWrittenIndex >= index:
                            roomTab.append(row)
                            row = [''] * len(bodyAllign)
                        row[index] = readResults[pageNum]["lines"][lineNum]["text"]
                        lastWrittenIndex = index
                        break
                    elif bodyAllign[index] == 'r' and abs(
                            (tableCords[pageCount]["Cords"][index] - rightCord)) < cost:
                        if lastWrittenIndex >= index:
                            roomTab.append(row)
                            row = [''] * len(bodyAllign)
                        row[index] = readResults[pageNum]["lines"][lineNum]["text"]
                        lastWrittenIndex = index
                        break
                    elif bodyAllign[index] == 'c' and abs(
                            (tableCords[pageCount]["Cords"][index] - centerCord)) < cost:
                        if lastWrittenIndex >= index:
                            roomTab.append(row)
                            row = [''] * len(bodyAllign)
                        row[index] = readResults[pageNum]["lines"][lineNum]["text"]
                        lastWrittenIndex = index
                        break
        pageCount = pageCount + 1
    roomTab.append(row)
    return roomTab
def nextVal(curValue, readResults, PageNum, lineNum):
    for pageNum in range(PageNum, PageNum + 1):
        for lineNum in range(lineNum, len(readResults[pageNum]["lines"])):
            x = readResults[pageNum]["lines"][lineNum]['text']
            if curValue in readResults[pageNum]["lines"][lineNum]['text']:
                if abs(len(curValue) - len(readResults[pageNum]["lines"][lineNum]['text'])) < 3:
                    return readResults[pageNum]["lines"][lineNum + 1]['text'], pageNum
                else:
                    return readResults[pageNum]["lines"][lineNum]['text'][
                           readResults[pageNum]["lines"][lineNum]['text'].index(curValue) + len(curValue):], pageNum
    return "no", pageNum

def nextValue(curValue, readResults, startPageNum, endPageNum):
    for pageNum in range(startPageNum, endPageNum + 1):
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            x = readResults[pageNum]["lines"][lineNum]['text']
            if curValue in readResults[pageNum]["lines"][lineNum]['text']:
                if abs(len(curValue) - len(readResults[pageNum]["lines"][lineNum]['text'])) < 3:
                    return readResults[pageNum]["lines"][lineNum + 1]['text'], pageNum
                else:
                    return readResults[pageNum]["lines"][lineNum]['text'][
                           readResults[pageNum]["lines"][lineNum]['text'].index(curValue) + len(curValue):], pageNum
    return "no", pageNum


def getTableCordsFromPageNo(readResults, pgStrEndStrings, fixedValList, fixedAllign,start):
    startPageNum = -1
    endPageNum = -1
    tableCords = []
    for pageNum in range(start, len(readResults)):
        starting = 0.00
        ending = float(readResults[pageNum]["height"])
        cordList = [-1] * len(fixedValList)
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            cell = readResults[pageNum]["lines"][lineNum]['text']
            if 'Page No' in cell and startPageNum == -1:
                nextVal,pageNo = nextValue('Page No.' , readResults, pageNum, pageNum)
                if '1' in cell + nextVal:
                    newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in nextVal[nextVal.index('of') + 2:])
                    totalPages = int(newstr.split()[0])
                    startPageNum = pageNum
                    endPageNum = pageNum + totalPages-1
            if startPageNum != -1:  # Page Started
                cordList,starting,ending=getCords(readResults, pageNum, lineNum, pgStrEndStrings, starting, ending, fixedValList, cordList,
                             fixedAllign)
        if startPageNum != -1:
                tableCords.append({"PageNum": pageNum, "Starting": starting, "Ending": ending, "Cords": cordList})
        if endPageNum==pageNum:
            return tableCords, startPageNum, endPageNum

    return tableCords, startPageNum, endPageNum
def understand(param):
    newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in param)
    listOfNum=newstr.split()
    if len(listOfNum)>1:
        rate=min(listOfNum)
        count=max(listOfNum)
        if param.find('$')!=-1:
            newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in param[param.find('$')+1:])
            listOfNumbers=newstr.split(' ')
            rate=listOfNumbers[0]
            if rate==count:
                for num in listOfNum:
                    if num!=count:
                        count=num
                        break
        return count,rate
    else :
        return 0,0