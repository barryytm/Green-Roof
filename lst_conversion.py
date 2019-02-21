import os, shutil, arcpy

arcpy.env.overwriteOutput = True # overwrite

# remove hidden files
def get_files(path):
    files = os.listdir(path)
    for file in files:
        if file[0] == '.':
            files.remove(file)
    return files

def create_dir(origin, landsat):
    dir = origin + "\\" + landsat
    if os.path.exists(dir):
        shutil.rmtree(dir, ignore_errors=True)
    os.makedirs(dir)

def calc_lst(origin, landsat):
    source = origin + "\\landsat" + "\\"+ landsat
    output = origin + "\\output"

    # File locations
    Band_4 = source + "\\" + landsat + "_B4.TIF"
    Band_5 = source + "\\" + landsat + "_B5.TIF"
    Band_10 = source + "\\" + landsat + "_B10.TIF"
    TOA = output + "\\" + landsat + "\\TOA"
    BT = output + "\\" + landsat + "\\BT"
    NDVI = output + "\\" + landsat + "\\NDVI"
    ProVeg = output + "\\" + landsat + "\\ProVeg"
    Emissivity = output + "\\" + landsat + "\\Emissivity"
    LST = output + "\\" + landsat + "\\LST"
    LST_reclass = output + "\\" + landsat + "\\LST_reclass"
    UHI = output + "\\" + landsat + "\\UHI"

    # Calculation of TOA (Top of Atmospheric) spectral radiance
    arcpy.gp.RasterCalculator_sa("0.0003342*'{0}'+0.1".format(Band_10), TOA)

    # TOA to Brightness Temperature conversion
    arcpy.gp.RasterCalculator_sa("(1321.0789/Ln((774.8853/'{0}' )+1))-273.15".format(TOA), BT)

    # Calculate the NDVI
    arcpy.gp.RasterCalculator_sa("Float(Float('{1}'-'{0}')/Float('{1}'+'{0}'))".format(Band_4, Band_5), NDVI)

    # Get the Minimum of NDVI
    NDVI_min = arcpy.GetRasterProperties_management(NDVI, "MINIMUM").getOutput(0)

    # Get the Maximum of NDVI
    NDVI_max = arcpy.GetRasterProperties_management(NDVI, "MAXIMUM").getOutput(0)

    # Calculate the proportion of vegetation
    arcpy.gp.RasterCalculator_sa("Square(('{0}'-{1})/({2}-{1}))".format(NDVI, NDVI_min, NDVI_max), ProVeg)

    # Calculate Emissivity
    arcpy.gp.RasterCalculator_sa("0.004 * '{0}'+ 0.986".format(ProVeg), Emissivity)

    # Calculate the Land Surface Temperature
    arcpy.gp.RasterCalculator_sa("'{0}'/(1+(0.00115*'{0}'/1.4388)*Ln('{1}'))".format(BT, Emissivity), LST)

    # Get the Minimum of LST
    LST_min= arcpy.GetRasterProperties_management(LST, "MINIMUM").getOutput(0)

    # Get the Maximum of LST
    LST_max = arcpy.GetRasterProperties_management(LST, "MAXIMUM").getOutput(0)

    # Get the Mean of LST
    LST_mean = arcpy.GetRasterProperties_management(LST, "MEAN").getOutput(0)

    # Get the Standard Deviation of LST
    LST_STD = arcpy.GetRasterProperties_management(LST, "STD").getOutput(0)

     # Calculate the Urban Heat Island effect
    arcpy.gp.RasterCalculator_sa("'{0}'+(float({1})+(float({2})/2)) - '{0}'".format(LST, LST_mean, LST_STD), UHI)

    # NEED: Double check the thresholds
    # # For reclassification
    # LST_STD_above_mean = str(float(LST_mean) + float(LST_STD))
    # LST_STD_below_mean = str(float(LST_mean) - float(LST_STD))
    # LST_STD_double_above_mean = str(float(LST_mean) + 2*float(LST_STD))
    # LST_STD_double_below_mean = str(float(LST_mean) - 2*float(LST_STD))
    # new_class = "{0} {1} 1;{1} {2} 2;{2} {3} 3;{3} {4} 4;{4} {5} 5;{5} {6} 6".format(LST_min, LST_STD_double_below_mean, LST_STD_below_mean, LST_mean, LST_STD_above_mean, LST_STD_double_above_mean , LST_max)

    # # Reclassify LST
    # arcpy.gp.Reclassify_sa(LST, "VALUE", new_class, LST_reclass, "DATA")

if __name__ == "__main__":
    origin = "C:\\Users\\barry\\Desktop\\ggr462\\Green-Roof"
    dirs = get_files(origin + "\\landsat")
    for folder in dirs:
        # create_dir(origin + "\\output", folder) # creat out put folders
        calc_lst(origin, folder)
