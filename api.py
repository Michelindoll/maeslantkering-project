import json
try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Fallback for Python 2
    from urllib import urlopen, request

def GetNAPDataRWS():
    url = "http://www.rijkswaterstaat.nl/apps/geoservices/rwsnl/?mode=features&projecttype=waterstanden"
    response = urlopen(url)
    output = json.loads(response.read().decode("utf-8"))
    return output

def GetNAPLocation(locatieNaam, apidata):
    for item in apidata['features']:
        if item['locatienaam'] == locatieNaam:
            waterstand = item
            break
    return waterstand
