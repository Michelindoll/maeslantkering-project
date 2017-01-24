import pymysql
from auth import dbpass, dbuser, dbhost, db

def createSQLConnection():
    return pymysql.connect(host=dbhost, user=dbuser, password=dbpass, db=db)

def WriteSensorDataToDB(WaterLevel, Unixtime):
    connection = createSQLConnection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO sensordata (waterstand, tijd) VALUES ({},{})".format(WaterLevel, Unixtime)
        cursor.execute(sql)
    connection.commit()

def SelectSensorDataFromDB():
    connection = createSQLConnection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT waterstand, tijd FROM (SELECT * FROM sensordata ORDER BY tijd DESC) T1 ORDER BY tijd"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def SelectLastReadingFromDB():
    connection = createSQLConnection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT waterstand AS waterstand FROM sensordata ORDER BY tijd DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
