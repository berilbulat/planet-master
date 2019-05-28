import rasterio
import numpy as np
import os
import activation


def extract ():
	# download_location = "downloads"
	download_location = "output"
	search_list = activation.request_search_list()
	print search_list
	spectral_band_for_assets = []
	for search in search_list:
		image_files = {}
		for file in os.listdir(download_location + "/" + search['item_id'] + "/"):
			print file
			if file.endswith(".tif") and "DN_udm" not in file:
		   		image_files[os.path.splitext(file)[0]] = os.path.join(download_location + "/" + search['item_id'] + "/", file)

		print image_files
		# filename = "downloads/20170623_180038_0f34_3B_AnalyticMS.tif"

		# # Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
		spectral_band = {}
		for key,filename in image_files.items():
			bands = {}
			print filename
			with rasterio.open(filename) as src:
			    band_blue_radiance = src.read(1)
			    bands["band_blue_radiance"] = band_blue_radiance
			    
			with rasterio.open(filename) as src:
			    band_green_radiance = src.read(2)
			    bands["band_green_radiance"] = band_green_radiance

			with rasterio.open(filename) as src:
			    band_red_radiance = src.read(3)
			    bands["band_red_radiance"] = band_red_radiance

			with rasterio.open(filename) as src:
			    band_nir_radiance = src.read(4)
			    bands["band_nir_radiance"] = band_nir_radiance
			spectral_band[search['item_id']] = bands

		spectral_band_for_assets.append(spectral_band)
	print spectral_band_for_assets
	return spectral_band_for_assets

def input_raster_file ( filename ):
	# download_location = "downloads"
	download_location = "output"
	with rasterio.open(download_location + "/" + filename + "_3B_AnalyticMS_clip.tif") as src:
		return src
