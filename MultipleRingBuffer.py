import sys ,os, copy
from osgeo import ogr,osr

grouseSHP = "C:\\Scratch\\SageScratch\\plyGrouse_Al.shp"

sys.path.append("N:\\SHC\\2_Projects\\009_JuniperRemoval_SageGrouse\\41_ProximityAnalysis\\")
sys.path.append("U:\\04_Programming\\01_Py\\")
from ogrTools import erase
from OGRbuffer import buffer

def DeleteSHP(inputFileName):
    DriverName = "ESRI Shapefile"      # e.g.: GeoJSON, ESRI Shapefile
    FileName = inputFileName
    driver = ogr.GetDriverByName(DriverName)
    if os.path.exists(FileName):
        driver.DeleteDataSource(FileName)
        return 1
    else:
        return 0


def OGRMerge(input1,input2,output):
    os.system("ogr2ogr "+output+" "+input1)
    os.system("ogr2ogr -update -append "+output+" "+input2+" -nln merged")

def merger(listInputSHP,outputFilename):
    numFiles = len(listInputSHP)
    k = 0
    while k < numFiles - 1:
        OGRMerge(listInputSHP[k],listInputSHP[k+1], outputFilename)
        k = k+1

listDist = [5,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
listSort = copy.deepcopy(listDist)
listSort.sort(reverse=True)
inputSHP = ''
filePathName1 = "C:\\Scratch\\SageScratch\\workAllCirs\\outs\\plyGrouse"
filePathName2 = ".shp"
filePathNameOut = "_erased.shp"

k = 1  # k counts Grouse

while k < 3431:   # that's how many grouses, key off GID ('grouse ID')
    print "starting",k
    os.chdir("C:\\Scratch\\SageScratch")
        # create a new data source and layer

        #export point

    thisGrouseDir = "C:\\Scratch\\SageScratch\\grouses\\"+str(k)
    os.mkdir( thisGrouseDir ) 
    for dist in listDist:
        thisSHP = "ptsGrouse_All_"+str(dist)+"m.shp"		
        os.system('''ogr2ogr -where GID="'''+str(k)+'''" '''+thisGrouseDir+" "+thisSHP)

    os.chdir(thisGrouseDir)


    print listSort
    listDel = []
    for items in listSort:

        print items
        nextIndex = listSort.index(items) + 1
        thisIndex = nextIndex - 1
        if nextIndex == len(listSort):
            pass
        else: 
            thisSHP = "ptsGrouse_All_"+str(listSort[thisIndex])+"m.shp"
        #print thisSHP
            nextSHP = "ptsGrouse_All_"+str(listSort[nextIndex])+"m.shp"
            ringSHP = "ptsGrouse_All_"+str(listSort[thisIndex])+"m_ring.shp"
            listDel.append("ptsGrouse_All_"+str(listSort[thisIndex])+"m_ring.shp")
            erase(thisSHP,nextSHP,ringSHP)
            DeleteSHP(thisSHP)
    listDel.append("ptsGrouse_All_5m.shp")
    nameOut = "grouse"+str(k)+"rings.shp"

    print listDel, "LENGTH:",len(listDel)
 	
    k = k+1