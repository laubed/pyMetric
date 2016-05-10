import time

import math
from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database, getMetric
from werkzeug.exceptions import abort
from pyMetricServer.system.decorators import crossdomain
from flask.json import jsonify


@app.route("/metric/api/v1.0/metric/get")
@crossdomain(origin="*")
def get_metric():
    res = getMetric(request.args.get("fromtime", None), request.args.get("totime", None),
                    request.args.get("origin", None), request.args.get("key", None), request.args.get("count", None),
                    (request.args.get("order", None), bool(request.args.get("desc", False))));
    return jsonify({"results": res})


@app.route("/metric/api/v1.0/metric/current")
@crossdomain(origin="*")
def current_metric():
    res = getMetric(request.args.get("fromtime", None), request.args.get("totime", None),
                    request.args.get("origin", None), request.args.get("key", None), 1,
                    ("Time", False))
    return jsonify({"results": res})


@app.route('/metric/api/v1.0/metric', methods=['POST'])
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



