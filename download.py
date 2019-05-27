from demo_filters import environment
import activation
import json
import requests

def request_download_status(search_list):
	# request an item
	session = activation.setup_auth()

	for search_item in search_list:
		try:
			item = \
			  session.get(
			    (environment["ACTIVATION_ENDPOINT"] +
			    "{}/items/{}/assets/").format(search_item["item_type"], search_item["item_id"]))

			#print item.json()["visual"]["status"]
			#print item.json()
			#search_item["status"] = item.json()["visual"]["status"]

			#4-band
			print item.json()[search_item["asset_type"]]["status"]
			search_item["status"] = item.json()[search_item["asset_type"]]["status"]
		except Exception as e:
			print e.message
			continue

def request_download_location(search_list):
	# request an item
	session = activation.setup_auth()

	download_urls = []
	for search_item in search_list:
		try:
			if search_item["status"] == 'active':
				download_url = {}
				item = \
				  session.get(
				    (environment["ACTIVATION_ENDPOINT"] +
				    "{}/items/{}/assets/").format(search_item["item_type"], search_item["item_id"]))
				
				#print item.json()["visual"]["location"]
				#print item.json()
				#download_url[search_item["item_id"]] = item.json()["visual"]["location"]

				#4-band location
				print item.json()[search_item["asset_type"]]["location"]
			
				download_url[search_item["item_id"]] = item.json()[search_item["asset_type"]]["location"]
				download_urls.append(download_url)
			else:
				print "NOT READY YET!"
		except Exception as e:
			print e.message
			continue
	return download_urls

def download_image(download_urls, asset_type):
	requests = activation.setup_auth()
	for download_url in download_urls:
		for key, value in download_url.items():
			with requests.get(value, stream=True) as r:
				r.raise_for_status()
				if asset_type == "analytic_xml":
					file = ".xml"
				else: 
					file = ".tif"
				with open("downloads/" + key + file, 'wb') as f:
					for chunk in r.iter_content(chunk_size=8192): 
						if chunk: # filter out keep-alive new chunks
							f.write(chunk)
							#f.flush()
activation.activate()
search_list = activation.request_search_list()
request_download_status(search_list)
download_urls = request_download_location(search_list)
print(download_urls)
download_image(download_urls, "analytic")

# search_list = activation.request_search_list()
# print search_list

# #TEST DOWNLOAD
# download_urls = []
# download_url = {}
# download_url["thumb3"] = "https://tiles.planet.com/data/v1/item-types/PSScene4Band/items/20190127_180134_0f22/thumb"
# download_urls.append(download_url)
# download_image(download_urls)

