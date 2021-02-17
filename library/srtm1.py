from osgeo import gdal

def read(my_file, lat, lon):
    data = gdal.Open(my_file)
    band1 = data.GetRasterBand(1)
    GT = data.GetGeoTransform()
    # call gdal's Affine Transformation (GetGeoTransform method)
    # GetGeoTransform translates latitude, longitude to pixel indices
    x_pixel_size = GT[1]
    y_pixel_size = GT[5]
    xP = int((lon - GT[0]) / x_pixel_size )
    yL = int((lat - GT[3]) / y_pixel_size )
    return ( int( band1.ReadAsArray(xP,yL,1,1) ) )

# gda; Affine GetGeoTransform interprets different file formats, tile sizes and resolutions
# File formats supported: GeoTIFF, DTED, HGT, BIL
# Data sources: USGS EarthExplorer, CGIAR-CSI, NASA ASTER GDEM, OpenTopography, GMTED2010

