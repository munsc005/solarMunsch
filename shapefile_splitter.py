#shapefile_splitter.py - Andrew Munsch, 2014
#Takes an input feature class, and copies each feature to a new feature class (shapefile) and saves it to a folder of your choice.

#imports-----------

import arcpy, sys

##User inputs--------
inTiles = sys.argv[1]  #file to split
outFolder = sys.argv[2]        #location of new feature classes

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

del tile_cursor
del row
