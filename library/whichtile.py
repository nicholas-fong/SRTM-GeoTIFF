import math

def find_tiff ( latitude, longitude ):
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
