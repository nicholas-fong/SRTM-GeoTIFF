# append elevation data to gpx waypoints, route points and track points.
# GeoTiff files are assumed to be stored on local drive and in ../geotiff/ relative to this python code
# Linux: sudo apt install gdal-bin   Windows: install miniconda environment.

import sys
import gpxpy
import math
from osgeo import gdal

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
    return( f"../geotiff/{hemi}{t1}{meri}{t2}.tif" ) 

def extract (tiff_file, lat, lon):
    gdal.UseExceptions()
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
    array_result = band1.ReadAsArray(xP, yL, 1, 1)
    single_element = array_result[0, 0]  # Extract a single element
    integer_value = int(single_element)  # Convert to an integer
    return (integer_value)
            
# read a gpx file and append elevation tags to waypoints, route points and track points

with open( sys.argv[1]+'.gpx', 'r') as infile:
    gpx = gpxpy.parse(infile)
infile.close()

for p in gpx.waypoints:
    tiff_file=find(p.latitude, p.longitude)
    z = extract (tiff_file,p.latitude,p.longitude)
    p.elevation = z

for routes in gpx.routes:
    for p in routes.points:
        tiff_file=find(p.latitude, p.longitude)
        z = extract (tiff_file,p.latitude,p.longitude)
        p.elevation = z

for track in gpx.tracks: 
    for segment in track.segments:
        for p in segment.points:
            tiff_file=find(p.latitude, p.longitude)
            z = extract (tiff_file,p.latitude,p.longitude)
            p.elevation = z

#print (gpx.to_xml())
with open(sys.argv[1]+'.gpx', 'w') as file:
    file.write( gpx.to_xml() )
file.close()

    