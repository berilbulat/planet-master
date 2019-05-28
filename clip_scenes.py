from demo_filters import environment
from demo_filters import geo_json_geometry
import json
import requests
import time
import os
from tqdm import tqdm
import zipfile
import activation

# Set API key (this should to be an environment variable)
api_key = environment['API_KEY']

# Download Location
output = "output/"

# Area Of Interest (clip geometry) in GeoJSON format
aoi_json = geo_json_geometry

search_list = activation.request_search_list()
print search_list
for search in search_list:
    # Construct clip API payload
    clip_payload = {
        'aoi': geo_json_geometry,
        'targets': [
          {
            'item_id': search['item_id'],
            'item_type': search['item_type'],
            'asset_type': search['asset_type']
          }
        ]
    }

    # Request clip of scene (This will take some time to complete)
    request = requests.post(environment["CLIP_ENDPOINT"], auth=(api_key, ''), json=clip_payload)
    print request.json()

    clip_url = request.json()['_links']['_self']

    # Poll API to monitor clip status. Once finished, download and upzip the scene
    clip_succeeded = False
    while not clip_succeeded:

        # Poll API
        check_state_request = requests.get(clip_url, auth=(api_key, ''))
        
        # If clipping process succeeded , we are done
        if check_state_request.json()['state'] == 'succeeded':
            clip_download_url = check_state_request.json()['_links']['results'][0]
            clip_succeeded = True
            print("Clip of scene succeeded and is ready to download") 
        
        # Still activating. Wait 1 second and check again.
        else:
            print("...Still waiting for clipping to complete...")
            time.sleep(1)

    # Download clip
    response = requests.get(clip_download_url, stream=True)
    with open(output + search['item_id'] + '.zip', "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

    # Unzip file
    ziped_item = zipfile.ZipFile(output + search['item_id'] + '.zip')
    ziped_item.extractall(output + search['item_id'])    
      
    # Delete zip file
    os.remove(output + search['item_id'] + '.zip')
    print('Downloaded clips located in: ' + output + " for " + search['item_id'] )