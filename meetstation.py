import db
import time

def GetDataFromSensor():
    SensorData = 3.00
    return SensorData

WaterLevel = GetDataFromSensor()
Unixtime = int(time.time())
db.WriteSensorDataToDB(WaterLevel, Unixtime)
time.sleep(60)
