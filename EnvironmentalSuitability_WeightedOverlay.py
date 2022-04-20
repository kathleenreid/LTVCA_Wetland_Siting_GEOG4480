#!/usr/bin/env python
# coding: utf-8

# In[30]:


get_ipython().run_line_magic('matplotlib', 'inline')
import arcpy
import matplotlib.pyplot as plt
import numpy as np
import os


# STEP 1: READ "TIF" FILE INTO AN ARCPY RASTER
# Format: variable_Raster = arcpy.Raster('file_name.tif')

# In[31]:


Constraint_Mask_Raster = arcpy.Raster('Constraint_Mask_30m_CLIP2.tif')
Slope_Raster = arcpy.Raster('LTVCA_Slope_Normal_CLIP.tif')
SoilType_Raster = arcpy.Raster('Soil_Survey_Complex_Reclass_30m_Normal_CLIP.tif')
DepthInSink_Raster = arcpy.Raster('Depth_In_Sink_Normal_CLIP.tif')
WetnessIndex_Raster = arcpy.Raster('LTVCA_WetnessIndex_Normal_CLIP.tif')
LandCover_Raster = arcpy.Raster('SOLRIS_LC_Normal_CLIP_3.tif')
TileDrainage_Raster = arcpy.Raster('LTVCA_Tile_Drainage_Normal_CLIP_2.tif')


# In[32]:


MaskInfo = Constraint_Mask_Raster.getRasterInfo()
SlopeInfo = Slope_Raster.getRasterInfo()
SoilInfo = SoilType_Raster.getRasterInfo()
DSinkInfo = DepthInSink_Raster.getRasterInfo()
WIInfo = WetnessIndex_Raster.getRasterInfo()
LCInfo = LandCover_Raster.getRasterInfo()
TDInfo = TileDrainage_Raster.getRasterInfo()


# In[33]:


MaskInfo.getCellSize(), MaskInfo.getNoDataValues(), 


# In[34]:


SlopeInfo.getCellSize(), SlopeInfo.getNoDataValues(),


# In[35]:


SoilInfo.getCellSize(), SoilInfo.getNoDataValues(),


# In[36]:


DSinkInfo.getCellSize(), DSinkInfo.getNoDataValues(),


# In[37]:


WIInfo.getCellSize(), WIInfo.getNoDataValues(),


# In[38]:


LCInfo.getCellSize(), LCInfo.getNoDataValues(),


# In[39]:


TDInfo.getCellSize(), TDInfo.getNoDataValues(),


# STEP 2: CONVERT ARCPY RASTER TO A NUMPY ARRAY
# Format: variable_array = arcpy.RasterToNumPyArray(variable)

# In[40]:


Constraint_Mask_Array = arcpy.RasterToNumPyArray(Constraint_Mask_Raster)
Slope_Array = arcpy.RasterToNumPyArray(Slope_Raster)
SoilType_Array = arcpy.RasterToNumPyArray(SoilType_Raster)
DepthInSink_Array = arcpy.RasterToNumPyArray(DepthInSink_Raster)
WetnessIndex_Array = arcpy.RasterToNumPyArray(WetnessIndex_Raster)
LandCover_Array = arcpy.RasterToNumPyArray(LandCover_Raster)
TileDrainage_Array = arcpy.RasterToNumPyArray(TileDrainage_Raster)


# STEP 3: ASSIGN EACH VARIABLE ARRAY TO A SHORTHAND VARIABLE NAME 
# Format: var = variable_array

# In[41]:


Mask = Constraint_Mask_Array 
Slope = Slope_Array 
Soil = SoilType_Array 
DSink = DepthInSink_Array 
WI = WetnessIndex_Array 
LC = LandCover_Array 
TD = TileDrainage_Array 


# STEP 4: PRINT SHAPE OF ARRAY
# Format: print(var.shape)

# In[42]:


print(Mask.shape) 
print(Slope.shape) 
print(Soil.shape)  
print(DSink.shape) 
print(WI.shape)  
print(LC.shape)  
print(TD.shape) 


# STEP 5: SAVE ARRAY DIMENSIONS TO VARIABLES

# In[43]:


#Mask
a = 3213
b = 3803

#Slope
c = 3213
d = 3803

#Soil
e = 3213
f = 3803

#DSink
g = 3213
h = 3803

#WI
i = 3213
j = 3803

#LC
k = 3213
l = 3803

#TD
m = 3213
n = 3803


# STEP 6: CREATE NEW EMPTY ARRAYS TO STORE WeightedVar's
# Format: WeightedVar = np.zeros( (h,w), dtype = np.uint8)

# In[44]:


WeightedSlope = np.zeros((c,d), dtype = np.uint8) 
WeightedSoil = np.zeros((e,f), dtype = np.uint8)  
WeightedDSink = np.zeros((g,h), dtype = np.uint8)
WeightedWI = np.zeros((i,j), dtype = np.uint8)  
WeightedLC = np.zeros((k,l), dtype = np.uint8) 
WeightedTD = np.zeros((m,n), dtype = np.uint8) 


# STEP 7: CALCULATE WEIGHTED VALUES OF MATRIX AND ASSIGN TO A NEW VARIABLE 
# Format: WeightedVar = (var*weightValue)

# In[45]:


WeightedSlope = np.multiply(Slope,0.057991856) 
WeightedSoil = np.multiply(Soil,0.389860485)
WeightedDSink = np.multiply(DSink,0.059661516)
WeightedWI = np.multiply(WI,0.157197046)   
WeightedLC = np.multiply(LC,0.300290629) 
WeightedTD = np.multiply(TD,0.034998469) 


# STEP 8: SUM ALL "WeightedVar"s AND SAVE TO A NEW VARIABLE 
# Format: WeightedSum = (WeightedVar + WeightedVar + .... + WeightedVar)

# In[46]:


WeightedSum = np.zeros((3213, 3803), dtype = np.uint8)


# In[47]:


WeightedSum = (WeightedSlope + WeightedSoil + WeightedDSink + WeightedWI + WeightedLC + WeightedTD)


# STEP 9: CREATE NEW EMPTY ARRAY TO STORE FINAL SUITABILITY 
# Format: EnviroSuit = np.zeros ( (h,w), dtype = np.uint8)
# Set h and w to maximum height and width of any of the input arrays

# In[48]:


EnviroSuit = np.zeros ( (3213, 3803), dtype = np.uint8)


# STEP 10: CALCULATE FINAL SUITABILITY BY MULTIPLYING WEIGHTEDSUM BY "ConstraintMask"
# Format: EnviroSuit = (WeightedSum * ConstraintMask)

# In[49]:


EnviroSuit = np.multiply(WeightedSum,Mask)


# In[ ]:





# STEP 11: SET ARCPY ENVIRONMENT VARIABLES AND SAVE FINAL SUITABILTIY AS AN OUTPUT "TIF" RASTER

# In[50]:


### TEMP:
arcpy.env.outputCoordinateSystem = 'Constraint_Mask_30m_CLIP2.tif'
arcpy.env.overwriteOutput = True ## if you don't set this to True, you'll get an error if you run this cell more than once

xmin = 368041.297389
ymin = 4657219.285984
lower_left = arcpy.Point(xmin, ymin)
reclassed_raster = arcpy.NumPyArrayToRaster(EnviroSuit, lower_left, 30, 30)

## change the outfile so that the new files saves to your lab folder
outfile = r"C:/Users/kathl/Documents/Undergraduate/W22/GEOG 4480/GEOG4480_FinalProject_FinalVersion/EnvironmentalSuitability.tif"
reclassed_raster.save(outfile)


# In[52]:


EnivroSuit_Raster = arcpy.Raster('EnvironmentalSuitability.tif')
EnviroSuitInfo = EnivroSuit_Raster.getRasterInfo()
EnviroSuitInfo.getCellSize(), EnviroSuitInfo.getNoDataValues(), 

