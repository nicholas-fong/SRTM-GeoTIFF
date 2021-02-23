from osgeo import gdal

def read(my_file, lat, lon):
    data = gdal.Open(my_file)
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
    return ( int( band1.ReadAsArray(xP,yL,1,1) ) )

# File type supported: GeoTIFF, DTED, HGT, BIL
# Square overlapping or non-overlapping rasters supported
# Rectangular rasters supported
# GeoTIFF with LZW compression supported
