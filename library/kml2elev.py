from lxml import etree as ET
import xml.dom.minidom as minidom
import sys
import math
from osgeo import gdal

# add elevation data to KML
# all required GeoTiff files are assumed to be stored on local drive and in ../geotiff/ relative to this python code
# Linux: sudo apt install gdal-bin   
# Windows: install miniconda
#   conda install conda-forge::gdal   open anacoda command prompt  cd to python source files

# GDAL's Affine Transformation (GetGeoTransform) 
# https://gdal.org/tutorials/geotransforms_tut.html
# GetGeoTransform translates latitude, longitude to pixel indices
# GT[0] and GT[3] define the "origin": upper left pixel 
# without rotation, GT[2] and GT[4] are zero

# Open the KML file with error checking
try:
    with open(sys.argv[1] + ".kml") as infile:
        tree = ET.parse(infile)
    root = tree.getroot()
except FileNotFoundError:
    print(f"Error: File {sys.argv[1]}.kml not found.")
    sys.exit(1)
except ET.ParseError:
    print("Error: Failed to parse the KML file.")
    sys.exit(1)

# Define namespaces 
kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

def find_tile(latitude, longitude):
    if latitude >= 0.0 and longitude >= 0.0:
        hemi, meri = "N", "E"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.floor(longitude):03d}"
    elif latitude >= 0.0 and longitude < 0.0:
        hemi, meri = "N", "W"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif latitude < 0.0 and longitude < 0.0:
        hemi, meri = "S", "W"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif latitude < 0.0 and longitude >= 0.0:
        hemi, meri = "S", "E"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.floor(longitude):03d}"
    return f"../geotiff/{hemi}{t1}{meri}{t2}.tif"

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
        return integer_value
    except Exception as e:
        print(f"Error extracting altitude: {e}")
        return 0

def add_elevation(geometry_element):
    coordinates_elem = geometry_element.find('kml:coordinates', namespaces=kml_namespace)
    if coordinates_elem is not None:
        coordinates = coordinates_elem.text.strip().split()
        list_floats = [list(map(float, item.split(','))) for item in coordinates]
        coord_with_elev = []
        for item in list_floats:
            longitude = item[0]
            latitude = item[1]
            tiff_file = find_tile(latitude, longitude)
            z = extract_elevation(tiff_file, latitude, longitude)
            coord_with_elev.append([longitude, latitude, z])
        coordinates_elem.text = ' '.join([','.join(map(str, coord)) for coord in coord_with_elev])

# style 1 of pretty print, eliminat blank lines, returns string
def prettify(element):
    rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_string)
    pretty_string = (reparsed.toprettyxml(indent="  ", encoding='utf-8')).decode('utf-8')
    # Remove extra blank lines
    lines = [line for line in pretty_string.split('\n') if line.strip()]
    return '\n'.join(lines)
# style 2 of pretty print: ET.tosring --> minidom --> toprettyxml, returns binary string
# def prettify(element):
#   rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
#   reparsed = minidom.parseString(rough_string)
#   return reparsed.toprettyxml(indent="  ", encoding='utf-8')
# style 3 KML to string pretty print
# print( ET.tostring(kml, encoding='utf-8', pretty_print=True, xml_declaration=True ).decode() )

# main()
# Iterate through Placemark elements
for placemark in root.findall('.//kml:Placemark', namespaces=kml_namespace):
    name_elem = placemark.find('kml:name', namespaces=kml_namespace)
    name = name_elem.text.strip() if name_elem is not None else 'Unnamed'

    point = placemark.find('.kml:Point', namespaces=kml_namespace)
    line_string = placemark.find('.kml:LineString', namespaces=kml_namespace)
    polygon = placemark.find('.kml:Polygon', namespaces=kml_namespace)
    multigeometry = placemark.find('.kml:MultiGeometry', kml_namespace)

    if point is not None:
        add_elevation(point)

    elif line_string is not None:
        add_elevation(line_string)

    elif polygon is not None:
        outer_ring = polygon.find('.kml:outerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        add_elevation(outer_ring)
        inner_rings = polygon.findall('.kml:innerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        for inner_ring in inner_rings:
            add_elevation(inner_ring)

    elif multigeometry is not None:
        points = multigeometry.findall('.kml:Point', kml_namespace)
        lines = multigeometry.findall('.kml:LineString', kml_namespace)
        polygons = multigeometry.findall('.kml:Polygon', kml_namespace)
        for point in points:
            add_elevation(point)
        for line in lines:
            add_elevation(line)    
        for polygon in polygons:
            outer_ring = polygon.find('.kml:outerBoundaryIs/kml:LinearRing', kml_namespace)
            add_elevation(outer_ring)
            inner_rings = polygon.findall('.kml:innerBoundaryIs/kml:LinearRing', kml_namespace)
            for hole in inner_rings:
                add_elevation(hole)

# sylte 1 output: <?xml version="1.0" encoding="utf-8"?>
pretty_kml = prettify(root)
#print (pretty_kml)
with open(sys.argv[1]+'.kml', 'w') as output_file:
    output_file.write(pretty_kml)
print ( f"File with elevation saved as {sys.argv[1]+'.kml'}")        
# style 2 output: <?xml version='1.0' encoding='UTF-8'?>
# super simple, but uses '' instead of ""
# tree.write(sys.argv[1] + ".kml", encoding="utf-8", xml_declaration=True)
