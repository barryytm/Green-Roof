import os
# import arcpy
# arcpy.env.overwriteOutput

# remove hidden files
def get_files(path):
    files = os.listdir(path)
    for file in files:
        if file[0] == '.':
            files.remove(file)
    return files

MUTI_BAND_10 = "0.0003342"
ADD_BAND_10 = "0.1"

TOA = ""
BT = ""
NDVI = ""


if __name__ == "__main__":
    folder = get_files('./landsat8')
    for i in folder:
        Band_4 = folder + '/' + folder + "_B4.TIF"
        Band_5 = folder + '/' + folder + "_B5.TIF"
        Band_10 = folder + '/' + folder + "_B10.TIF"
