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
    res = getMetric(request.args.get("fromtime", None), request.args.get("totime", None),
                    request.args.get("origin", None), request.args.get("key", None), request.args.get("count", None),
                    (request.args.get("order", "Time"), bool(request.args.get("desc", True))));
    return jsonify({"results": res, "resultcount": len(res)})


@app.route("/metric/api/v1.0/metric/current")
@crossdomain(origin="*")
def current_metric():
    res = getMetric(request.args.get("fromtime", None), request.args.get("totime", None),
                    request.args.get("origin", None), request.args.get("key", None), 1,
                    ("Time", True))
    return jsonify({"results": res, "resultcount": len(res)})


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



