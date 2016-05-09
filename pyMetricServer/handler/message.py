import time

from flask import request
from pyMetricServer import app
from pyMetricServer.system.database import database
from werkzeug.exceptions import abort

from pyMetricServer.system.decorators import crossdomain


@app.route('/metric/api/v1.0/message/<string:maxentries>', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_message_short(maxentries):
    return get_message_long(0, time.time(), maxentries)


@app.route('/metric/api/v1.0/message/<int:fromtime>/<int:totime>/<string:maxentries>', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_message_long(fromtime, totime, maxentries):
    cursor = database.cursor()

    if maxentries != 0:
        cursor.execute("SELECT Id, Time, Origin, Message, Type FROM log_messages WHERE Time > %s AND TIME < %s ORDER BY Time DESC LIMIT %s;",
                       (fromtime, totime, maxentries))
    else:
        cursor.execute("SELECT Id, Time, Origin, Message, Type FROM log_messages WHERE Time > %s AND TIME < %s ORDER BY Time DESC;",
                       (fromtime, totime))

    data = "["
    for dataobject in cursor:
        data += """
            {
                "Id" : \"""" + str(dataobject[0]) + """\",
                "Time" : \"""" + str(dataobject[1]) + """\",
                "Origin" : \"""" + str(dataobject[2]) + """\",
                "Message" : \"""" + str(dataobject[3]) + """\",
                "Type" : \"""" + str(dataobject[4]) + """\"
            },
        """
    data = data.strip().strip(",")
    data += "]"
    cursor.close()
    return data, 200, {'Content-Type': 'application/json'}


@app.route('/metric/api/v1.0/message', methods=['POST'])
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
