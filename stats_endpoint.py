#stats endpoint

import os
import requests
from requests.auth import HTTPBasicAuth
from demo_filters import environment
from demo_filters import redding


def stats_initialize():
	stats_endpoint_request = {
	  "interval": "day",
	  "item_types": ["REOrthoTile"],
	  "filter": redding
	}

	return stats_endpoint_request

def stats():
	result = \
	  requests.post(
	    environment['STATS_ENDPOINT'],
	    auth=HTTPBasicAuth(environment['API_KEY'], ''),
	    json=stats_initialize() )
	return result
