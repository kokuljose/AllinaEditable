from MyModules.Template import OMNI,Intercontinental,TravelPros,Cooper
from MyModules import MyTable,MyLoL2DOCX
def GetTableFromJSON(CGResult,FRResult,filename,excelFileName):
    IsRevised=False
    allTables={}
    # if 'OMNI Hotels & Resorts' in FRResult["analyzeResult"]["documentResults"][0]["docType"]:
    #     print("omni")
    #     generalDetailsTable,overviewTable,detailedTable,IsRevised=OMNI.getAllTables(FRResult,CGResult)
    # elif 'Intercontinental' in FRResult["analyzeResult"]["documentResults"][0]["docType"]:
    #     print("intercontinental")
    generalDetailsTable, overviewTable, detailedTable, IsRevised,generalDetailsJSON,overviewJSON,allTables = Intercontinental.getAllTables(FRResult, CGResult,excelFileName)
    # elif 'Cooper' in FRResult["analyzeResult"]["documentResults"][0]["docType"]:
    #     print("cooper")
    #     generalDetailsTable, detailedTable = Cooper.getAllTables(FRResult)
    # elif 'TravelPros' in FRResult["analyzeResult"]["documentResults"][0]["docType"]:
    #     generalDetailsTable, detailedTable = TravelPros.getAllTables(FRResult)
    # elif 'Tristar' in FRResult["analyzeResult"]["documentResults"][0]["docType"]:
    #     generalDetailsTable, detailedTable = TravelPros.getAllTables(FRResult)
    print("success")

    MyTable.saveToCSV(detailedTable,filename[:-4]+"Reconciled")
    return generalDetailsJSON,overviewJSON,allTables
    # MyLoL2DOCX.LoL2DOCX(detailedTable,filename[:-4],IsRevised)
