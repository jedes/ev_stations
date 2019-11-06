# curl -d '{ "FilteringOptions": {"AvailableStationsOnly": "False", "FastDCStationsOnly": "False", "ShowOtherNetworkStations": "True" } }' -X POST -H "Content-Type: application/json; charset=utf-8" https://account.flo.ca/api/network/markers

import requests
import pickle
from collections import namedtuple

MapPerspective = namedtuple('MapPerspective',
                            ['zoom', 'south', 'west', 'north', 'east'])

with open('stations_list.dat', 'wb') as outfile:

    def recurseMap(mp):
        latSpan = abs(mp.north - mp.south) / 2
        lngSpan = abs(mp.east - mp.west) / 2
        processZoomLevel(MapPerspective(mp.zoom+1,
                         mp.south, mp.west,
                         mp.south+latSpan, mp.west+lngSpan))
        processZoomLevel(MapPerspective(mp.zoom+1,
                         mp.south, mp.west+lngSpan,
                         mp.south+latSpan, mp.east))
        processZoomLevel(MapPerspective(mp.zoom+1,
                         mp.south+latSpan, mp.west,
                         mp.north, mp.west+lngSpan))
        processZoomLevel(MapPerspective(mp.zoom+1,
                         mp.south+latSpan, mp.west+lngSpan,
                         mp.north, mp.east))

    def processZoomLevel(mp):
        r = requests.post('https://account.flo.ca/api/network/markers',
             headers={'Content-Type': 'application/json; charset=utf-8',
                      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'},
             json={"FilteringOptions": {"AvailableStationsOnly": "False",
                                        "FastDCStationsOnly": "False",
                                        "ShowOtherNetworkStations": "True"},
                   "ZoomLevel": mp.zoom,
                   "Bounds": {"SouthWest": {"Lat": mp.south, "Lng": mp.west},
                              "NorthEast": {"Lat": mp.north, "Lng": mp.east}}})

        if r.status_code != 200:
            raise -1

        hasClusters = False
        for station in r.json():
            if station['IsCluster']:
                hasClusters = True
                break

        if hasClusters:
            recurseMap(mp)
        else:
            for station in r.json():
                pickle.dump(station, outfile)

    processZoomLevel(MapPerspective(5, 39, -97, 59, -47))
