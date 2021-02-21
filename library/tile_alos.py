# tile filename algorithm to find appropriate ALOS non overlapping SRTM file.
# ALOS tiles are 6000 x 6000 non-overlapping; the algorithm is different than overlapping tiles.

import math

def find( latitude, longitude ):

    if ( latitude >= 0.0 and longitude >= 0.0 ): 
        hemi, meri = "N" "E"  
        if ( latitude > math.floor(latitude)):
            t1 = math.floor(latitude)
        else:
            t1 = math.floor(latitude) - 1
        if ( longitude < math.ceil(longitude )):
            t2 = math.floor(longitude)
        else:
            t2 = math.ceil(longitude)

    elif ( latitude >= 0.0 and longitude < 0.0 ):
        hemi, meri = "N" "W"
        if ( latitude > math.floor(latitude)):
            t1 = math.floor(latitude)
        else:
            t1 = math.floor(latitude) - 1
        if ( longitude < math.ceil(longitude )):
            t2 = abs (math.floor(longitude))
        else:
            t2 = abs (math.ceil(longitude))

    elif ( latitude < 0.0 and longitude < 0.0 ):
        hemi, meri = "S" "W"
        if ( latitude >  math.floor(latitude) ):
            t1 = abs((math.floor(latitude)))
        else:
            t1 = abs((math.floor(latitude ) - 1))
        if ( longitude < math.ceil(longitude )):
            t2 = abs(math.floor(longitude))
        else:
            t2 = abs(math.ceil(longitude))

    elif ( latitude < 0.0 and longitude >= 0.0 ):
        hemi, meri = "S" "E"
        if ( latitude >  math.floor(latitude) ):
            t1 = abs((math.floor(latitude)))
        else:
            t1 = abs((math.floor(latitude ) - 1))
        if ( longitude < math.ceil(longitude )):
            t2 = math.floor(longitude)
        else:
            t2 = math.ceil(longitude)
        
    return (f"{hemi}{t1:02d}{meri}{t2:03d}.tif")
