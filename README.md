## SRTM-GeoTIFF
A simple yet versatile Python module to read elevation from raster-based SRTM files from a variety of data sources such as:

USGS EarthExplorer, CGIAR-CSI, NASA ASTER GDEM, OpenTopography, ALOS World 3D, etc.

File types supported: `GeoTIFF`, `DTED`, `HGT`, `BIL`

Data type supported: raster files with virtually few restrictions on pixel dimensions or aspect ratio, there is no need to align a corner pixel to the intersection of integer latitude and integer longitude. ASTER GDEM 1&deg; x 1&deg; tiles 3601x3601. CGIAR-CSI 5&deg; x 5&deg; tiles 6000x6000. ALOS 1&deg; x 1&deg; tiles 3600x3600. EarthExplorer 1&deg; x 1&deg; tiles are 3601x3601, 1801x3601, 1201x1201, 601x1201. This module handles all comfortably because GDAL's GetGeoTransform (Affine Transformation) transforms latitude, longitude into pixel indices. It also handles LZW compressed raster automagically.

The more challenging task is perhaps to find which tile/filename to use for a particular lat/lon location, especially when each data source uses their own file naming convention. For personal use, I use EarthExplorer's `GeoTIFF` because the file naming convention is similar to .hgt and is easily parsed (see tilename.py). This naming convention however is designed for 1&deg; x 1&deg; tiles. Data files that has other tile-size and file naming convention require additional attention.

For new users to EarthExplorer, this [primer](/EarthExplorer.md) may be helpful to interactively select and download GeoTIFF files.

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
Find out which 1&deg; x 1&deg; tile to use:
```
>>>import tilename
>>>tilename.find( 49.6, -122.1 )
>>>'n49_w123.tif'
```
