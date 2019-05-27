# the geo json geometry object we got from geojson.io
import os

geo_json_geometry = {
  "type": "Polygon",
  "coordinates": [
    [
      [
        -116.25114440917967,
        33.67838986400781
      ],
      [
        -116.2341070175171,
        33.67838986400781
      ],
      [
        -116.2341070175171,
        33.685246405160576
      ],
      [
        -116.25114440917967,
        33.685246405160576
      ],
      [
        -116.25114440917967,
        33.67838986400781
      ]
    ]
  ]
}

environment = {
  "API_KEY"       : os.environ['PLANET_API_KEY'],
  "STATS_ENDPOINT"  : "https://api.planet.com/data/v1/stats",
  "SEARCH_ENDPOINT" : "https://api.planet.com/data/v1/quick-search",
  "ACTIVATION_ENDPOINT" : "https://api.planet.com/data/v1/item-types/"
}

# filter for items the overlap with our chosen geometry
geometry_filter = {
  "type": "GeometryFilter",
  "field_name": "geometry",
  "config": geo_json_geometry
}


# filter images acquired in a certain date range
date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "2019-04-20T00:00:00.000Z",
    "lte": "2019-04-22T00:00:00.000Z"
  }
}

# filter any images which are more than lte% clouds
cloud_cover_filter = {
  "type": "RangeFilter",
  "field_name": "cloud_cover",
  "config": {
    "lte": 0.5
  }
}

# create a filter that combines our geo and date filters
# could also use an "OrFilter"
redding = {
  "type": "AndFilter",
  "config": [geometry_filter, date_range_filter, cloud_cover_filter]
}