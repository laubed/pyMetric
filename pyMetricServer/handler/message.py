import time

from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database, getMessage
from werkzeug.exceptions import abort
from flask.json import jsonify

from pyMetricServer.system.decorators import crossdomain

@app.route('/metric/api/v1.0/messages/get', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_messages():
    timefrom = request.args.get("timefrom", None)
    timeto = request.args.get("timeto", None)
    origin = request.args.get("origin", None)
    typ = request.args.get("type", None)
    count = request.args.get("count", None)
    order = (request.args.get("order", "time"), bool(request.args.get("desc", True)))
    res = getMessage(timefrom, timeto, origin, typ, count, order)
    return jsonify({
        "results": res,
        "resultcount": len(res),
        "param_fromtime": timefrom,
        "param_totime": timeto,
        "param_origin": origin,
        "param_type": typ,
        "param_count": count,
        "param_order": order[0],
        "param_desc": order[1]
    })

@app.route('/metric/api/v1.0/messages', methods=['POST'])
@crossdomain(origin='*')
def add_message():
    # print request.json
    if not request.json or not 'Origin' in request.json or not 'Message' in request.json or not 'Type' in request.json:
        abort(400)
    else:
        cursor = database.cursor();
        cursor.execute("INSERT INTO log_messages (Time, Origin, Message, Type) VALUES (%s,%s,%s,%s);",
                       (time.time(), request.json["Origin"], request.json["Message"], request.json["Type"]))
        cursor.close()
        database.commit()
        return "{'message': 'OK'}"
