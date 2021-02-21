## SRTM-GeoTIFF
A simple and versatile Python module to read elevation data from raster-based SRTM files from data sources such as:

`NASA ASTER GDEM` `USGS EarthExplorer` `ALOS World 3D` `OpenTopography` `CGIAR-CSI`

File types supported: `GeoTIFF`, `DTED`, `HGT`, `BIL`

Data type supported: raster files with few restrictions on pixel dimensions or aspect ratios. These file structures are handled automatically: NASA's ASTER GDEM 1&deg; x 1&deg; 3601x3601. ALOS 1&deg; x 1&deg; 3600x3600. CGIAR-CSI 5&deg; x 5&deg; 6000x6000. USGS 1&deg; x 1&deg; 3601x3601, 1801x3601 and 3&deg; x 3&deg; 1201x1201, 601x1201. This module makes use of GDAL's GetGeoTransform (Affine Transformation) to translate latitude, longitude into pixel indices. It also handles LZW compressed rasters automagically.

The more challenging task is perhaps to find which tile/filename to use for a particular lat/lon location, especially when each data source uses their own file naming convention. For personal hobby use, I use NASA's ASTER GDEM `GeoTIFF` since the file [naming convention](/library/tilename.py) (with some regex manipulations) is almost exactly the same style as the original SRTM .hgt. For ALOS's 3600x3600 non-overlapping tiles, a modified algorithm [tile_alos.py](/library/tile_alos.py) is used to parse latitude and longitude to the correct filename.

[ASTER GDEM](https://search.earthdata.nasa.gov/search/) user interface is farily straight forward. For new users to EarthExplorer, this [primer](/EarthExplorer.md) may be helpful. 

### Example:
```
>>>import srtm1
>>>srtm1.read( './N46E008.tif', 46.854539, 8.49701)
2698 (Lucern, Switzerland)
>>>srtm1.read( './nN49W123.tif', 49.68437, -122.14162 )
644  (British Columbia, Canada)
>>>srtm1.read( './S33W071.tif', -32.653197, -70.0112 )
6929 (Aconcagua, Argentina)
>>>srtm1.read( './S36E149.tif', -35.2745, 149.09752 )
810  (Canberra, Australia)
```
### Determine which tile to use:

For NASA and USGS 1 pixel overlapping tiles:
```
>>> import tilename
>>> tilename.find( 49.6, -122.1 )
>>> 'N49W123.tif'
>>> tilename.find( 49, -122.1 )
>>> 'N49W123.tif'
```
For ALOS non-overlapping tiles:
```
>>> import tile_alos
>>> tile_alos.find ( 49.6, -122.1 )
>>> 'N49W123.tif'
>>> tile_alos.find ( 49, -122.1 )
>>> 'N48W123.tif' 
```
Subtle difference, but critical to avoid out of bound errors in batch processing.
