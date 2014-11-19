
def funNDVI(tif):

    import struct,os,string,re,binascii,glob
    from osgeo import gdal
    import numpy as np

    print tif,"\n"
    tifarr=tif.split('.')
    newtiff=tifarr[0]+'_ndvi.tif'
    print newtiff,"\n"
    tifbands=[]
    g = gdal.Open(tif)
    for i in xrange(1,g.RasterCount+1):
        tifbands.append(g.GetRasterBand(i).ReadAsArray())
    red=np.array(tifbands[0],dtype= float)
    nir=np.array(tifbands[3],dtype= float)
    check = np.logical_and ( red > 1, nir > 1 )
    ndvi = np.where ( check,  (nir - red ) / ( nir + red ),-9) 
    nullnum=-9
    geo = g.GetGeoTransform()  
    proj = g.GetProjection()   
    shape = red.shape        
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create( "temptiff", shape[1], shape[0], 1, gdal.GDT_Float32)
    dst_ds.SetGeoTransform( geo )
    dst_ds.SetProjection( proj )
    dst_ds.GetRasterBand(1).WriteArray(ndvi)
    dst_ds = None;g=None  # save, close
	
    sysCall = "gdalbuildvrt -srcnodata -9  test.vrt temptiff"
    os.system(sysCall)
	
    finaltiff="gdal_translate -of GTiff -co COMPRESS=DEFLATE test.vrt %s"%(newtiff)
    os.system(finaltiff)

def testIsString(input):
    return isinstance(input,basestring)
    
def SuperStacker(listRasters):
    import os
    strList = ""
    outName = listRasters[0].split('.')[0]+"_ss."+listRasters[0].split('.')[1]
    for items in listRasters:
        strList = strList+" "+items
    os.system("gdal_merge -separate "+strList+" -o "+outName)

def StackProcess(input_listTif_or_Tif):
    #if testIsString(input_listTif_or_Tif):
    funNDVI(input_listTif_or_Tif)
    listRast = []
    listRast.append(input_listTif_or_Tif)
    listRast.append(input_listTif_or_Tif.split('.')[0]+"_ndvi."+input_listTif_or_Tif.split('.')[1])
    SuperStacker(listRast)
    
def SuperStackMe(input_listTif_or_Tif):
    if testIsString(input_listTif_or_Tif):
        StackProcess(input_listTif_or_Tif)
    else:
        for f in input_listTif_or_Tif:
            #print f
            StackProcess(f) 

