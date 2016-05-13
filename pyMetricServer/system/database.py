"""
Database module

used to fetch and insert data into the database.
Constructs queries from arguments with most of them being optional.
Prevent some SQL injection attacks (most of them are secured via psycopg2)
"""
import psycopg2
import random

from pyMetricServer import DEBUG
from pyMetricServer.config import *
import time


if not DEBUG:
    database = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS,
                                database=DATABASE_NAME)
    cursor = database.cursor();
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS log_messages (Id BIGSERIAL, Time INTEGER, Origin TEXT, Message TEXT, Type INTEGER);")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS log_metrics (Id BIGSERIAL, Time INTEGER, Origin TEXT, Key TEXT, Value DOUBLE PRECISION);")
    database.commit()
    cursor.close()
else:
    database = None


def getMetric(timefrom=None, timeto=None, origin=None, key=None, count=None, order=None):
    if DEBUG:
        return getMetricDebug(timefrom, timeto, origin, key, count, order)

    results = []
    cursor = database.cursor()

    params = []
    query = "SELECT Id, Time, Origin, Key, Value FROM log_metrics "
    if (timefrom != None or timeto != None or origin != None or key != None):
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
        if order[1]:
            desc = "DESC "
        else:
            desc = "ASC "

        if order[0] == "time":
            query += "ORDER BY Time " + desc
        elif order[0] == "value":
            query += "ORDER BY Value " + desc
        elif order[0] == "key":
            query += "ORDER BY Key " + desc
        elif order[0] == "origin":
            query += "ORDER BY Origin " + desc
        elif order[0] == "id":
            query += "ORDER BY Id" + desc

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
            "Value": str(row[4])
        })

    cursor.close()

    return results


def getMetricDebug(timefrom=None, timeto=None, origin=None, key=None, count=None, order=None):
    results = []
    for x in range((int(timeto)-int(timefrom))/20):
        results.append({
            "Id": str(random.randint(1, 2*1024*1024)),
            "Time": str(time.time()-x*20),
            "Origin": str(origin),
            "Key": str(key),
            "Value": str(random.randint(0, 100))
        })
    return results




def getMessage(timefrom=None, timeto=None, origin=None, typ=None, count=None, order=None):
    results = []
    cursor = database.cursor()

    params = []
    query = "SELECT Id, Time, Origin, Message, Type FROM log_messages "
    if (timefrom != None or timeto != None or origin != None or typ != None):
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

    if typ != None:
        query += "Type = %s AND "
        params.append(typ)

    query = query.strip("AND ")
    query += " "

    if order != None and order[0] != None:
        if order[1]:
            desc = "DESC "
        else:
            desc = "ASC "

        if order[0] == "time":
            query += "ORDER BY Time " + desc
        elif order[0] == "type":
            query += "ORDER BY Type " + desc
        elif order[0] == "origin":
            query += "ORDER BY Origin " + desc
        elif order[0] == "id":
            query += "ORDER BY Id" + desc

    if count != None:
        query += "LIMIT %s "
        params.append(count)

    cursor.execute(query, tuple(params))
    for row in cursor:
        results.append({
            "Id": str(row[0]),
            "Time": str(row[1]),
            "Origin": str(row[2]),
            "Message": str(row[3]),
            "Type": str(row[4])
        })

    return results
    pass


def insertMetric(time, origin, key, value):
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO log_metrics (Time, Origin, Key, Value) VALUES (%s, %s, %s, %s) RETURNING Id, Time, Origin, Key, Value",
        (time, origin, key, value))
    row = cursor.fetchone()
    cursor.close()
    database.commit()
    return {
        "Id": str(row[0]),
        "Time": str(row[1]),
        "Origin": str(row[2]),
        "Key": str(row[3]),
        "Value": str(row[4])
    }


def insertMessage(time, origin, message, typ):
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO log_messages (Time, Origin, Message, Type) VALUES (%s, %s, %s, %s) RETURNING Id, Time, Origin, Message, Type",
        (time, origin, message, typ));
    row = cursor.fetchone()
    cursor.close()
    database.commit()
    return {
        "Id": str(row[0]),
        "Time": str(row[1]),
        "Origin": str(row[2]),
        "Message": str(row[3]),
        "Type": str(row[4])
    }
