# An algorithm to find the file name for non-overlapping SRTM rasters such as ALOS.
# ALOS rasters are 6000 x 6000 non-overlapping.

import math

def find_tiff( latitude, longitude ):

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


answer = input( "Do you want to enter a latitude , longitude now ? Y or N  ").upper()
if ( answer == 'Y'):
    latlon = input ( "enter latitude, longitude =  ")
    latitude = float(latlon.split(',')[0])
    longitude = float(latlon.split(',')[1])
    print (find_tiff (latitude, longitude))
else:
    tile_list = []
    filename = input ("Enter the filename of a CSV file [.asc is assumed] that contains latitude, longitude :  ")
    with open( filename + '.asc' ) as fp:
        while True:
            input_line = fp.readline()
            if len(input_line) == 0:
                break
            elements = input_line.split(",")
            if len(elements) >= 2:
                try:
                    # Convert the first two elements to float
                    latitude = float(elements[0])
                    longitude = float(elements[1])
                except ValueError:
                    print("Unable to convert to float: Invalid input")
            else:
                print("EOF")
            tile_name = find_tiff ( latitude, longitude )
            tile_list.append( tile_name )

    tile_list = sorted( set( tile_list ) )  # remove duplicate and sort

    for tiles in tile_list:
        print (tiles)
    with open( filename + '-geotiff.asc', 'w') as outfile:
        for tiles in tile_list:
            outfile.write("%s\n" % tiles)
