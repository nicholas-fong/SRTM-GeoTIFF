Comparision of different SRTM data files from various sources:


| Source | SRTM Traditional  | USGS EarthExplorer | ASTER (NASA) | ALOS (AW3D30) | OpenTopography | CGIAR |
| ----  |:-----:|:-----:|:------:|:-------:|:------:|:----:|
| File type  |  HGT  |  GeoTIFF or DTED  | GeoTIFF | GeoTIFF | GeoTIFF | GeoTIFF |
| Tile area | 1&deg; x 1&deg; |1&deg; x 1&deg; | 1&deg; x 1&deg; | 1&deg; x 1&deg; | any | 5&deg; x 5&deg; |
| Resolution | 30 m | 30 m | 30 m | 30 m | 90 m | 90 m |
| Embedded Metadata | no | yes | yes | yes | yes | yes |
| Pixel Dimension | 3601x3601 | 3601x3601 | 3601x3601 | 3600x3600 | any | 6000x6000 |
| Aspect Ratio | square | square | square | square | any | square |
| 1 pixel Oversize | yes | yes | yes | no |  | no |
| Area or Point | point | point | area | area | area | area |
| no data returns | -32768 | -32767 | | | 0 |  |
| Compression | none | none | LZW | none | LZW |  |


* HGT files without embedded metadata is subject to other HGT files with identical file name corrupting the results. This could happen if the filename is accidentially changed.
