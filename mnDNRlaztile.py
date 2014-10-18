#mnDNRlaztile.py
#Splits Laz files into Minnesota DNR tile scheme via a shapefile of the desired tiles - Andrew Munsch, 2014


#imports-----------

import arcpy, sys, subprocess, os

##User inputs--------
inTiles = sys.argv[1]  #shapefile with individual tiles "E:\LiDAR_Processing\stearns_testtiles.shp"
outTiles = sys.argv[2] #"E:\LiDAR_Processing\splitscratch"         #location of new feature classes
lasToolsFolder = sys.argv[3] #"E:\LiDAR_Processing\lastools\\bin"  #location of laz tools folder
lasFolder = sys.argv[4] #"E:\LiDAR_Processing\stearns_test"      #location of lAZ files to be clipped to DNR tile scheme
lasScratch = sys.argv[5] #"E:\LiDAR_Processing\stearns_scratch"  
lasOut = sys.argv[6] #"E:\LiDAR_Processing\clippedlaz"           #Location of clipped LAZ files. 

lasToolsFolder = lasToolsFolder + "\\bin"

#Create search cursor for input data.
tile_cursor = arcpy.SearchCursor(inTiles)

#Make a feature layer to copy the feature from.
arcpy.MakeFeatureLayer_management(inTiles,"tempfile")

#Loop through each feature in the feature class and create a new shapfile containing the individual feature.
for row in tile_cursor:
    tileName = row.getValue("DNR_QQQ_ID") #to create the file name. 
    tileName_nodash = tileName.replace("-","_") #because shapefiles do not allow dashes.
    outputpath = outTiles + "\\" + tileName_nodash + ".shp"
    tileQ = """"DNR_QQQ_ID" = '""" + tileName + """'"""  #Build an SQL querey to select the desired feature.
    print tileQ
    arcpy.SelectLayerByAttribute_management("tempfile", "NEW_SELECTION", tileQ) #selects the feature to be copied.
    arcpy.CopyFeatures_management("tempfile",outputpath) #Creates the new shapefile. 
    
    #example commandStringClip Literal: E:\LiDAR_Processing\lastools\bin\lasclip -i E:\LiDAR_Processing\stearns_test\*.laz -poly E:\LiDAR_Processing\splitscratch\3526_20_61.shp -odir E:\LiDAR_Processing\stearns_scratch -olaz
    #example commandStringMerge Literal:  E:\LiDAR_Processing\lastools\bin\lasmerge -i E:\LiDAR_Processing\stearns_scratch\*.laz -o E:\LiDAR_Processing\clippedlaz\3526-20-61.laz
    
    commandStringClip = lasToolsFolder + "\\lasclip -i " + lasFolder + "\\*.laz -poly " + outputpath + " -odir " + lasScratch + " -olaz -cores 8"
    commandStringMerge = lasToolsFolder + "\\lasmerge -i " + lasScratch + "\\*.laz -o " + lasOut + "\\" + tileName + ".laz" 

    subprocess.call(commandStringClip) #clip the laz files
    subprocess.call(commandStringMerge) #merge the clipped laz files
    arcpy.Delete_management(outputpath) #delte the shapefile used to clip the laz files.

#get rid of the pre-merged clipped laz files to avoid issues later on. 
    for the_file in os.listdir(lasScratch):
        file_path = os.path.join(lasScratch, the_file)
        os.unlink(file_path)

del tile_cursor
del row
