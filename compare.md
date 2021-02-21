Comparision of different SRTM data files from various sources:


| Source | NASA ASTER  | USGS EarthExplorer | NASA ASTER | ALOS (AW3D30) | OpenTopography | CGIAR-CSI |
| ----  |:-----:|:-----:|:------:|:-------:|:------:|:----:|
| File type  | GeoTIFF  |  GeoTIFF or DTED  | HGT * | GeoTIFF | GeoTIFF | GeoTIFF |
| Tile area | 1&deg; x 1&deg; |1&deg; x 1&deg; | 1&deg; x 1&deg; | 1&deg; x 1&deg; | see note | 5&deg; x 5&deg; |
| Resolution | 30 m | 30 m | 30 m | 30 m | 90 m | 90 m |
| Embedded Metadata | yes | yes | no * | yes | yes | yes |
| Pixel Dimension (Aspect Ratio) | 3601x3601 | 3601x3601 | 3601x3601 | 3600x3600 | see note | 6000x6000 |
| 1 pixel Oversize (1 pixel Overlap) | yes | yes | yes |  |  see note|  |
| Area or Point | area | point | point | area | area | area |
| no data return value |  | -32767 | -32768 |   |  | -32768 |
| Compression | LZW | none | none | none | LZW | none |


* HGT files without embedded metadata is vulnerable to data corruption by other HGT files with same file name.
* [This algorithm](/library/tilename.py) works for selecting tiles with overlapping pixel (e.g. NASA, USGS).
* [Alternate algorithm](/library/tile_alos.py) is needed for selecting tiles with non-overlaping pixel (e.g. ALOS). It has not been stress tested.
* My preference is NASA ASTER because it has LZW compression and it returns Area data instead of Pixel data.
* For "tough area" such as Himalayas, ALOS produces excellent accuracy and no voids.
* OpenTopography extracts data from ALOS AW3D30, SRTM 1 arc-second or 3 arc-seconds and assembles them to an arbitrary tile area specified by you.
