import os
import requests
from requests.auth import HTTPBasicAuth

# demo filter that filters by geometry, date and cloud cover
from demo_filters import environment
from demo_filters import redding

def search_initialize(): 
	# Search API request object
	search_endpoint_request = {
	  "item_types" : ["PSScene4Band"],
	  "filter" : redding
	}
	return search_endpoint_request

def search():
	result = \
	  requests.post(
	    environment['SEARCH_ENDPOINT'],
	    auth=HTTPBasicAuth(environment['API_KEY'], ''),
	    json=search_initialize() )
	return result

#print search().text
