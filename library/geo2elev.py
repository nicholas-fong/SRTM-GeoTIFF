from osgeo import gdal
import sys
import math
import json
import re
from geojson import FeatureCollection, Feature, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection

# add elevation data to GeoJSON
# all required GeoTiff files are assumed to be stored on local drive and in ../geotiff/ relative to this python code
# Linux: sudo apt install gdal-bin   
# Windows: install miniconda
#   conda install conda-forge::gdal   open anacoda command prompt  cd to python source files

# Determine file name of GeoTIFF file based on latitude longitude
# NASA ASTER use N E S W; USGS use lowercase n e s w
# NASA does not use _ in the file name, USGS uses _ as a separator
# returned file name is made to look similar to traditional .HGT
# File type supported: GeoTIFF, DTED, HGT, BIL
# Square overlapping or non-overlapping rasters are also supported
# Rectangular rasters are supported
# GeoTIFF with LZW compression are supported

# GDAL's Affine Transformation (GetGeoTransform) 
# https://gdal.org/tutorials/geotransforms_tut.html
# GetGeoTransform translates latitude, longitude to pixel indices
# GT[0] and GT[3] define the "origin": upper left pixel 
# without rotation, GT[2] and GT[4] are zero

# remove newlines and blanks in the coordinates array, for better readibility of the GeoJSON pretty print
def pretty_dumps(obj, **kwargs):
    def compact_coordinates(match):
        # Remove newlines and extra spaces within the coordinates array
        return match.group(0).replace('\n', '').replace(' ', '')
    json_str = json.dumps(obj, **kwargs)
    # Use a more robust regex to match coordinate arrays
    json_str = re.sub(r'\[\s*([^\[\]]+?)\s*\]', compact_coordinates, json_str)
    return json_str

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

def extract_elevation(tiff_file, lat, lon):
    gdal.UseExceptions()
    try:
        data = gdal.Open(tiff_file)
        if data is None:
            print(f"Failed to open file: {tiff_file}")
            return 0        
        band1 = data.GetRasterBand(1)
        GT = data.GetGeoTransform()
        x_pixel_size = GT[1]
        y_pixel_size = GT[5]
        xP = int((lon - GT[0]) / x_pixel_size)
        yL = int((lat - GT[3]) / y_pixel_size)
        array_result = band1.ReadAsArray(xP, yL, 1, 1)
        single_element = array_result[0, 0]
        integer_value = int(single_element)
        return integer_value    # return elevation found in GeoTIFF tile
    except Exception as e:
        print(f"Error extracting altitude: {e}")
        return 0

def add_elevation(coords):
    new_coords = []
    for coord in coords:
        longitude, latitude = coord[0], coord[1]
        tiff_name = '../geotiff/' + find_tiff(latitude, longitude)
        elev = extract_elevation(tiff_name, latitude, longitude)
        new_coords.append([longitude, latitude, elev])
    return new_coords

def process_geometry(geom):  #recursive function to manipulate geometry objects
    if geom['type'] == 'GeometryCollection':    
        processed_member = []
        for member in geom['geometries']:             
            processed_member.append(process_geometry(member))   #recursive call to handle each geom object in collection
        return GeometryCollection(processed_member)
    else:
        coords = geom.get('coordinates')
        if coords is not None:
            if geom['type'] == 'Point':  # Point is a special simple case
                longitude, latitude = coords[0], coords[1]
                tiff_name = '../geotiff/' + find_tiff(latitude, longitude)
                point_elev = extract_elevation(tiff_name, latitude, longitude)
                return Point((longitude, latitude, point_elev))
            elif geom['type'] == 'LineString':
                new_coords = add_elevation(coords)
                return LineString(new_coords)
            elif geom['type'] == 'Polygon':
                new_coords = [add_elevation(ring) for ring in coords]
                return Polygon(new_coords)
            elif geom['type'] == 'MultiPoint':
                new_coords = add_elevation(coords)
                return MultiPoint(new_coords)
            elif geom['type'] == 'MultiLineString':
                new_coords = [add_elevation(line) for line in coords]
                return MultiLineString(new_coords)
            elif geom['type'] == 'MultiPolygon':
                new_coords = [[add_elevation(ring) for ring in polygon] for polygon in coords]
                return MultiPolygon(new_coords)
        return None

try:
    with open(sys.argv[1] + '.geojson', 'r', encoding='utf-8') as infile:
        data = json.load(infile)
except FileNotFoundError:
    print("file not found")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Failed to parse GeoJSON file.")
    sys.exit(1)  

bucket = []

for feature in data['features']:
    geom = feature['geometry']
    processed_geom = process_geometry(geom)
    if processed_geom is not None:
        new_feature = Feature(geometry=processed_geom, properties=feature['properties'])
        bucket.append(new_feature)

new_string = pretty_dumps(FeatureCollection(bucket), indent=2, ensure_ascii=False)

with open(sys.argv[1] + '.geojson', 'w') as outfile:
    outfile.write(new_string)
print ( f"File saved as {sys.argv[1]+'.geojson'}")