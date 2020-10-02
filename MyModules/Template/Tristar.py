from MyModules import MyTable


def getTravelTable(DocResult):
    travelTable=[]
    if DocResult["fields"]["Invoice Amount"] != None:
        travelTable.append(["Travel Expense", '', '', '', '', DocResult["fields"]["Invoice Amount"]['text'], DocResult["fields"]["Invoice Amount"]['text']])
        travelTable.append(["Travel Expense",'',  DocResult["fields"]["Invoice Amount"]['text'], '', ''])
    elif DocResult["fields"]["Final Invoice Amount"] != None:
        travelTable.append(["Travel Expense", '', '', '', '', DocResult["fields"]["Final Invoice Amount"]['text'], DocResult["fields"]["Final Invoice Amount"]['text']])
        travelTable.append(["Travel Expense", '', DocResult["fields"]["Final Invoice Amount"]['text'], '', ''])
    return travelTable


def getAllTables(FRResult):
    detailedTable=[]
    generalDetailsTable,IsRevised=MyTable.getGeneralDetailsTable(FRResult["analyzeResult"]["documentResults"][0])
    detailedTable.extend(generalDetailsTable)
    #overviewTable, tables = MyTable.getOverviewTable(FRResult["analyzeResult"]["documentResults"][0])
    travelTable=getTravelTable(FRResult["analyzeResult"]["documentResults"][0])
    detailedTable.extend(travelTable)
    return generalDetailsTable,detailedTable