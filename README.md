## SRTM-GeoTIFF
A simple yet powerful Python module to read elevation from raster-based SRTM files from a variety of data sources:<br>
USGS EarthExplorer, CGIAR-CSI, NASA ASTER GDEM, OpenTopography (UCSD), GMTED2010<br>
File types supported: GeoTIFF, DTED, HGT, BIL<br>
Data types supported: raster-based files with virtually no restrictions on geometry, resolutions and lat/lon boundary.<br>
The module calls gdal's GetGeoTransform (an Affine Transformation) to correctly translates latitude, longitude to pixel indices in the raster.

The more challenging task is to find which tile/filename to use for a particular lat/lon point, especially each data source uses their own file naming convention.
For personal use, I prefer EarthExplorer's GeoTIFF because the file naming convention is very similar to .hgt and is easily parsed. This naming convention however is restriced to 1&deg; x 1&deg; tiles. CGIAR-CSI publishes 5&deg; x 5&deg; tiles.

Use EarthExplorer [helper](/EarthExplorer-howto.md) to manually select and download GeoTIFF or DTED files.

## Example:
```
>>>import srtm1
>>>srtm1.read( './n22_e114.tif', 22.4101, 114.1246 )
945  (Hong Kong, China)
>>>srtm1.read( './n49_w123.tif', 49.68437, -122.14162 )
644  (British Columbia, Canada)
>>>srtm1.read( './s33_w071.tif', -32.653197, -70.0112 )
6929 (Aconcagua, Argentina)
>>>srtm1.read( './s36_e149.tif', -35.2745, 149.09752 )
810  (Canberra, Australia)
```
Find which tile to use:
```
>>>import tilename
>>>tilename.find( 49.6, -122.1 )
>>>'n49_w123.tif'
>>>
```
