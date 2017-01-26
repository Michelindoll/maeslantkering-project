import db,api, time, datetime

def GrabData(locatienaam, apidata):
    print("Getting data for "+locatienaam)
    try:
        latestdata = db.SelectLastReadingFromDB(locatienaam)
    except:
        print("Getting latest data failed for "+locatienaam)
    try:
        data = api.GetNAPLocation(locatienaam, apidata)
        print("Got API data")
    except:
        print("Api call failed for "+locatienaam)

    waterstand = data['waarde']
    tijd = data['meettijd']

    try:
        print(locatienaam, tijd, latestdata[1])
        if int(tijd) != int(latestdata[1]):
            print("Posting data to DB")
            db.WriteSensorDataToDB(waterstand, tijd, locatienaam)
            print("Posted data to DB")
            print("Got data for " + locatienaam + ' ' + str(datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y ')))
        else:
            print("Dubbele Waarde")
    except:
        print("Posting data DB failed for "+locatienaam)
    print(' ')


while True:
    apidata = api.GetNAPDataRWS()
    GrabData('Maeslantkering zeezijde N', apidata)
    GrabData('Rotterdam', apidata)
    GrabData('Dordrecht', apidata)
    print("Sleeping")
    time.sleep(300)
