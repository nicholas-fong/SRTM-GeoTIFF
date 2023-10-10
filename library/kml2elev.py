# Parse Google KML and add elevation extracted from GeoTIFF tiles (NASA or USGS)
# only works on linux system because it is nearly impossible to install gdal/osgeo on Windows system
import xml.etree.ElementTree as ET
import sys
import simplekml
import math
from osgeo import gdal   # sudo apt install gdal-bin

#main() is here
kml = simplekml.Kml()
# Open the KML file
with open(sys.argv[1]+".kml") as infile:
    tree = ET.parse(infile)
root = tree.getroot()
# Define namespaces (KML uses namespaces)
kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

def find_tile ( latitude, longitude ):
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

def extract_altitude (tiff_file, lat, lon):
    data = gdal.Open(tiff_file)
    band1 = data.GetRasterBand(1)
    GT = data.GetGeoTransform()
    # call gdal's Affine Transformation (GetGeoTransform method)
    # GetGeoTransform translates latitude, longitude to pixel indices
    x_pixel_size = GT[1]
    y_pixel_size = GT[5]
    xP = int((lon - GT[0]) / x_pixel_size )
    yL = int((lat - GT[3]) / y_pixel_size )
    return ( int( band1.ReadAsArray(xP,yL,1,1) ) )

def add_elevation(geometry_element):
    coordinates_elem = geometry_element.find('kml:coordinates', namespaces=kml_namespace)
    if coordinates_elem is not None:
        coordinates = coordinates_elem.text.strip().split()
        # coordinates is a long list of strings ['121,31','122,32']
        list_floats = [list(map(float, item.split(','))) for item in coordinates]
        # list_floats is a long list of float [[121, 31],[122,32]]
        coord_with_elev = []
        for item in list_floats:
            longitude=item[0]
            latitude=item[1]
            tiff_file=find_tile(latitude, longitude)
            z = extract_altitude (tiff_file,latitude,longitude)
            coord_with_elev.append([longitude,latitude,z])
        return coord_with_elev

# Iterate through Placemark elements
for placemark in root.findall('.//kml:Placemark', namespaces=kml_namespace):
    name_elem = placemark.find('kml:name', namespaces=kml_namespace)
    name = name_elem.text.strip() if name_elem is not None else 'Unnamed'

    # Check for Point, LineString, or Polygon geometry
    point = placemark.find('.//kml:Point', namespaces=kml_namespace)
    line_string = placemark.find('.//kml:LineString', namespaces=kml_namespace)
    polygon = placemark.find('.//kml:Polygon', namespaces=kml_namespace)

    if point is not None:
        mypoint = kml.newpoint(name=name)
        mypoint.coords = add_elevation(point)

    elif line_string is not None:
        myline = kml.newlinestring(name=name)
        myline.coords = add_elevation(line_string)

    elif polygon is not None:
        mypol = kml.newpolygon(name=name)
        outer_ring = polygon.find('.//kml:outerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        mypol.outerboundaryis = add_elevation(outer_ring) 
        # slight setback: simplekml can store only one inner ring despite multiple inner rings exist.
        #blocks = polygon.findall('.//kml:innerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        #for inner_ring in blocks:                
        #    mypol.innerboundaryis = add_elevation(inner_ring)

print(kml.kml())
kml.save(sys.argv[1]+".kml")

