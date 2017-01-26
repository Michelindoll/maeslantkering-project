import db,api, time, datetime

def GrabData(locatienaam, apidata):
    print("Getting data for "+locatienaam)
    try:
        latestdata = db.SelectLastReadingFromDB()
    except:
        print("Getting latest data failed for "+locatienaam)
    try:
        data = api.GetNAPLocation(locatienaam, apidata)
        print("Got API data")
        waterstand = data['waarde']
        tijd = data['meettijd']
        print(locatienaam, tijd, latestdata[1])
        if int(tijd) != int(latestdata[1]):
            print("Posting data to DB")
            db.WriteSensorDataToDB(waterstand, tijd, locatienaam)
            print("Posted data to DB")
            print("Got data for " + locatienaam + ' ' + str(datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y ')))
        else:
            print("Dubbele Waarde")
    except:
        print("Api call failed for"+locatienaam)



while True:
    apidata = api.GetNAPDataRWS()
    GrabData('Maeslantkering zeezijde N', apidata)
    GrabData('Rotterdam', apidata)
    GrabData('Dordrecht', apidata)
    print("Sleeping")
    time.sleep(300)
