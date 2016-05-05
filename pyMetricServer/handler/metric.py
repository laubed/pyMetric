import time

from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database
from werkzeug.exceptions import abort

from pyMetricServer.system.decorators import crossdomain


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
