# add elevation data to GeoJSON
# all required GeoTiff files are assumed to be stored on local drive and in ../geotiff/ relative to this python code
# Linux: sudo apt install gdal-bin   
# Windows: install miniconda
#   conda install conda-forge::gdal

from osgeo import gdal
import sys
import math
import json
from geojson import FeatureCollection, Feature, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection

# Determine file name of GeoTIFF file based on latitude longitude
# NASA ASTER use N E S W; USGS use lowercase n e s w
# NASA does not use _ in the file name, USGS uses _ as a separator
# returned file name is made to look similar to traditional .HGT
# File type supported: GeoTIFF, DTED, HGT, BIL
# Square overlapping or non-overlapping rasters are also supported
# Rectangular rasters are supported
# GeoTIFF with LZW compression are supported

def find_tiff(latitude, longitude):
    if (latitude >= 0.0 and longitude >= 0.0):
        hemi, meri = "N", "E"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.floor(longitude):03d}"
    elif (latitude >= 0.0 and longitude < 0.0):
        hemi, meri = "N", "W"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif (latitude < 0.0 and longitude < 0.0):
        hemi, meri = "S", "W"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif (latitude < 0.0 and longitude >= 0.0):
        hemi, meri = "S", "E"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.floor(longitude):03d}"
    return f"{hemi}{t1}{meri}{t2}.tif"

def extract(tiff_file, lat, lon):
    gdal.UseExceptions()
    data = gdal.Open(tiff_file)
    band1 = data.GetRasterBand(1)
    GT = data.GetGeoTransform()
    # GDAL's Affine Transformation (GetGeoTransform) 
    # https://gdal.org/tutorials/geotransforms_tut.html
    # GetGeoTransform translates latitude, longitude to pixel indices
    # GT[0] and GT[3] define the "origin": upper left pixel 
    x_pixel_size = GT[1]
    y_pixel_size = GT[5]
    xP = int((lon - GT[0]) / x_pixel_size)
    yL = int((lat - GT[3]) / y_pixel_size)
    # without rotation, GT[2] and GT[4] are zero
    array_result = band1.ReadAsArray(xP, yL, 1, 1)
    single_element = array_result[0, 0]
    integer_value = int(single_element)
    return integer_value

def add_elevation_to_coords(coords):
    new_coords = []
    for coord in coords:
        longitude, latitude = coord[0], coord[1]
        tiff_name = '../geotiff/' + find_tiff(latitude, longitude)
        elev = extract(tiff_name, latitude, longitude)
        new_coords.append([longitude, latitude, elev])
    return new_coords

def process_geometry(geom, name):               #recursive function to handle GeometryCollection object
    if geom['type'] == 'GeometryCollection':    
        geometries = []
        for g in geom['geometries']:             
            geometries.append(process_geometry(g, name))   #recursive calls
        return GeometryCollection(geometries)
    else:
        coords = geom.get('coordinates')
        if coords is not None:
            if geom['type'] == 'Point':
                longitude, latitude = coords[0], coords[1]
                tiff_name = '../geotiff/' + find_tiff(latitude, longitude)
                elev = extract(tiff_name, latitude, longitude)
                return Point((longitude, latitude, elev))
            elif geom['type'] == 'LineString':
                new_coords = add_elevation_to_coords(coords)
                return LineString(new_coords)
            elif geom['type'] == 'Polygon':
                new_coords = [add_elevation_to_coords(ring) for ring in coords]
                return Polygon(new_coords)
            elif geom['type'] == 'MultiPoint':
                new_coords = add_elevation_to_coords(coords)
                return MultiPoint(new_coords)
            elif geom['type'] == 'MultiLineString':
                new_coords = [add_elevation_to_coords(line) for line in coords]
                return MultiLineString(new_coords)
            elif geom['type'] == 'MultiPolygon':
                new_coords = [[add_elevation_to_coords(ring) for ring in polygon] for polygon in coords]
                return MultiPolygon(new_coords)
        return None

with open(sys.argv[1] + '.geojson', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

features = []

for feature in data['features']:
    myname = feature['properties'].get('name', feature['properties'].get('Name', 'noname'))
    geom = feature['geometry']
    processed_geom = process_geometry(geom, myname)
    if processed_geom is not None:
        my_feature = Feature(geometry=processed_geom, properties={"name": myname})
        features.append(my_feature)

new_string = json.dumps(FeatureCollection(features), indent=2, ensure_ascii=False)

#with open(sys.argv[1] + '_processed.geojson', 'w') as outfile:
with open(sys.argv[1] + '.geojson', 'w') as outfile:
    outfile.write(new_string)
