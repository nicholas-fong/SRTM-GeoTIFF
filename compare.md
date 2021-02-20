Comparision of different SRTM data files from various sources:


| Source | NASA ASTER  | USGS EarthExplorer | NASA ASTER | ALOS (AW3D30) | OpenTopography | CGIAR-CSI |
| ----  |:-----:|:-----:|:------:|:-------:|:------:|:----:|
| File type  | GeoTIFF  |  GeoTIFF or DTED  | HGT * | GeoTIFF | GeoTIFF | GeoTIFF |
| Tile area | 1&deg; x 1&deg; |1&deg; x 1&deg; | 1&deg; x 1&deg; | 1&deg; x 1&deg; | any | 5&deg; x 5&deg; |
| Resolution | 30 m | 30 m | 30 m | 30 m | 90 m | 90 m |
| Embedded Metadata | yes | yes | no * | yes | yes | yes |
| Pixel Dimension (Aspect Ratio) | 3601x3601 | 3601x3601 | 3601x3601 | 3600x3600 | any | 6000x6000 |
| 1 pixel Oversize (1 pixel Overlap) | yes | yes | yes | no |  | no |
| Area or Point | area | point | point | area | area | area |
| no data return value |  | -32767 | -32768 | | 0 | -32768 |
| Compression | LZW | none | none | none | LZW | none |


* HGT files without embedded metadata is vulnerable to data corruption by other HGT files with same file name.
* For square files without pixel overlap (ALOS, CGIAR), a file name selection algorithm needs to be developed to handle "out of range error" at the edges. 
* [This algorithm](/library/tilename.py) works well for square tiles with 1 pixel overlap (ASTER GeoTIFF, USGS GeoTIFF or USGS DTED).
* My preference is NASA ASTER because it has LZW compression and it returns Area data instead of Pixel data.
* For "tough area" such as Himalayas, ALOS produces the best results (best accuracy and no voids).
