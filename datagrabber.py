import db,api, time

while True:
    print("Getting data")
    maeslantkeringdata = api.GetNAPMaeslantkering()
    print("Got API data")
    waterstand = maeslantkeringdata['waarde']
    tijd = maeslantkeringdata['meettijd']
    print("Posting data to DB")
    db.WriteSensorDataToDB(waterstand,tijd)
    print("Posted data to DB")
    print("Sleeping")
    time.sleep(1200)
