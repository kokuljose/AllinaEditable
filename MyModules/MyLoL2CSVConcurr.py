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
        sum=sum+float(val)
    return round(sum,2)


def formatTable(Event, IONum, GLCode, Category, Table):
    tab=[]
    for row in Table:
        tab.append([Event[0], IONum[0], GLCode[0], Category,row[2],row[4],row[4]])
    return tab


def formatRoomTable(Event, IONum, GLCode, Category, RoomTable):
    tab=[Event[0], IONum[0], GLCode[0], Category,getSumofList(RoomTable,2),RoomTable[0][3],getSumofList(RoomTable,4)]
    return tab
def getMealsParking(Event, IONum, GLCode, Category,MealsParkingTable):
    tab=[]
    qty=0.0
    amt=0.0
    rate=0.0
    for row in MealsParkingTable:
        if row[0] == "Parking":
            continue
        if row[0] == "Meals":
            tab.append([Event, IONum, GLCode, Category,qty,rate,amt])
            break
        else:
            qty=qty+float(row[2])
            rate=rate+float(row[3])
            amt=amt+float(row[4])
    qty = 0.0
    amt = 0.0
    mealTab=False
    for row in MealsParkingTable:
        if row[0] == "Meals":
            mealTab=True
            continue
        elif mealTab:
            qty=qty+float(row[2])
            amt=amt+float(row[4])
    tab.append([Event, IONum, GLCode, Category, qty, amt, amt])
    return tab
def formatMiscTable(Event, IONum, GLCode, Category, MiscTable):
    tab = []
    for row in MiscTable:
        if row[0] =="Meals" or row[0] =="Parking":
            tab.extend(getMealsParking(Event[0], IONum[0], GLCode[0], Category,MiscTable[MiscTable.index(row):]))
            return tab
        else:
            tab.append([Event[0], IONum[0], GLCode[0], Category, row[2], "-" + row[4], "-" + row[4]])
    return tab
def getTabDetails(allTables,Event,IONum):
    CSVTab=[]
    RebateTable=getTabFromList(allTables[1][1])
    RoomTable = getTabFromList(allTables[3][1])
    FoodTable = getTabFromList(allTables[5][1])
    AVTable = getTabFromList(allTables[7][1])
    MiscTable = getTabFromList(allTables[9][1])
    rebateTable = formatTable(Event[1], IONum[1], allTables[0][1], "AdvisorForums-", RebateTable)
    roomTable = formatRoomTable(Event[1], IONum[1], allTables[2][1], "AdvisorForums-", RoomTable)
    foodTable = formatTable(Event[1], IONum[1], allTables[2][1], "AdvisorForums-", FoodTable)
    avTable = formatTable(Event[1], IONum[1], allTables[2][1], "AdvisorForums-", AVTable)
    miscTable = formatMiscTable(Event[1], IONum[1], allTables[2][1], "AdvisorForums-", MiscTable)
    CSVTab.extend(rebateTable)
    CSVTab.append(roomTable)
    CSVTab.extend(foodTable)
    CSVTab.extend(avTable)
    CSVTab.extend(miscTable)
    return CSVTab


def getGeneralDetails(valueList):
    genTab=[]
    for row in valueList:
        genTab.append([row[0],row[1][0],"","","","",""])
    return genTab


def getCSVLoL(allTables):
    CSVTab=[]
    generalDetails=getGeneralDetails(allTables[:-10])
    tabDetails=getTabDetails(allTables[-10:],allTables[1],allTables[5])
    CSVTab.extend(generalDetails)
    CSVTab.extend(tabDetails)
    CSVTab.append(["","","","","","Total",allTables[9][1][0]])
    return CSVTab
