# determine file name of GeoTIFF file based on latitude longitude
# For square tiles: 1 degree x 1 degree, 1 pixel overlap. 
# Minor style difference between NASA ASTER and USGS EarthExplorer
# NASA ASTER use N E S W; USGS use lowercase n e s w
# NASA does not use _ in the file name, USGS uses _ as a separator


import math

def find ( latitude, longitude ):
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
    
