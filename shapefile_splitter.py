#shapefile_splitter.py - Andrew Munsch, 2014
#Takes an input feature class, and copies each feature to a new feature class (shapefile) and saves it to a folder of your choice.

#imports-----------

import arcpy, sys, cmd

##User inputs--------
inTiles = sys.argv[1]  #file to split
outFolder = sys.argv[2]        #location of new feature classes
lazToolFolder = sys.argv[3]
lazFolder = sys.argv[4]     #location of lAZ files to be clipped to DNR tile scheme
lazOut = sys.argv[5]        #Location of clipped LAZ files. 


#Create search cursor for input data.
tile_cursor = arcpy.SearchCursor(inTiles)

#Make a feature layer to copy the feature from.
arcpy.MakeFeatureLayer_management(inTiles,"tempfile")

#Loop through each feature in the feature class and create a new shapfile containing the individual feature.
for row in tile_cursor:
    tileName = row.getValue("DNR_QQQ_ID") #to create the file name. 
    tileName_nodash = tileName.replace("-","_") #because shapefiles do not allow dashes.
    outputpath = outFolder + "\\" + tileName_nodash + ".shp"
    tileQ = """"DNR_QQQ_ID" = '""" + tileName + """'"""  #Build an SQL querey to select the desired feature.
    print tileQ
    arcpy.SelectLayerByAttribute_management("tempfile", "NEW_SELECTION", tileQ) #selects the feature to be copied.
    arcpy.CopyFeatures_management("tempfile",outputpath) #Creates the new shapefile. 
    
    #example command line string: lasclip -i path/*.laz -poly poly.shp -out path/tilename.laz 
    
    commandString = lazToolFolder + "lasclip -i " + lazFolder +"*.laz " + "-poly " + outputpath + " -out " + lazOut + tileName + ".laz" 
    cmd(commandString)

del tile_cursor
del row
