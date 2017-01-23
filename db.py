import pymysql
from auth import dbpass, dbuser, dbhost, db

def createSQLConnection():
    return pymysql.connect(host=dbhost, user=dbuser, password=dbpass, db=db)

def SelectFromDB(field, table, where):
    connection = createSQLConnection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT {} FROM {} WHERE {}".format(field, table, where)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def WriteSensorDataToDB(WaterLevel, Timestamp):
    connection = createSQLConnection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO SensorData (WaterLevel, Time) VALUES ({},{})".format(WaterLevel, Timestamp)
        cursor.execute(sql)
    connection.commit()
