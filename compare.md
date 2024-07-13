Comparision of different SRTM data files from various sources:


| Source | NASA and JSS  | USGS EarthExplorer | NASA ASTER | ALOS (AW3D30) | OpenTopography | 
| ----  |:-----:|:-----:|:------:|:-------:|:------:|
| File type  | GeoTIFF  |  GeoTIFF or DTED  | HGT * | GeoTIFF | GeoTIFF | 
| Tile area | 1&deg; x 1&deg; |1&deg; x 1&deg; | 1&deg; x 1&deg; | 1&deg; x 1&deg; | see note | 
| Resolution | 30 m | 30 m | 30 m | 30 m | 30 m or 90 m | 
| Embedded Metadata | yes | yes | no * | yes | yes | yes |
| Pixel Dimension | 3601x3601 | 3601x3601 | 3601x3601 | 3600x3600 | see note | 
| 1 pixel overlapping tiles | yes | yes | yes | non-overlap  | see note | 
| Area or Point | area | point | point | area | area | 
| no data return value |  | -32767 | -32768 |   |  | 
| Compression | LZW | none | none | none | LZW | 


* HGT files without embedded metadata is vulnerable to data corruption by other HGT files with same file name.
* [This algorithm](/library/tilename.py) works for selecting tiles with overlapping pixel (e.g. NASA, USGS).
* [Alternate algorithm](/library/tile_alos.py) is needed to select tiles with non-overlaping pixel (e.g. ALOS).
* My preference is NASA ASTER because it has LZW compression and it returns Area data instead of Pixel data.
* For "difficult area" such as the Himalayas, ALOS produces excellent accuracy and no voids.
* OpenTopography extracts data from ALOS, SRTM 1 or SRTM 3 and assembles them to an arbitrary tile area specified by you.
