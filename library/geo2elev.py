from osgeo import gdal  # osgeo gdal only works in Ubuntu
import sys
import math
from statistics import mean
import geojson
import json
from geojson import FeatureCollection, Feature, Point, LineString

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

def read_tiff (tiff_file, lat, lon):
    data = gdal.Open(tiff_file) 
    band1 = data.GetRasterBand(1)
    GT = data.GetGeoTransform()
    # GDAL's Affine Transformation (GetGeoTransform) 
    # https://gdal.org/tutorials/geotransforms_tut.html
    # GetGeoTransform translates latitude, longitude to pixel indices
    # GT[0] and GT[3] define the "origin": upper left pixel 
    x_pixel_size = GT[1]    #horizontal pixel size
    y_pixel_size = GT[5]    #vertical pixel size
    xP = int((lon - GT[0]) / x_pixel_size )
    yL = int((lat - GT[3]) / y_pixel_size )
    # without rotation, GT[2] and GT[4] are zero
    return ( int ( band1.ReadAsArray(xP,yL,1,1) ) )

# Determine file name of GeoTIFF file based on latitude longitude
# For square tiles with 1 pixel overlap. Not for square tiles with non-overlapping pixels.
# Minor style difference between NASA ASTER and USGS EarthExplorer
# NASA ASTER use N E S W; USGS use lowercase n e s w
# NASA does not use _ in the file name, USGS uses _ as a separator
# returned file name is made to look the same as traditional .HGT except .TIF
# File type supported: GeoTIFF, DTED, HGT, BIL
# Square overlapping or non-overlapping rasters supported
# Rectangular rasters supported
# GeoTIFF with LZW compression supported

if len(sys.argv) < 2:
    print("Please enter a geojson file to add elevation ")
    sys.exit(1)

basket = []       
data = geojson.load(open( sys.argv[1] + '.geojson'))

for i in range(len(data['features'])):
    try:
        myname = data['features'][i]['properties']['name']
    except:
        try:
            myname = data['features'][i]['properties']['Name']
        except:
            myname = 'noname'

    geom = data['features'][i]['geometry']
    xyz = geom['coordinates'] 
    xyz_tricky = geom['coordinates'][0] #tricky: first element of list of list is also a list

    if geom['type'] == 'Point':
        longitude = xyz[0]
        latitude = xyz[1]
        tiff_name = '../geotiff/' + find_tiff ( latitude, longitude )
        elev = read_tiff (tiff_name, latitude, longitude)
        my_point = Point((longitude, latitude, elev))
        my_feature = Feature(geometry=my_point, properties={"name":myname})
        basket.append(my_feature)

    elif ( geom['type'] == 'Polygon' ):  # if Polygon, calculate centroid and treat it as a Point
        node = geom['coordinates'][0]  # Polygon: first element of a list of lists is the list of coordinates
        bucket1=[]
        bucket2=[]
        for j in range(len(node)-1):  # skip the duplicated last node, which is the same as first node.
            bucket1.append( node[j][1] )
            bucket2.append( node[j][0] )
        latitude = mean(bucket1)
        longitude = mean(bucket2)
        label = myname
        tiff_name = '../geotiff/' + find_tiff ( latitude, longitude )
        elev = read_tiff (tiff_name, latitude, longitude)
        my_point = Point((longitude, latitude, elev))
        my_feature = Feature(geometry=my_point, properties={"name":'Ploygon Centroid'})
        basket.append(my_feature)

    elif geom['type'] == 'LineString':
        coords = xyz  # list of tuples
        str_list = []
        for j in coords:
            longitude = j[0]
            latitude = j[1]
            tiff_name = '../geotiff/' + find_tiff ( latitude, longitude )
            elev = read_tiff (tiff_name, latitude, longitude)
            str_list.append([longitude, latitude, elev])
        my_line = LineString(str_list)
        my_feature = Feature(geometry=my_line, properties={"name":myname})
        basket.append(my_feature)   

geojson_string = json.dumps(FeatureCollection(basket), indent=2, ensure_ascii=False)
#print(geojson_string)

with open(sys.argv[1]  + '.geojson', 'w') as outfile:
    outfile.write( geojson_string )
