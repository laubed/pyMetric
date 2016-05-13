"""
Message data handler

Used to insert or fetch message data.
Only handles get/post request. Database interaction is done in database module
"""
import time

from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database, getMessage, insertMessage
from werkzeug.exceptions import abort
from flask.json import jsonify

from pyMetricServer.system.decorators import crossdomain


@app.route('/api/v1.0/messages/get', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_messages():
    """
    Used to get a list of message entries
    GET Params:
        timefrom    -   Only fetch messages more recent than this timestamp
        timeto      -   Only fetch messages older than this timestamp
        origin      -   Only fetch messages with this origin
        type        -   Only fetch messages with this type
        count       -   Only fetch that much messages
        order       -   specifies an order column: time,origin,type,id
        desc        -   specifies an order type: desc -> true, asc -> false

    :return:    return a list of messages in a json container
    """
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


@app.route('/api/v1.0/messages', methods=['POST'])
@crossdomain(origin='*')
def add_message():
    """
    Used to add a message entry
    POST Params:
        origin      -       Origin of the message
        message     -       The message itself
        type        -       The messagetype
        time        -       The timestamp of the message (optional, use current time if not specified)
    :return:    The inserted message in json container
    """
    # print request.json
    origin = request.form.get("origin", None)
    message = request.form.get("message", None)
    typ = request.form.get("type", None)
    times = request.form.get("time", time.time())
    if origin == None or message == None or typ == None:
        abort(400)
    else:
        res = insertMessage(times, origin, message, typ)
        return jsonify({
            "results": res,
            "resultcount": len(res)
        })