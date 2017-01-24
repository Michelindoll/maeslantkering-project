import json
try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Fallback for Python 2
    from urllib import urlopen, request

def GetNAPMaeslantkering():
    url = "http://www.rijkswaterstaat.nl/apps/geoservices/rwsnl/?mode=features&projecttype=waterstanden"
    response = urlopen(url)
    output = json.loads(response.read().decode("utf-8"))
    for item in output['features']:
        if item['locatienaam'] == 'Maeslantkering zeezijde N':
            measlantkeringwaterstand = item
            break
    return measlantkeringwaterstand
