import os
import requests
import search_endpoint
from demo_filters import environment
import json


def parse_search_json(search_results):
	search_list = []
	try:
		search_obj = json.loads(search_results)
		for feature in search_obj["features"]:
			search_feature = {}
			search_feature["item_id"] = feature["id"]
			search_feature["item_type"] = feature["properties"]["item_type"]
			search_feature["asset_type"] = "analytic"
			search_list.append(search_feature.copy())
	except Exception as e:
		print e.message

	return search_list

# setup auth
def setup_auth():
	session = requests.Session()
	session.auth = (environment['API_KEY'], '')
	return session

def request_items(search_list):
	# request an item

	response_list = []
	try:
		session = setup_auth()

		for search_item in search_list:
			item = \
			  session.get(
			    (environment["ACTIVATION_ENDPOINT"] +
			    "{}/items/{}/assets/").format(search_item["item_type"], search_item["item_id"]))

			print ( (environment["ACTIVATION_ENDPOINT"] +
			    "{}/items/{}/assets/").format(search_item["item_type"], search_item["item_id"] ))
			# extract the activation url from the item for the desired asset
			#item_activation_url = item.json()[asset_type]["_links"]["activate"]

			item_activation_url = item.json()[search_item["asset_type"]]["_links"]["activate"]

			print (item_activation_url)

			# request activation
			response = session.post(item_activation_url)

			response_list.append(response)
	except Exception as e:
		print e.message

	return response_list

def request_search_list():
	search_results = search_endpoint.search().text

	search_list = parse_search_json(search_results)

	return search_list

def activate():
	response_list = request_items(request_search_list())

	print response_list
	return response_list

