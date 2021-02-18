## SRTM-GeoTIFF
A simple yet powerful Python module to read elevation from raster-based SRTM files from a variety of data sources such as:<br>
USGS EarthExplorer, CGIAR-CSI, NASA ASTER GDEM, OpenTopography (UCSD), USGS GMTED2010 (wide area)

File types supported: GeoTIFF, DTED, HGT, BIL

Data types supported: raster-based files with virtually no restrictions on pixel dimensions or aspect ratio, plus there is no need to align a corner pixel to the intersection of integer latitude and integer longitude.

This module calls GDAL's GetGeoTransform (Affine Transformation) to correctly translate latitude, longitude into pixel indices to access the raster.

The more challenging task is perhaps to find which tile/filename to use for a particular lat/lon point, especially each data source uses their own file naming convention.
For personal use, I prefer EarthExplorer's `GeoTIFF` because the file naming convention is very similar to .hgt and is easily parsed (see tilename.py) and pass the filename to the srtm1 module. This naming convention however is designed for 1&deg; x 1&deg; tiles. Data sources such as ALOS and CGIAR-CSI publishes 5&deg; x 5&deg; tiles which require other arrangements.

If you are new to EarthExplorer, you may find this [primer](/EarthExplorer.md) helpful to interactively select and download GeoTIFF files.

### Example:
```
>>>import srtm1
>>>srtm1.read( './n46_e008.tif', 46.854539, 8.49701)
2698 (Lucern, Switzerland)
>>>srtm1.read( './n49_w123.tif', 49.68437, -122.14162 )
644  (British Columbia, Canada)
>>>srtm1.read( './s33_w071.tif', -32.653197, -70.0112 )
6929 (Aconcagua, Argentina)
>>>srtm1.read( './s36_e149.tif', -35.2745, 149.09752 )
810  (Canberra, Australia)
```
Find out which tile to use:
```
>>>import tilename
>>>tilename.find( 49.6, -122.1 )
>>>'n49_w123.tif'
```
