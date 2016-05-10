import psycopg2
from pyMetricServer.config import *
import time


database = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_NAME)
cursor = database.cursor();
cursor.execute("CREATE TABLE IF NOT EXISTS log_messages (Id BIGSERIAL, Time INTEGER, Origin TEXT, Message TEXT, Type INTEGER);")
cursor.execute("CREATE TABLE IF NOT EXISTS log_metric (Id BIGSERIAL, Time INTEGER, Origin TEXT, Key TEXT, Value DOUBLE PRECISION)")
database.commit()
cursor.close()



def getMetric(timefrom = None, timeto = None, origin = None, key = None, count = None, order = None):
    results = []
    cursor = database.cursor()

    params = []
    query = "SELECT Id, Time, Origin, Key, Value FROM log_metric "
    if(timefrom != None or timeto != None or origin != None or key != None):
        query += "WHERE "

    if timefrom != None:
        query += "Time >= %s AND "
        params.append(timefrom)

    if timeto != None:
        query += "Time <= %s AND "
        params.append(timeto)

    if origin != None:
        query += "Origin = %s AND "
        params.append(origin)

    if key != None:
        query += "Key = %s AND "
        params.append(key)

    query = query.strip("AND ")
    query += " "


    if order != None and order[0] != None:
        if(order[1]):
            query += "ORDER BY %s DESC " % order[0]
        else:
            query += "ORDER BY %s ASC " % order[0]

    if count != None:
        query += "LIMIT %s "
        params.append(count)

    cursor.execute(query, tuple(params))
    for row in cursor:
        results.append({
            "Id": str(row[0]),
            "Time": str(row[1]),
            "Origin": str(row[2]),
            "Key": str(row[3]),
            "Value": str(row[4]),
        })

    return results
