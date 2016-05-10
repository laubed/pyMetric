import time

import math
from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database, getMetric, insertMetric
from werkzeug.exceptions import abort
from pyMetricServer.system.decorators import crossdomain
from flask.json import jsonify
import time


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
    Example:
        GET /api/v1.0/metrics/get?fromtime=0&totime=123000423&origin=10.0.0.9&key=cpu_usage&count=20&order=time&desc=false
    :return:    returns all rows in metric data which matches specified criteria
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
        Example:
            GET /api/v1.0/metrics/current?origin=10.0.0.9&key=cpu_usage
        :return:    returns all rows in metric data which matches specified criteria
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
    """
    Used to insert a metric value into database
    Post Params:
        origin      -   Origin of the metric data
        key         -   Key of the metric data
        value       -   Value of the metric data
        time        -   Timestamp of the metric data (optional)
    :return:    returns the row just inserted
    """
    origin = request.form.get("origin", None)
    key = request.form.get("key", None)
    value = request.form.get("value", None)
    times = request.form.get("time", time.time())
    if origin == None or key == None or value == None:
        abort(400)
    else:
        res = insertMetric(times, origin, key, value)
        return jsonify({
            "results": res,
            "resultcount": len(res)
        })



