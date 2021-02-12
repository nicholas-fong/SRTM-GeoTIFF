# SRTM-GeoTIFF
Python function to read SRTM elevation from a GeoTIFF file downloaded from USGS EarthExplorer delivery system.
The USGS EarthExplorer is USGS's preferred method to download SRTM data files. Previously, SRTM tiles were in .hgt format, EarthExplorer delivery/download only allows BIL, DTED or GeoTIFF file types.
There is a learning curve to use EarthExplorer, once it is mastered, it can as useful as the defunct ftp and http download methods.
The Python function automatically adapts to different tile sizes such as 1201x1201 (3 arc), 3601 x 3601 (1 arc) and 1201x601.
The function relys on these libraries: rasterio, numpy and math.
The function determines which tile_name to use based on latitude and longitude, tries to open that file from a local directory or network directory. If the file does not exist, it throws an error. Use EarthExplorer to download the file and try again.
The EarthExplorer download file name example: n23_w113_3arc_v2.tif, _3arc can be _1arc, _v2 can be _v1 or _v3, depending on your choices and data availability. 
You can have a choice of Non-Void Filled, Void-Filled, and 1 Arc-Second Global.
For convenience, I delete trailing characters using regex 's/_.arc_v.//'  and just use n23_w113.tif

To use:
assuming (3 Arc-Second) n49_w123.tif is in the same directory as read_srtm.py
python read_srtm.py 49.68437 -122.14162
elevation is 644 meters.
Now replace n49_w123.tif with the 1 Arc-Second version,
python read_srtm.py 49.68437 -122.14162
elevation is 657 meters.
