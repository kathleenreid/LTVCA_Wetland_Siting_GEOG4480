import arcpy
import numpy as np
from arcpy.sa import *
arcpy.env.workspace = "C:/Users/Casey Trombley/University of Guelph/Final MCE Input Files - Final Version"

 


#Variables to hold the names of the suitability mask and transformed criteria layers.

 

print ("Setting scenario variables")
constraintMask = "Constraint_Mask_30m_CLIP2.tif"
slopeRast = "LTVCA_Slope_Normal_CLIP.tif"
soilRast = "Soil_Survey_Complex_Reclass_30m_Normal_CLIP.tif"
depthRast = "Depth_In_Sink_Normal_CLIP.tif"
wetRast = "LTVCA_WetnessIndex_Normal_CLIP.tif"
landRast = "SOLRIS_LC_Normal_CLIP_3.tif"
tileRast = "LTVCA_Tile_Drainage_Normal_CLIP_2.tif"

 

weightSlope = 0.058
weightSoil = 0.3899
weightDepth = 0.0597
weightWet = 0.1572
weightLand = 0.3003
weightTile = 0.035

 


# Create list to hold the sensitivity scenarios
# Each scenario will test increasing one weight by 0.01 while decreasing the other 5 by 0.002

 

listScenarios = ["Slope", "Soil Type", "Depth in Sink", "Wetness Index", "Land Cover", "Tile drainage"]

 

# Loop through each scenario to creaste a scenario-specific suitability layer

 

scenNum = 0 # This is to help with creating output names below
for scenario in listScenarios:
    print ("Processing " + scenario + " scenarios")
    i = 0.01 # Initial weight increase for each set of scenarios
    #for i in np.arange(0.01,0.11,0.01):
    while i <= 0.1: #The most we'll increase a specific weight is by 0.1
        print ("    Weight + " + str(i))
        
        if scenario =="Slope": #add weight to the slope and take weight from the others
            tempWeightSlope = weightSlope + i
            tempWeightSoil = weightSoil - (i/5)
            tempWeightDepth = weightDepth - (i/5)
            tempWeightWet = weightWet - (i/5)
            tempWeightLand = weightLand - (i/5)
            tempWeightTile = weightTile - (i/5)

 


        elif scenario =="Soil Type":
            tempWeightSlope = weightSlope - (i/5)
            tempWeightSoil = weightSoil + i
            tempWeightDepth = weightDepth - (i/5)
            tempWeightWet = weightWet - (i/5)
            tempWeightLand = weightLand - (i/5)
            tempWeightTile = weightTile - (i/5)

 


        elif scenario =="Depth in Sink":
            tempWeightSlope = weightSlope - (i/5)
            tempWeightSoil = weightSoil - (i/5)
            tempWeightDepth = weightDepth + i
            tempWeightWet = weightWet - (i/5)
            tempWeightLand = weightLand - (i/5)
            tempWeightTile = weightTile - (i/5)

 


        elif scenario =="Wetness Index":
            tempWeightSlope = weightSlope - (i/5)
            tempWeightSoil = weightSoil - (i/5)
            tempWeightDepth = weightDepth - (i/5)
            tempWeightWet = weightWet + i
            tempWeightLand = weightLand - (i/5)
            tempWeightTile = weightTile - (i/5)

 


        elif scenario =="Land Cover":
            tempWeightSlope = weightSlope - (i/5)
            tempWeightSoil = weightSoil - (i/5)
            tempWeightDepth = weightDepth - (i/5)
            tempWeightWet = weightWet - (i/5)
            tempWeightLand = weightLand + i
            tempWeightTile = weightTile - (i/5)

 


        else:
            tempWeightSlope = weightSlope - (i/5)
            tempWeightSoil = weightSoil - (i/5)
            tempWeightDepth = weightDepth - (i/5)
            tempWeightWet = weightWet - (i/5)
            tempWeightLand = weightLand - (i/5)
            tempWeightTile = weightTile + i

 


        #Use map algebra to calculate a new suitability raster
        print ("-----Calculating suitability-----")
        scenNum += 1 #Increase scenNum by 1

 

        tempSuitRast = RasterCalculator([constraintMask, slopeRast, soilRast, depthRast, wetRast, landRast, tileRast], ["a","b", "c", "d", "e", "f", "g"], f"a*( ({tempWeightSlope}*b) + ({tempWeightSoil}*c) + ({tempWeightDepth}*d) + ({tempWeightWet}*e) + ({tempWeightLand}*f) + ({tempWeightTile}*g) )")
        tempSuitRast.save(f"C:/Users/Casey Trombley/University of Guelph/Final MCE Input Files - Final Version/{scenario}_Sensitivity" + str(scenNum) + ".tif")
              
        #outRaster = arcpy.env.workspace + r"\SensitivitySuitability" + str(scenNum) #creates the output layer name
        #tempSuitRast = (constraintMask) * ((tempWeightSlope *(slopeRast)) + (tempWeightSoil * (soilRast)) + (tempWeightWet * Raster(wetRast)) + (tempWeightLand * Raster(landRast)) + (tempWeightTile * Raster(tileRast))) #apply MCE equation
        #tempSuitRast.save(outRaster)

 

        i += 0.01 #increases the weight step by 0.01

 

print ("Complete!")