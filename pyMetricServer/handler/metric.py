import time

import math
from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database, getMetric
from werkzeug.exceptions import abort
from pyMetricServer.system.decorators import crossdomain
from flask.json import jsonify


@app.route("/api/v1.0/metrics/get")
@crossdomain(origin="*")
def get_metric():
    """
    Used to get a list of metric data.
    GET Params:
        fromtime    -   specifies a min timestamp to search for
        totime      -   specifies a max timestamp to search for
        origin      -   specifies the origin field in the database to search for
        key         -   specifies the key field in the database to search for
        count       -   specifies how many rows should be returned
        order       -   specifies the field by which resulsts get ordered
        desc        -   specifies wether the results are sorted in ascending oder descending order
    :return:    return all rows in metric data which matches specified criteria
    """

    fromtime = request.args.get("fromtime", None)
    totime = request.args.get("totime", None)
    origin = request.args.get("origin", None)
    key = request.args.get("key", None)
    count = request.args.get("count", None)
    order = (request.args.get("order", "Time"), bool(request.args.get("desc", True)))
    res = getMetric(fromtime, totime, origin, key, count, order)
    return jsonify({
        "results": res,
        "resultcount": len(res),
        "param_fromtime": fromtime,
        "param_totime": totime,
        "param_origin": origin,
        "param_key": key,
        "param_count": count,
        "param_order": order[0],
        "param_desc": order[1]
    })


@app.route("/api/v1.0/metrics/current")
@crossdomain(origin="*")
def current_metric():
    """
        Used to get the last entry from a specific origin and key
        (You can even use it without origin and key so it shows the last data pushed to the server)
        GET Params:
            origin      -   specifies the origin field in the database to search for
            key         -   specifies the key field in the database to search for
        :return:    return all rows in metric data which matches specified criteria
        """
    fromtime = None
    totime = None
    origin = request.args.get("origin", None)
    key = request.args.get("key", None)
    count = 1
    order = ("time", True)
    res = getMetric(fromtime, totime, origin, key, count, order)
    return jsonify({
        "results": res,
        "resultcount": len(res),
        "param_fromtime": fromtime,
        "param_totime": totime,
        "param_origin": origin,
        "param_key": key,
        "param_count": count,
        "param_order": order[0],
        "param_desc": order[1]
    })


@app.route('/api/v1.0/metrics', methods=['POST'])
@crossdomain(origin='*')
def add_metric():
    # print request.json
    if not request.json or not 'Origin' in request.json or not 'Key' in request.json or not 'Value' in request.json:
        abort(400)
    else:
        cursor = database.cursor()
        cursor.execute("INSERT INTO log_metric (Time, Origin, Key, Value) VALUES (%s,%s,%s,%s);",
                       (time.time(), request.json["Origin"], request.json["Key"], request.json["Value"]))
        cursor.close()
        database.commit()
        return "{'message': 'OK'}"



