import pymysql, aes
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
        sql = "SELECT waterstand, tijd FROM (SELECT * FROM sensordata ORDER BY tijd DESC LIMIT 35) T1 ORDER BY tijd"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def SelectLastReadingFromDB():
    connection = createSQLConnection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT waterstand, tijd FROM sensordata ORDER BY tijd DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        waterstand = result[0]['waterstand']
        tijd = result[0]['tijd']
        return waterstand, tijd

def getLoginCredentails():
    connection = createSQLConnection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT username, password FROM user"
        cursor.execute(sql)
        result = cursor.fetchall()
        password = aes.decryptData(eval(result[0]['password']))
        username = aes.decryptData(eval(result[0]['username']))
        return username, password
