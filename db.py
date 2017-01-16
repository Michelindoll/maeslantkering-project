import pymysql
from auth import dbpass, dbuser, dbhost, db

def createSQLConnection():
    return pymysql.connect(host=dbhost, user=dbuser, password=dbpass, db=db)

def WriteToDB(table, field, value):
    connection = createSQLConnection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table, field, value)
        cursor.execute(sql)
    connection.commit()

def SelectFromDB(field, table, where):
    connection = createSQLConnection()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT {} FROM {} WHERE {}".format(field, table, where)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
