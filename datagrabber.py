import db,api, time, datetime

waterstand = 0
tijd = 0
while True:
    try:
        latestdata = db.SelectLastReadingFromDB()
    except:
        print("Getting latest data failed")
    print("Getting data")
    try:
        maeslantkeringdata = api.GetNAPMaeslantkering()
        print("Got API data")
        waterstand = maeslantkeringdata['waarde']
        tijd = maeslantkeringdata['meettijd']
        print(tijd, latestdata[1])
        if int(tijd) != int(latestdata[1]):
            print("Posting data to DB")
            db.WriteSensorDataToDB(waterstand,tijd)
            print("Posted data to DB")
        else:
            print("Dubbele Waarde")
    except:
        print("Api call failed")
    print(str(datetime.datetime.now()))
    print("Sleeping")
    time.sleep(1200)
