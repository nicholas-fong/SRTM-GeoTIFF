# add elevation data to KML file
# all required GeoTiff files are assumed to be stored on local drive and in ../geotiff/ relative to this python code
# Linux: sudo apt install gdal-bin   
# Windows: install miniconda
#   conda install conda-forge::gdal

import xml.etree.ElementTree as ET
import sys
import math
from osgeo import gdal

# Function to strip namespaces
def strip_ns_prefix(elem):
    for subelem in elem.iter():
        subelem.tag = subelem.tag.split('}', 1)[1] if '}' in subelem.tag else subelem.tag
    return elem

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

# Strip namespaces from the tags
root = strip_ns_prefix(root)

# Define namespaces (KML uses namespaces)
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

def extract_altitude(tiff_file, lat, lon):
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
    coordinates_elem = geometry_element.find('coordinates')
    if coordinates_elem is not None:
        coordinates = coordinates_elem.text.strip().split()
        list_floats = [list(map(float, item.split(','))) for item in coordinates]
        coord_with_elev = []
        for item in list_floats:
            longitude = item[0]
            latitude = item[1]
            tiff_file = find_tile(latitude, longitude)
            z = extract_altitude(tiff_file, latitude, longitude)
            coord_with_elev.append([longitude, latitude, z])
        coordinates_elem.text = ' '.join([','.join(map(str, coord)) for coord in coord_with_elev])

def process_multigeometry(multigeometry):
    for child in multigeometry:
        if child.tag.endswith('Polygon'):
            name_elem = child.find('name')
            name = name_elem.text if name_elem is not None else 'Unnamed'
            outer_ring = child.find('.//outerBoundaryIs/LinearRing')
            add_elevation(outer_ring)
            inner_rings = child.findall('.//innerBoundaryIs/LinearRing')
            for inner_ring in inner_rings:
                add_elevation(inner_ring)
        elif child.tag.endswith('LineString'):
            name_elem = child.find('name')
            name = name_elem.text if name_elem is not None else 'Unnamed'
            add_elevation(child)
        elif child.tag.endswith('Point'):
            name_elem = child.find('name')
            name = name_elem.text if name_elem is not None else 'Unnamed'
            add_elevation(child)

def process_placemark(placemark):
    # Print the entire structure of the placemark for debugging
    # print(ET.tostring(placemark, encoding='unicode'))
    
    multigeometry = placemark.find('.//MultiGeometry')
    if multigeometry is not None:
        process_multigeometry(multigeometry)
    else:
        point = placemark.find('.//Point')
        line_string = placemark.find('.//LineString')
        polygon = placemark.find('.//Polygon')

        if point is not None:
            add_elevation(point)
        elif line_string is not None:
            add_elevation(line_string)
        elif polygon is not None:
            outer_ring = polygon.find('.//outerBoundaryIs/LinearRing')
            add_elevation(outer_ring)
            inner_rings = polygon.findall('.//innerBoundaryIs/LinearRing')
            for inner_ring in inner_rings:
                add_elevation(inner_ring)

# Iterate through Placemark elements
for placemark in root.findall('.//Placemark'):
    process_placemark(placemark)

# Save the modified KML
tree.write(sys.argv[1] + ".kml", encoding="utf-8", xml_declaration=True)
