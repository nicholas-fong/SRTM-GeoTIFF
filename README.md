# SRTM-GeoTIFF
A simple Python function to read SRTM elevation from a GeoTIFF file downloaded from USGS EarthExplorer delivery system.
The USGS EarthExplorer is USGS's preferred method to download SRTM data files. Previously, SRTM tiles were available in .hgt format, but the new EarthExplorer delivery/download only allows BIL, DTED or GeoTIFF file types.<br>
There is a learning curve to use EarthExplorer, once it is mastered, it can as useful as the defunct ftp or http delivery methods, except slower.<br><br>
This Python function automatically adapts to different tile sizes such as 1201x1201 (3 arc), 3601x3601 (1 arc). It also understands 1201x601 (1201-high,601-wide) for tiles above 50° north and below 50° south. These areas are sampled at a resolution of 2 arc-second by 1 arc-second. This function determines which tile_name to use based on latitude and longitude, tries to open that file from a local directory. If the file does not exist, it throws an error. Use EarthExplorer [helper](https://github.com/nicholas-fong/SRTM-GeoTIFF/blob/main/EarthExplorer-howto.md) to download the correct file and try again.

EarthExplorer downloaded file name example: n23_w123_3arc_v2.tif<br>
_3arc is sampled at 3 arc-seconds (approximately 90 meters)<br>
_1arc is sampled at 1 arc-seconds (approximately 30 meters)<br>
_v1 _v2 _v3 = Non-Void Filled, Void-Filled, 1 arc-second void-filled Global<br>

For simplicity and convenience, I delete some characters using regular expression **'s/_.arc_v.//'**  and simply use something like n23_w123.tif

# Examples:
```
$python read_srtm.py 49.68437 -122.14162
(assuming a 3 arc-seconds n49_w123.tif is already in the current working directory)
elevation is 644 meters.

(Next download from EarthExplorer a 1 arc-second version of n49_w123.tif)
$python read_srtm.py 49.68437 -122.14162
elevation is 657 meters.

$python read_srtm.py 31.5485 35.4675
GeoTIFF tile: n31_e035.tif
elevation is -415 meters (Dead Sea)

$python read_srtm.py -32.653197 -70.0112
GeoTIFF tile used: s33_w071.tif
elevation 6930 meters (Aconcagua, Argentina)

```
The return value of this simple python function is exatcly the same as **gdallocationinfo** for test points in all four quadrants. You can use this function as a stand alone query tool, or incorporate it in other applications such as [gpx-add-SRTM-elevation](https://github.com/nicholas-fong/gpx-add-SRTM-elevation)
