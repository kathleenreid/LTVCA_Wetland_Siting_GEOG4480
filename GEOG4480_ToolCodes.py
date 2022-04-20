
#Import the Whitebox Tools module
from WBT.whitebox_tools import WhiteboxTools
import os
#Set working directory for whitebox tools modules and tools
wbt = WhiteboxTools()  # Initialize WhiteboxTools
wdir = "D:\GEOG4480_FinalProject_FinalVersion"
assert(os.path.isdir(wdir))
wbt.work_dir = wdir
wbt.set_verbose_mode(False)


def main():


    #Sink Tool 
    print("Checking for depression filling/presence of sinks")
    wbt.sink(
        i = "LTVCA_DEM_30m.tif", #Input Raster DEM File
        output = "Check_Depression_Filling_Sinks.tif", #Output raster file
        zero_background=False, #Flag indicating whether a background value of zero should be used
    )

    #Slope Tool 
    print("Generating slope raster")
    wbt.slope(
        dem = "LTVCA_DEM_30m.tif", #Input raster DEM file 
        output = "LTVCA_Slope.tif", #Output raster file
        zfactor=None, #Optional multiplier for when vertical and horizonal units are not the same
        units="degrees", #Units of output raster (Deg, Rad, Percent)
    )

    #Depth-In-Sink Tool 
    print("Generating Depth in Sink Raster")
    wbt.depth_in_sink(
        dem = "LTVCA_DEM_30m.tif", #Input raster DEM file 
        output = "Depth_In_Sink.tif", #Output raster file
        zero_background=False, #Flag indicating whether a background value of zero should be used
    )

    #Specific contributing area flow accumulation 
    print("Generating Specific Contributing Area Flow Accumulation Raster")
    wbt.quinn_flow_accumulation(
        dem = "LTVCA_DEM_30m.tif",
        output = "SCA_Flow_Accumulation.tif",
        out_type="specific contributing area",
        exponent=1.0,
        threshold=None,
        log=False,
        clip=False,
    )

    #Total upslope contributing area flow accumulation 
    print("Generating Total Upslope Contributing Area Flow Accumulation Raster")
    wbt.quinn_flow_accumulation(
        dem = "LTVCA_DEM_30m.tif",
        output = "TCA_Flow_Accumulation.tif",
        out_type ="catchment area",
        exponent=1.0,
        threshold=None,
        log=False,
        clip=False,
    )
   
    #Wetness index
    print("Calculating Wetness Index")
    wbt.wetness_index(
        sca = "SCA_Flow_Accumulation.tif", 
        slope = "LTVCA_Slope.tif", 
        output = "LTVCA_WetnessIndex.tif", 
    )



main ()
