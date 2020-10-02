from MyModules import MyTable

def getGeneralDetailsTable(DocResults):
    generalDetailsTable=[]
    IsRevised=False
    if DocResults["fields"]["Company"]!=None:
        company=DocResults["fields"]["Company"]["text"]
    else:
        company=str(DocResults["docType"]).split(':')
        company=company[len(company)-1]
    if DocResults["fields"]["City"]!=None:
        generalDetailsTable.append([company+", "+DocResults["fields"]["City"]["text"].replace(',',''),'','','','','',''])
    else:
        generalDetailsTable.append([company, '', '', '', '', '', ''])
    if DocResults["fields"]["Invoice Number"]!=None:
        generalDetailsTable.append(['Invoice '+DocResults["fields"]["Invoice Number"]["text"],'','','','','',''])
    else:
        generalDetailsTable.append(['', '', '', '', '', '', ''])
    if DocResults["fields"]["In Payment For"]!=None:
        generalDetailsTable.append([DocResults["fields"]["In Payment For"]["text"], '', '', '', '', '', ''])
    else:
        generalDetailsTable.append(['', '', '', '', '', '', ''])
    if DocResults["fields"]["Invoice Date"]!=None:
        generalDetailsTable.append([DocResults["fields"]["Invoice Date"]["text"], '', '', '', '', '', ''])
    else:
        generalDetailsTable.append(['', '', '', '', '', '', ''])
    if DocResults["fields"]["Room Total Final"]!=None and DocResults["fields"]["Earned Comps Total Final"]!=None and DocResults["fields"]["Food Total Final"]!=None :
        IsRevised=True
        generalDetailsTable.append([ '', '', '', '', '', DocResults["fields"]["Final Invoice Amount"]["text"]+ " Reconciled",DocResults["fields"]["Final Invoice Amount"]["text"]+" Billed"])
    elif DocResults["fields"]["Room Total"] != None and DocResults["fields"]["Earned Comps Total"] != None and DocResults["fields"]["Food Total"] != None:
        IsRevised=False
        generalDetailsTable.append(
            ['', '', '', '', '', DocResults["fields"]["Invoice Amount"]["text"] + " Reconciled",
             DocResults["fields"]["Invoice Amount"]["text"] + " Billed"])
    else:
        generalDetailsTable.append(['', '', '', '', '', '$ Reconciled', '$ Billed'])
    return generalDetailsTable,IsRevised

def getOverviewTable(DocResults):
    overviewTable=[]
    table=[[],[]]
    if DocResults["fields"]["Room Total Final"]!=None and DocResults["fields"]["Earned Comps Total Final"]!=None and DocResults["fields"]["Food Total Final"]!=None :
        if DocResults["fields"]["Rebate Total Final"]["text"]!='$0.00':
            table[0].append("Rebate")
            table[1].append(DocResults["fields"]["Rebate Total Final"])
            overviewTable.append(["Rebate To Master",'','','','',DocResults["fields"]["Rebate Total Final"]["text"],
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
            overviewTable.append(["Earned Comps", '', '', '', '', DocResults["fields"]["Earned Comps Total Final"]["text"],
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
    return overviewTable,table

def getRebateTable(DocResults):
    rebateTable = []
    if DocResults["fields"]["Room Total Final"] != None and DocResults["fields"]["Earned Comps Total Final"] != None and DocResults["fields"]["Food Total Final"] != None:
        rebateTable.append(["Rebate To Master", '', '', '', '', DocResults["fields"]["Rebate Total Final"]["text"],
                              DocResults["fields"]["Rebate Total Final"]["text"]])
        rebateTable.append(["5% of Total Room Revenue",'','1','',DocResults["fields"]["Rebate Total Final"]["text"],'',''])
    else:
        rebateTable.append(["Rebate To Master", '', '', '', '', DocResults["fields"]["Rebate Total"]["text"],
                            DocResults["fields"]["Rebate Total"]["text"]])
        rebateTable.append(["5% of Total Room Revenue", '', '1', '', DocResults["fields"]["Rebate Total"]["text"],'', ''])
    return rebateTable


def getRoomShortTab(roomFullTab):
    roomShortTab=[]
    names=[]
    noOfDays = 0
    perDayRate = '0.00'
    guestTotal = ''
    roomRate='0.00'
    for rowIndex in range(0,len(roomFullTab)):
        for colIndex in range(0,len(roomFullTab[rowIndex])):
            cell=roomFullTab[rowIndex][colIndex]
            if 'Room #' in cell:
                noOfDays = 0
                perDayRate = '0.00'
                guestTotal = ''
                names=cell[:cell.index('Room')].split(',')
            elif 'Sub Tota' in cell:
                noOfDays=noOfDays+1
                perDayRate=roomFullTab[rowIndex][colIndex+1]
            elif 'Guest Tota' in cell:
                perDayRate=perDayRate.replace(',','.')
                if(float(perDayRate)>float(roomRate)):
                    roomRate=perDayRate
                guestTotal=roomFullTab[rowIndex][colIndex+1]
                roomShortTab.append([names[0],names[1],noOfDays,perDayRate,guestTotal,'',''])
    return roomShortTab,roomRate

def getRoomTable(readResults):
    startIdentifiers=[["los", "angeles"], ["ROOM", "TAX","Room","Tax"]]
    endIdentifiers=[["for staying at", "Thank you for"],["Los", "Angeles", "Hotel at California"]]
    pgStrEndStrings = [["Date", "Description", "Charges", "Payment"], ["Los", "Angeles", "Hotel at California"]]
    fixedValList = [["Date"],["Description", "Room Charge"], ["Charges"]]
    fixedAllign = ['l','l', 'l']
    bodyAllign = ['l','l', 'l']
    tableCords,startPageNum,endPageNum= MyTable.getTableCords(readResults,startIdentifiers,endIdentifiers,
                                                              pgStrEndStrings,fixedValList,fixedAllign)
    roomFullTab=MyTable.getTable(readResults,tableCords,startPageNum,endPageNum,bodyAllign)
    roomTab,roomRate=getRoomShortTab(roomFullTab)
    return roomTab,roomRate


def getFoodShortTab(foodFullTab):
    foodShortTab = []
    Date=''
    Event=''
    Amount=''
    weekDays=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
    prevDates=[]
    for rowIndex in range(0, len(foodFullTab)):
        for colIndex in range(0, len(foodFullTab[rowIndex])):
            cell = foodFullTab[rowIndex][colIndex]
            if any(x in cell for x in weekDays):
                if "PM" in foodFullTab[rowIndex][colIndex+1] or "AM" in foodFullTab[rowIndex][colIndex+1]:
                    Date=cell.split(',')[1]
                    if Date not in prevDates:
                        prevDates.append(Date)
            if "Dinner" in cell:
                Event="Dinner"
            if "Breakfast" in cell:
                Event="Breakfast"
            if "Supper" in cell:
                Event="Supper"
            if "Lunch" in cell:
                Event="Lunch"
            if "Grand Total" in cell:
                Amount=foodFullTab[rowIndex][colIndex+1]
                foodShortTab.append([Date,"Day "+str(len(prevDates))+" - "+Event,"1",'',Amount,'',''])
                Date = ''
                Event = ''
                Amount = ''
    return foodShortTab


def getFoodTable(readResults):
    startIdentifiers = [["los", "angeles"], ["CATERING", "F & B"]]
    endIdentifiers = [["los", "angeles"], ["MA3"]]
    pgStrEndStrings = [["Time", "Function"], ["Balance Due", "Signature"]]
    fixedValList = [["Quantity"], ["Time"], ["Room"], ["Price","Subtotal:"], ["Amount"]]
    fixedAllign = ['l', 'l', 'l','r','r']
    bodyAllign = ['l', 'l', 'l','r','r']
    tableCords, startPageNum, endPageNum = MyTable.getTableCords(readResults, startIdentifiers, endIdentifiers,
                                                                 pgStrEndStrings, fixedValList, fixedAllign)
    foodFullTab = MyTable.getTable(readResults, tableCords, startPageNum, endPageNum, bodyAllign)
    foodTab = getFoodShortTab(foodFullTab)
    return foodTab


def getAVShortTab(readResults, startPageNum, endPageNum):
    pageNum=startPageNum
    AVShortTab=[]
    while (pageNum<=endPageNum):
        Date,pageNum = MyTable.nextValue("Report Date", readResults, pageNum, endPageNum)
        if Date=="no":
            pageNum = pageNum + 1
            continue
        Amount,pageNum = MyTable.nextValue("Order Total", readResults, pageNum, endPageNum)
        AVShortTab.append([Date,"AV","1",'',Amount,'',''])
        pageNum=pageNum+1
    return AVShortTab


def getAVTable(readResults):
    startIdentifiers = [["los", "angeles"], ["AUDIO", "A/V","Audio","Visual"]]
    endIdentifiers = [["los", "angeles"], ["MA4"]]
    pgStrEndStrings = [["Time", "Function"], ["Balance Due", "Signature"]]#no use
    fixedValList = [["Quantity"], ["Time"], ["Room"], ["Price", "Subtotal:"], ["Amount"]]#no use
    fixedAllign = ['l', 'l', 'l', 'r', 'r']#no use
    tableCords, startPageNum, endPageNum = MyTable.getTableCords(readResults, startIdentifiers, endIdentifiers,
                                                                 pgStrEndStrings, fixedValList, fixedAllign)

    avTab = getAVShortTab(readResults,startPageNum,endPageNum)
    return avTab


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

def getMiscShortTab(miscFullTab):
    miscShortTab=[]
    names=[]
    Event=''
    mealsTab=[]
    parkingTab = []
    parking=[]
    parkingRate=0
    porterage=[]
    gratuity=[]
    noOfDays = 0
    perDayRate = ''
    guestTotal = ''
    parkingList=['Valet','Parking']
    mealsList=['Dinner','Liquor','Food','Wine','Beer','Breakfast','Lunch']
    Key="Promotional Credit 15% Discount, per contract"
    subTotalList=[]
    for rowIndex in range(0, len(miscFullTab)):
        for colIndex in range(0, len(miscFullTab[rowIndex])):
            cell = miscFullTab[rowIndex][colIndex]
            if "Promotional Credit" in cell:
                if '%' in miscFullTab[rowIndex+1][colIndex]:
                    Key=miscFullTab[rowIndex+1][colIndex]
                mealsTab.append([Key,"","1","",miscFullTab[rowIndex][colIndex+1],'',''])
                rowIndex=rowIndex+4
            if "Room #" in cell:
                noOfDays = 0
                perDayRate = ''
                guestTotal = ''
                names=cell[:cell.index('Room')].split(',')
            elif 'Sub Total' in cell:
                noOfDays = noOfDays + 1
                perDayRate = miscFullTab[rowIndex][colIndex + 1]
                subTotalList.append(perDayRate)
            elif 'Guest Total' in cell:
                guestTotal = miscFullTab[rowIndex][colIndex + 1]
                mealRate=''
                if '-' not in guestTotal:
                    if 'Meals' in Event and 'Parking' in Event:
                        if Event.find('Meals')<Event.find('Parking'):
                            mealRate=subTotalList[0]
                            parkingRate=subTotalList[1]
                        elif Event.find('Meals')>=Event.find('Parking'):
                            mealRate=subTotalList[1]
                            parkingRate=subTotalList[0]
                        if len(names)==0:
                            mealsTab.append(['', '', 1, '', mealRate, '', ''])
                        elif len(names)==1:
                            mealsTab.append([names[0], '', 1, '', mealRate, '', ''])
                        else:
                            mealsTab.append([names[0], names[1], 1, '', mealRate, '', ''])
                        if len(names) == 0:
                            parkingTab.append(['', '', noOfDays-1, '', parkingRate, '', ''])
                        elif len(names) == 1:
                            parkingTab.append([names[0], '', noOfDays-1, '', parkingRate, '', ''])
                        else:
                            parkingTab.append([names[0], names[1], noOfDays-1, '', parkingRate, '', ''])
                    elif 'Meals' in Event:
                        if len(names)==0:
                            mealsTab.append(['', '', noOfDays, '', guestTotal, '', ''])
                        elif len(names)==1:
                            mealsTab.append([names[0], '', noOfDays, '', guestTotal, '', ''])
                        else:
                            mealsTab.append([names[0], names[1], noOfDays, '', guestTotal, '', ''])
                    elif 'Parking' in Event:
                        parkingRate=perDayRate
                        parTot = float(perDayRate) * noOfDays
                        if float(guestTotal)!=float(perDayRate)*noOfDays:
                            if len(names) == 0:
                                mealsTab.append(['', '', 1, '', round(float(guestTotal)-parTot,2), '', ''])
                            elif len(names) == 1:
                                mealsTab.append([names[0], '', 1, '', round(float(guestTotal)-parTot,2), '', ''])
                            else:
                                mealsTab.append([names[0], names[1], 1, '', round(float(guestTotal)-parTot,2), '', ''])
                        else:
                            if len(names) == 0:
                                parkingTab.append(['', '', noOfDays, '', parTot, '', ''])
                            elif len(names) == 1:
                                parkingTab.append([names[0], '', noOfDays, '', parTot, '', ''])
                            else:
                                parkingTab.append([names[0], names[1], noOfDays, '', parTot, '', ''])
                Event=" "
                subTotalList=[]
            if any(x in cell for x in parkingList):
                Event=Event+"Parking"
            elif any(x in cell for x in mealsList):
                Event=Event+"Meals"
            elif "Porterage" in cell and colIndex==1:
                number,rate=understand(miscFullTab[rowIndex+1][colIndex])
                porterage=["Porterage",'',number,rate,miscFullTab[rowIndex][colIndex + 1],'','']
            elif "Housekeeping" in cell:
                number,rate=understand(miscFullTab[rowIndex+1][colIndex])
                gratuity=["Gratuties",'',number,rate,miscFullTab[rowIndex][colIndex + 1],'','']
    mealsTab.insert(0,['Meals','','','','','',''])
    noOfParking=0
    for park in parkingTab:
        noOfParking=noOfParking+int(park[2])
    parkingTab.insert(0,['Parking','',parkingRate,noOfParking,float(parkingRate)*noOfParking,'',''])
    miscShortTab.extend(mealsTab)
    miscShortTab.extend(parkingTab)
    miscShortTab.append(porterage)
    miscShortTab.append(gratuity)
    return miscShortTab

def getMiscTable(readResults):
    startIdentifiers = [["los", "angeles"], ["MISCELLANEOUS", "Miscellaneous"]]
    endIdentifiers = [["los", "angeles"], ["REBATE","Rebate"]]
    pgStrEndStrings = [["Date", "Description", "Payment"], ["Los", "Angeles", "Hotel at California"]]
    fixedValList = [["Date"], ["Description", "Room Charge"], ["Charges"]]
    fixedAllign = ['l', 'l', 'l']
    bodyAllign = ['l', 'l', 'l']
    tableCords, startPageNum, endPageNum = MyTable.getTableCords(readResults, startIdentifiers, endIdentifiers,
                                                                 pgStrEndStrings, fixedValList, fixedAllign)
    miscFullTab = MyTable.getTable(readResults, tableCords, startPageNum, endPageNum, bodyAllign)
    miscShortTab = getMiscShortTab(miscFullTab)
    return miscShortTab


def getCompsTable(DocResults,rateOfRoom):
    compsTable = []
    if DocResults["fields"]["Room Total Final"] != None and DocResults["fields"]["Earned Comps Total Final"] != None and \
            DocResults["fields"]["Food Total Final"] != None:
        comps=DocResults["fields"]["Earned Comps Total Final"]["text"].replace("-",'').replace("$",'')
        compsTable.append(["Earned Comps", '', '', '', '',comps ,comps])
        compsTable.append(
            ["Earned Comp Rooms", '', int((float(comps)+1.00)/float(rateOfRoom)), rateOfRoom, comps, '', ''])
    else:
        comps=DocResults["fields"]["Earned Comps Total"]["text"].replace("-",'').replace("$",'')
        compsTable.append(["Earned Comps", '', '', '', '',comps ,comps])
        compsTable.append(
            ["Earned Comp Rooms", '',int((float(comps)+1.00)/float(rateOfRoom)), rateOfRoom, comps, '', ''])
    return compsTable


def getAllTables(FRResult,CGResult):
    detailedTable = []
    generalDetailsTable,IsRevised=MyTable.getGeneralDetailsTable(FRResult["analyzeResult"]["documentResults"][0])
    detailedTable.extend(generalDetailsTable)
    overviewTable,tables=MyTable.getOverviewTable(FRResult["analyzeResult"]["documentResults"][0])
    roomRate=''
    if 'Rebate' in tables[0]:
        rebateTable = getRebateTable(FRResult["analyzeResult"]["documentResults"][0])
        detailedTable.extend(rebateTable)
    if 'Room' in tables[0]:
        roomTable,roomRate=getRoomTable(CGResult["analyzeResult"]["readResults"])
        detailedTable.append(["Rebate to Master",'','','','',tables[1][tables[0].index('Room')]])
        detailedTable.extend(roomTable)
    if 'Food' in tables[0]:
        foodTable=getFoodTable(CGResult["analyzeResult"]["readResults"])
        detailedTable.append(["Food and Beverage",'','','','',tables[1][tables[0].index('Food')]])
        detailedTable.extend(foodTable)
    if 'AV' in tables[0]:
        avTable=getAVTable(CGResult["analyzeResult"]["readResults"])
        detailedTable.append(["AV",'','','','',tables[1][tables[0].index('AV')]])
        detailedTable.extend(avTable)
    if 'Misc' in tables[0]:
        miscTable=getMiscTable(CGResult["analyzeResult"]["readResults"])
        detailedTable.append(["Miscellaneous",'','','','',tables[1][tables[0].index('Misc')]])
        detailedTable.extend(miscTable)
    if 'Comps' in tables[0]:
        compsTable = getCompsTable(FRResult["analyzeResult"]["documentResults"][0],roomRate)
        detailedTable.extend(compsTable)
    return generalDetailsTable,overviewTable,detailedTable,IsRevised