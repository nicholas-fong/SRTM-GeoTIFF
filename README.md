## SRTM-GeoTIFF
Python snippets to read elevation data from raster-based SRTM files (GeoTIFF) from data sources such as:

`USGS EarthExplorer` `Japan Space Systems` `NASA ASTER GDEM`  `ALOS AW3D30` `OpenTopography`

File types supported by this snippet: Public Domain- `GeoTIFF`, Military- `DTED`, ESRI- `BIL` and legacy- `HGT`

Data type supported by this snippet: raster files with few restrictions on pixel dimensions or aspect ratios. It can handle file types like: NASA/JSS ASTER GDEM 3601x3601. ALOS AW3D30 3600x3600. USGS 3601x3601, 1801x3601, 1201x1201 and 601x1201.

Snippet makes use of GDAL's [GetGeoTransform](https://gdal.org/tutorials/geotransforms_tut.html) (Affine Transformation) to translate the given latitude, longitude into pixel indices. It also handles LZW compressed rasters automagically.

The more challenging task is perhaps to find out which tile/filename to use for a particular lat/lon location, especially when each data source uses their own file naming convention. For personal hobby use, I use `GeoTIFF` tiles because the [file naming convention](/library/whichtile.py) (with small additional regex manipulations) is very similar to the original SRTM .hgt files. For ALOS's 3600x3600 non-overlapping tiles, a modified algorithm [tile_alos.py](/library/tile_alos.py) is necessary to parse given latitude and longitude to select the correct filename.

Sources of ASTER GDEM (Global Digital Elevation Model) in GeoTIFF format are:<br>
ASTER = Advanced Spaceborne Thermal Emission and Reflection Radiometry.

[NASA's Earth Data](https://search.earthdata.nasa.gov/search/) 

[USGS EarthExplorer](https://earthexplorer.usgs.gov/). Here is a [primer](/EarthExplorer.md) on how to download GeoTIFF from USGS EarthExplorer.

[Japan Space Systems ASTER GDEM](https://gdemdl.aster.jspacesystems.or.jp/index_en.html).

### Snippet to determine which GeoTIFF tile(s) to use:

For NASA and USGS (1-pixel overlapping tiles):
```
$python3 whichtile.py
```

For ALOS (non-overlapping tiles):<br>
In words, if the latitude is exactly an integer, then use 1 tile further south compared to NASA's/USGS's counterpart.
```
$python3 whichalos.py
```

### older snippet to determine which GeoTIFF tile to use:

For NASA and USGS (1-pixel overlapping tiles):
```
>>> import tilename
>>> tilename.find( 49.6, -122.1 )
>>> 'N49W123.tif'
>>> tilename.find( 49.0, -122.1 )
>>> 'N49W123.tif'
```
For ALOS (non-overlapping tiles):
In words, if the latitude is exactly an integer, then use 1 tile further south compared to NASA's/USGS's counterpart.
```
>>> import tile_alos
>>> tile_alos.find ( 49.6, -122.1 )
>>> 'N49W123.tif'
>>> tile_alos.find ( 49.0, -122.1 )
>>> 'N48W123.tif'
```
Subtle difference, but critical to avoid index out of range errors when latitude is an integer.

### Adding elelvation to GeoJSON file
Reads a geojson file and determines which GeoTIFF tiles to use (on local drive), reads it and finds the elevation, updates or adds elevation to GeoJSON Point, LineString and Polygon geometry.
(Grouse Grind is a popular hiking trail in Vancouver, Canada)
```
$python3 geo2elev.py grouse-grind
```
### Adding elevation to gpx file
Reads a gpx file and determines which GeoTIFF tiles to use (on local drive), reads it and finds the elevation, updates or adds elevation to gpx waypoints, routes and tracks.
(Grouse Grind is a popular hiking trail in Vancouver, Canada)
```
$Python3 gpx-add-elevation.py grouse-grind
```
### manually find the elevation of a single geolocation:

Using Python 3.10.6 and GDAL 3.4.3; 
Windows Subsystem Linux (Ubuntu 22.04)
```
>>>import srtm1
>>>srtm1.read( './N46E008.tif', 46.854539, 8.49701)
2691 (Lucern, Switzerland)
>>>srtm1.read( './N49W123.tif', 49.68437, -122.14162 )
618  (British Columbia, Canada)
>>>srtm1.read( './S33W071.tif', -32.653197, -70.0112 )
6926 (Aconcagua, Argentina)
>>>srtm1.read( './S36E149.tif', -35.2745, 149.09752 )
801  (Canberra, Australia)
```
