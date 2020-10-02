from MyModules import MyTable

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


def getMiscMealsShortTab(miscFullTab):
    miscShortTab = []
    names = []
    for rowIndex in range(0, len(miscFullTab)):
        Date=miscFullTab[rowIndex][0][:9]
        if "Room #" in miscFullTab[rowIndex][0] and 'Of' not in miscFullTab[rowIndex][0]:
            noOfDays = 0
            perDayRate = ''
            guestTotal = ''
            names = miscFullTab[rowIndex][0][:miscFullTab[rowIndex][0].index('Room')].split(',')
        if "Room #" in miscFullTab[rowIndex][1] and 'Of' not in miscFullTab[rowIndex][1]:
            noOfDays = 0
            perDayRate = ''
            guestTotal = ''
            names = miscFullTab[rowIndex][1][:miscFullTab[rowIndex][1].index('Room')].split(',')
        if 'Sub Tota' in miscFullTab[rowIndex][2]:
            noOfDays = noOfDays + 1
            perDayRate = miscFullTab[rowIndex][3]
        if 'Guest Tota' in miscFullTab[rowIndex][2]:
            if len(names) == 0:
                miscShortTab.append(['', '', noOfDays, '', miscFullTab[rowIndex][3], '', ''])
            elif len(names) == 1:
                miscShortTab.append([names[0], '', noOfDays, '', miscFullTab[rowIndex][3], '', ''])
            else:
                miscShortTab.append([names[0], names[1], noOfDays , '', miscFullTab[rowIndex][3], '', ''])
    return miscShortTab

def getMiscOtherShortTab(miscFullTab):
    miscShortTab=[]
    names=[]
    parkingTab = []
    porterage=[]
    gratuity=[]
    noOfDays = 0
    perDayRate = ''
    item=''
    packageTab=[]
    for rowIndex in range(0, len(miscFullTab)):
        Date=miscFullTab[rowIndex][0][:9]
        if "Room #" in miscFullTab[rowIndex][0]:
            noOfDays = 0
            perDayRate = ''
            guestTotal = ''
            names = miscFullTab[rowIndex][0][:miscFullTab[rowIndex][0].index('Room')].split(',')
        if "Room #" in miscFullTab[rowIndex][1]:
            noOfDays = 0
            perDayRate = ''
            guestTotal = ''
            names = miscFullTab[rowIndex][1][:miscFullTab[rowIndex][1].index('Room')].split(',')
        if 'Porterage' in miscFullTab[rowIndex][0] or 'Porterage' in miscFullTab[rowIndex][1]:
            number, rate = MyTable.understand(miscFullTab[rowIndex][3])
            porterage = [Date,"Porterage", number, rate, miscFullTab[rowIndex][4], '', '']
            item = 'Porterage'
        if 'Parking' in miscFullTab[rowIndex][0] or 'Parking' in miscFullTab[rowIndex][1]:
            noOfDays = noOfDays + 1
            perDayRate = miscFullTab[rowIndex][4]
            item='Parking'
        if 'Package' in miscFullTab[rowIndex][0]:
            newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in miscFullTab[rowIndex][3])
            listOfNum = newstr.split()
            packageTab.append([Date,miscFullTab[rowIndex][0],listOfNum[0],float(miscFullTab[rowIndex][4])/float(listOfNum[0]),miscFullTab[rowIndex][4],'',''])
        if 'Package' in miscFullTab[rowIndex][1]:
            item = 'Package'
            newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in miscFullTab[rowIndex][3])
            listOfNum = newstr.split()
            packageTab.append([Date, miscFullTab[rowIndex][1], listOfNum[0],
                              float(miscFullTab[rowIndex][4]) / float(listOfNum[0]), miscFullTab[rowIndex][4], '', ''])
        if 'Guest Tota' in miscFullTab[rowIndex][2] and item =='Parking':
            if len(names) == 0:
                parkingTab.append(['', '', noOfDays, perDayRate, float(perDayRate)*noOfDays, '', ''])
            elif len(names) == 1:
                parkingTab.append([names[0], '', noOfDays, perDayRate, float(perDayRate)*noOfDays, '', ''])
            else:
                parkingTab.append([names[0], names[1], noOfDays, perDayRate, float(perDayRate)*noOfDays, '', ''])
        if 'Housekeeping' in miscFullTab[rowIndex][3]:
            number, rate = MyTable.understand(miscFullTab[rowIndex-1][3])
            gratuity.append([miscFullTab[rowIndex-1][0][:9],'Housekeeping',number,rate,miscFullTab[rowIndex-1][4],'',''])
            item = 'House Keeping'

    miscShortTab.extend(packageTab)
    miscShortTab.append(porterage)
    miscShortTab.extend(gratuity)
    if parkingTab!=[]:
        miscShortTab.extend([["Parking","","","","","",""]])
    miscShortTab.extend(parkingTab)
    return miscShortTab

def getMiscTable(readResults,startPage):
    miscTab = []
    for pageNum in range(startPage, len(readResults)):
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            cell = readResults[pageNum]["lines"][lineNum]['text']
            if 'Parking' in cell or 'Porterage' in cell or 'Package' in cell:
                startPage = pageNum
    pgStrEndStrings = [["Date", "Description", "Charges", "Credits"], ["Guest Signature", "Telephone"]]
    fixedValList = [["Date"], ["Parking","Porterage","Package"],["Guest Tota"],["packages","bags","Routed From"], ["Charges"]]
    fixedAllign = ['c', 'l','r', 'l' ,'r']
    bodyAllign = ['l', 'l', 'r','l', 'r']
    tableCords, startPageNum, endPageNum = MyTable.getTableCordsFromPageNo(readResults,
                                                                           pgStrEndStrings, fixedValList, fixedAllign,
                                                                           startPage)
    miscFullTab = MyTable.getTable(readResults, tableCords, startPageNum, endPageNum, bodyAllign)
    miscOtherTab=getMiscOtherShortTab(miscFullTab)
    flag=False
    mealList=['Dinner','Liquor','Food','Wine','Beer','Breakfast','Lunch','Stinger','Minibar','Dining','Beverage']
    for pageNum in range(endPageNum, len(readResults)):
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            cell = readResults[pageNum]["lines"][lineNum]['text']
            for meal in mealList:
                if meal in cell:
                    startPage = pageNum
                    flag=True
                    break
        if flag:
            break
    pgStrEndStrings = [["Date", "Description", "Charges", "Credits"], ["Guest Signature", "Telephone"]]
    fixedValList = [["Date"], mealList,["Guest Tota","Sub Tota"], ["Charges"]]
    fixedAllign = ['c', 'l','r' ,'r']
    bodyAllign = ['l', 'l', 'r', 'r']
    tableCords, startPageNum, endPageNum = MyTable.getTableCordsFromPageNo(readResults,
                                                                           pgStrEndStrings, fixedValList, fixedAllign,
                                                                           startPage)
    miscFullTab = MyTable.getTable(readResults, tableCords, startPageNum, endPageNum, bodyAllign)
    miscMealsTab=[["Meals",'','','','','','']]
    miscMealsTab.extend(getMiscMealsShortTab(miscFullTab))
    miscTab.extend(miscOtherTab)
    miscTab.extend(miscMealsTab)
    return miscTab, endPageNum


def getAVTable(readResults,startPage):
    avTab=[]
    stPage=0
    for pageNum in range(startPage, len(readResults)):
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            cell = readResults[pageNum]["lines"][lineNum]['text']
            if 'Audio' in cell:
                stPage=pageNum
                break
        if stPage!=0:
            break
    pgStrEndStrings = [["Date", "Description", "Charges", "Credits"], ["Guest Signature", "Telephone"]]
    fixedValList = [["Date"], ["Audio"], ["Charges"]]
    fixedAllign = ['c','l','r']
    bodyAllign = ['l', 'l','r']
    tableCords, startPageNum, endPageNum = MyTable.getTableCordsFromPageNo(readResults,
                                                                           pgStrEndStrings, fixedValList, fixedAllign,
                                                                           stPage)
    avFullTab = MyTable.getTable(readResults, tableCords, startPageNum, endPageNum, bodyAllign)

    for rowIndex in range(0, len(avFullTab)):
        for colIndex in range(0, len(avFullTab[rowIndex])):
            item = avFullTab[rowIndex][colIndex]
            if "Audio" in item:
                Date=avFullTab[rowIndex][colIndex-1]#change date format
                avTab.append([Date,"AV",'1','',avFullTab[rowIndex][colIndex+1],'',''])
    return avTab,endPageNum

def getFoodTable(readResults,start):
    IsStarted = False
    foodTab=[]
    DescList=["Food","Room Rental"]
    Desc=''
    Date=''
    DateList=[]
    Meal=''
    mealsList = [['Dinner','DIN','Break','Breakfast','AMBK','PMBK','LUN','Lunch'],['Dinner','Dinner','Breakfast','Breakfast','AM Breakfast','PM Breakfast','Lunch','Lunch']]
    weekDays=["Sunday","Monday","Tueday","Wednesday","Thursday","Friday","Saturday"]
    for pageNum in range(start, len(readResults)):
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            cell = readResults[pageNum]["lines"][lineNum]['text']
            if 'Post As' in cell or 'BEO' in cell or 'Created' in cell:
                IsStarted=True
            if IsStarted:
                if any(x in cell for x in DescList):
                    Desc = cell.replace("Quantity","") +" "+ Meal + " Day " + str(len(DateList))
                if 'Tota' in cell and 'Grand' not in cell:
                    Total,page = MyTable.nextVal(cell, readResults, pageNum,lineNum)
                    foodTab.append([Date, Desc, '1', '', Total, '', ''])
                if any(x in cell for x in weekDays):
                    Date = cell[cell.index('day') + 4:]
                    if Date not in DateList:
                        DateList.append(Date)
                if any(x in cell for x in mealsList[0]):
                    for meal in mealsList[0]:
                        if meal in cell:
                            Meal = mealsList[1][mealsList[0].index(meal)]
                if 'INFORMATION' in cell:
                    return foodTab,pageNum
                if 'Folio' in cell and IsStarted:
                    return foodTab,pageNum
    return foodTab,pageNum

def getRebateTable(DocResults):
    rebateTable=[]
    rebateBody=[[],[]]
    if DocResults["fields"]["Room Total Final"] != None and DocResults["fields"]["Earned Comps Total Final"] != None and \
            DocResults["fields"]["Food Total Final"] != None:
        newstr = ''.join((ch if ch in '0123456789.,-$()' else ' ') for ch in DocResults["fields"]["Rebate Total Final"]["text"])
        listOfNumbers = newstr.split()
        listOfWords=DocResults["fields"]["Rebate Total Final"]["text"].split(')')
        for num in listOfNumbers:
            if '(' in num:
                number=num.replace(")","")
                for word in listOfWords:
                    if number in word:
                        rebateBody[0].append(word[:word.index("$")])
                        rebateBody[1].append(num)

        for ele in rebateBody[0]:
            rebateTable.append([ele, '', '1', '', "$"+rebateBody[1][rebateBody[0].index(ele)], '', ''])
    else:
        newstr = ''.join(
            (ch if ch in '0123456789.,-$()' else ' ') for ch in DocResults["fields"]["Rebate Total"]["text"])
        listOfNumbers = newstr.split()
        listOfWords = DocResults["fields"]["Rebate Total"]["text"].split(')')
        for num in listOfNumbers:
            if '(' in num:
                number = num.replace(")", "")
                for word in listOfWords:
                    if number in word:
                        rebateBody[0].append(word[:word.index("$")])
                        rebateBody[1].append(num)

        for ele in rebateBody[0]:
            rebateTable.append([ele, '', '1', '', "$" + rebateBody[1][rebateBody[0].index(ele)], '', ''])

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
            if 'Room #' in cell and 'Of' not in cell:
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
                if len(names) == 0:
                    roomShortTab.append(['','',noOfDays,perDayRate,guestTotal,'',''])
                elif len(names) == 1:
                    roomShortTab.append([names[0],'', noOfDays, perDayRate, guestTotal, '', ''])
                else:
                    roomShortTab.append([names[0], names[1], noOfDays, perDayRate, guestTotal, '', ''])
    return roomShortTab,roomRate


def getRoomTable(readResults):
    startIdentifiers = [["NEW", "YORK"], ["INFORMATION", "INVOICE"]]
    endIdentifiers = [["i have received", "the amount shown heron"], ["personally","thath the indicated person"]]
    pgStrEndStrings = [["Date", "Description", "Charges", "Credits"], ["300 W", "Telephone"]]
    fixedValList = [["Date"], ["State Hotel", "*Accomodation"],["Sub Total","Guest Total"], ["Charges"]]
    fixedAllign = ['c', 'l', 'r', 'r']
    bodyAllign = ['l', 'l', 'r', 'r']
    startPage=0
    for pageNum in range(0, len(readResults)):
        for lineNum in range(0, len(readResults[pageNum]["lines"])):
            cell = readResults[pageNum]["lines"][lineNum]['text']
            if 'Accommodation' in cell:
                startPage=pageNum
                break
        if startPage!=0:
            break
    tableCords, startPageNum, endPageNum = MyTable.getTableCordsFromPageNo(readResults,
                                                                 pgStrEndStrings, fixedValList, fixedAllign,startPage)
    roomFullTab = MyTable.getTable(readResults, tableCords, startPageNum, endPageNum, bodyAllign)
    roomTab, roomRate = getRoomShortTab(roomFullTab)
    return roomTab, roomRate,endPageNum



def getAllTables(FRResult,CGResult):
    detailedTable=[]
    allTables={}
    generalDetailsTable,IsRevised,generalDetailsJSON=MyTable.getGeneralDetailsTable(FRResult["analyzeResult"]["documentResults"][0])
    detailedTable.extend(generalDetailsTable)
    overviewTable, tables,overviewJSON = MyTable.getOverviewTable(FRResult["analyzeResult"]["documentResults"][0])
    roomRate = ''
    currentPage=0
    if 'Rebate' in tables[0]:
        rebateTable = getRebateTable(FRResult["analyzeResult"]["documentResults"][0])
        detailedTable.append(["Deposit/Credits", '', '', '', '', '', ''])
        detailedTable.extend(rebateTable)
        allTables.update(MyTable.getDict("Rebate",rebateTable))
    if 'Room' in tables[0]:
        roomTable, roomRate,currentPage = getRoomTable(CGResult["analyzeResult"]["readResults"])
        detailedTable.append(["Room and Tax", '','', '', '', '', tables[1][tables[0].index('Room')]])
        detailedTable.extend(roomTable)
        allTables.update(MyTable.getDict("Room",roomTable))
    if 'Food' in tables[0]:
        foodTable,currentPage = getFoodTable(CGResult["analyzeResult"]["readResults"],currentPage)
        detailedTable.append(["Food and Beverage", '', '', '','', '', tables[1][tables[0].index('Food')]])
        detailedTable.extend(foodTable)
        allTables.update(MyTable.getDict("Food",foodTable))
    if 'AV' in tables[0]:
        avTable,currentPage = getAVTable(CGResult["analyzeResult"]["readResults"],currentPage)
        detailedTable.append(["AV", '', '', '','', '', tables[1][tables[0].index('AV')]])
        detailedTable.extend(avTable)
        allTables.update(MyTable.getDict("AV",avTable))
    if 'Misc' in tables[0]:
        miscTable,endPage = getMiscTable(CGResult["analyzeResult"]["readResults"],currentPage)
        detailedTable.append(["Miscellaneous", '','', '', '', '', tables[1][tables[0].index('Misc')]])
        detailedTable.extend(miscTable)
        allTables.update(MyTable.getDict("Miscellaneous",miscTable))

    return generalDetailsTable, overviewTable, detailedTable, IsRevised,generalDetailsJSON,overviewJSON,allTables