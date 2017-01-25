import db,api, time, datetime

waterstand = 0
tijd = 0
while True:
    latestdata = db.SelectLastReadingFromDB()
    print("Getting data")
    maeslantkeringdata = api.GetNAPMaeslantkering()
    print("Got API data")
    waterstand = maeslantkeringdata['waarde']
    tijd = maeslantkeringdata['meettijd']
    if tijd != latestdata[1]:
        print("Posting data to DB")
        db.WriteSensorDataToDB(waterstand,tijd)
        print("Posted data to DB")
    else:
        print("Dubbele Waarde")
    print(str(datetime.datetime.now()))
    print("Sleeping")
    time.sleep(1200)
