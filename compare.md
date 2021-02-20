Comparision of different SRTM data files from various sources:


| Source | SRTM Traditional  | USGS EarthExplorer | ASTER (NASA) | ALOS (AW3D30) | OpenTopography | CGIAR-CSI |
| ----  |:-----:|:-----:|:------:|:-------:|:------:|:----:|
| File type  |  HGT  |  GeoTIFF / DTED  | GeoTIFF | GeoTIFF | GeoTIFF | GeoTIFF |
| Tile area | 1&deg; x 1&deg; |1&deg; x 1&deg; | 1&deg; x 1&deg; | 1&deg; x 1&deg; | any | 5&deg; x 5&deg; |
| Resolution | 30 m | 30 m | 30 m | 30 m | 90 m | 90 m |
| Embedded Metadata | no | yes | yes | yes | yes | yes |
| Pixel Dimension (Aspect Ratio) | 3601x3601 | 3601x3601 | 3601x3601 | 3600x3600 | any | 6000x6000 |
| 1 pixel Oversize (1 pixel Overlap) | yes | yes | yes | no |  | no |
| Area or Point | point | point | area | area | area | area |
| no data return value | -32768 | -32767 | | | 0 | -32768 |
| Compression | none | none | LZW | none | LZW | none |


* HGT files without embedded metadata is subject to other HGT files with identical file name corrupting the results. This could happen if the filename is accidentially changed.
* For files without 1 pixel overlap, the file name selection algorithm needs to be different to avoid out of range errors at the boundary. [This algorithm](/library/tilename.py) works for files with 1 pixel overlap (SRTM Traditional, USGS, NASA).
