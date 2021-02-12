# SRTM-GeoTIFF
Python function to read SRTM elevation from a GeoTIFF file downloaded from USGS EarthExplorer delivery system.
The USGS EarthExplorer is USGS's preferred method to download SRTM data files. Previously, SRTM tiles were in .hgt format, new EarthExplorer delivery/download only allows BIL, DTED or GeoTIFF file types.
There is a learning curve to use EarthExplorer, once it is mastered, it can as useful as the now defunct ftp and http delivery methods.
This Python function automatically adapts to different tile sizes such as 1201x1201 (3 arc), 3601x3601 (1 arc) and 1201x601(1201-high,601-wide) for tiles above 50° north and below 50° south latitude that are sampled at a resolution of 2 arc-second by 1 arc-second.
This function relys on these libraries: rasterio, numpy and math.
The function determines which tile_name to use based on latitude and longitude, tries to open that file from a local directory or network directory. If the file does not exist, it throws an error. Use EarthExplorer [tips](https://github.com/nicholas-fong/SRTM-GeoTIFF/blob/main/comments.md) to download the correct file and try again.

EarthExplorer downloaded file name example: n23_w123_3arc_v2.tif<br>
_3arc is sampled at 3 arc-seconds (approximately 90 meters)<br>
_1arc is sampled at 1 arc-seconds ((approximately 30 meters)<br>
_v1 _v2 _v3 = Non-Void Filled, Void-Filled, 1 arc-second void-filled Global<br>

For convenience, I delete trailing characters using regex **'s/_.arc_v.//'**  and simply use something like n23_w123.tif

Example usage:
assuming (3 arc-seconds) n49_w123.tif is already in the same directory as read_srtm.py

python read_srtm.py 49.68437 -122.14162

elevation is 644 meters.

Next download from EarthExplorer the 1 arc-second version of n49_w123.tif,

python read_srtm.py 49.68437 -122.14162

elevation is 657 meters.

The elevation points of this python function are exatcly the same as gdallocationinfo for test points in four quadrants. You can use this function as a stand alone one point query tool, or incorporate it in other applications (e.g. appending SRTM-based elevation points to a GPS track).

See [gpx-add-SRTM-elevation](https://github.com/nicholas-fong/gpx-add-SRTM-elevation)
