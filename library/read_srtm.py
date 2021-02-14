import sys
import math
import rasterio
import numpy as np

latitude = float(sys.argv[1])
longitude = float(sys.argv[2])

def which_tile ( latitude, longitude ):
    if  ( latitude >= 0.0 and longitude >= 0.0 ):
        hemi, meri = "n", "e"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.floor(longitude):03d}"
    elif ( latitude >= 0.0 and longitude < 0.0 ):
        hemi, meri = "n", "w"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif ( latitude < 0.0 and longitude < 0.0 ):
        hemi, meri = "s", "w"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif ( latitude < 0.0 and longitude >= 0.0 ):
        hemi, meri = "s", "e"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.floor(longitude):03d}"
    return( f"{hemi}{t1}_{meri}{t2}.tif" )  

def read_elevation(tiff_file, lat, lon):
    src=rasterio.open(tiff_file)
    array=src.read(1)
    #self adjusts to 3 Arc-Second 1201x1201 and 1 Arc-Second 3601x3601
    #also self adjusts to 1201x601 e.g. n53_w007.tif (Dublin)
    y =src.width-1
    x =src.height-1
    if ( lat >= 0.0 ):
        x = round (x  - lat%1 * x )
        y = round ( lon%1 * y )
        return array[ x, y ].astype(np.int16)
    if ( lat < 0.0 ):
        x = round ((1 - lat%1) * x )
        y = round ( lon%1 * y )
        return array[ x, y ].astype(np.int16)


my_file=which_tile(latitude,longitude)
print ( f"GeoTIFF tile used: {my_file}" )

z = read_elevation(my_file,latitude,longitude)
print (f"tiff_file elevation at {latitude:.6f} {longitude:.6f} is {z} meters")            
         
