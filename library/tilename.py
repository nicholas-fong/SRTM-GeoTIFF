# Determine file name of GeoTIFF file based on latitude longitude
# For square tiles with 1 pixel overlap. Not for square tiles with non-overlapping pixels.
# Minor style difference between NASA ASTER and USGS EarthExplorer
# NASA ASTER use N E S W; USGS use lowercase n e s w
# NASA does not use _ in the file name, USGS uses _ as a separator
# returned file name is made to look the same as traditional .HGT except .TIF

import math

def find ( latitude, longitude ):
    if  ( latitude >= 0.0 and longitude >= 0.0 ):
        hemi, meri = "N", "E"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.floor(longitude):03d}"
    elif ( latitude >= 0.0 and longitude < 0.0 ):
        hemi, meri = "N", "W"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif ( latitude < 0.0 and longitude < 0.0 ):
        hemi, meri = "S", "W"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif ( latitude < 0.0 and longitude >= 0.0 ):
        hemi, meri = "S", "E"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.floor(longitude):03d}"
    return( f"{hemi}{t1}{meri}{t2}.tif" ) 
    
