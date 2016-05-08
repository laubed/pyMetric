import time

import math
from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database
from werkzeug.exceptions import abort
from pyMetricServer.system.decorators import crossdomain


@app.route('/metric/api/v1.0/metric/<string:operation>/<string:key>/<int:fromtime>/<int:totime>', defaults={'origin': None})
@app.route("/metric/api/v1.0/metric/<string:operation>/<string:key>/<int:fromtime>/<int:totime>/<string:origin>")
@crossdomain(origin="*")
def get_metric(operation, fromtime, totime, key, origin=None):
    if not origin:
        resentry = None
        if operation == "MAX":
            cursor = database.cursor()
            cursor.execute(
                "SELECT Id, Time, Origin, Key, Value FROM log_metric WHERE Time > %s AND Time < %s AND Key = %s ORDER BY TIME ASC",
                (fromtime, totime, key))
            maxvalue = 0;
            for row in cursor:
                if row[4] >= maxvalue:
                    maxvalue = row[4]
                    resentry = row

        elif operation == "MIN":
            cursor = database.cursor()
            cursor.execute(
                "SELECT Id, Time, Origin, Key, Value FROM log_metric WHERE Time > %s AND Time < %s AND Key = %s ORDER BY TIME ASC",
                (fromtime, totime, key))
            minvalue = float("inf")

            for row in cursor:
                if row[4] <= minvalue:
                    minvalue = row[4]
                    resentry = row

        else:
            return "{'message': 'Operation not supported'}"

        if resentry is not None:
            return '{"Id": "%s", "Time": "%s", "Origin": "%s", "Key": "%s", "Value": "%s"},' % (
                str(resentry[0]), str(resentry[1]), str(resentry[2]), str(resentry[3]), str(resentry[4]))
        else:
            return "{}"
    else:
        resentries = []
        if operation == "GET":
            cursor = database.cursor()
            cursor.execute(
                "SELECT Id, Time, Origin, Key, Value FROM log_metric WHERE Time > %s AND Time < %s AND Key = %s AND Origin = %s ORDER BY Time ASC",
                (fromtime, totime, key, origin))
            for resentry in cursor:
                resentries.append((str(resentry[0]), str(resentry[1]), str(resentry[2]), str(resentry[3]), str(resentry[4])))

        result = "["
        for resentry in resentries:
            result += '{"Id": "%s", "Time": "%s", "Origin": "%s", "Key": "%s", "Value": "%s"},' % (
                str(resentry[0]), str(resentry[1]), str(resentry[2]), str(resentry[3]), str(resentry[4]))
        result = result.strip().strip(",")
        result += "]"
        return result


@app.route('/metric/api/v1.0/metric', methods=['POST'])
@crossdomain(origin='*')
def add_metric():
    print request.json
    if not request.json or not 'Origin' in request.json or not 'Key' in request.json or not 'Value' in request.json:
        abort(400)
    else:
        cursor = database.cursor()
        cursor.execute("INSERT INTO log_metric (Time, Origin, Key, Value) VALUES (%s,%s,%s,%s);",
                       (time.time(), request.json["Origin"], request.json["Key"], request.json["Value"]))
        cursor.close()
        database.commit()
        return "{'message': 'OK'}"
