import db
import time

def GetDataFromSensor():
    SensorData = 3.00
    return SensorData

WaterLevel = GetDataFromSensor()
TimeStamp = int(time.time())
db.WriteSensorDataToDB(WaterLevel, TimeStamp)
time.sleep(60)
