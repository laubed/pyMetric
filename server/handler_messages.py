from flask import request
from werkzeug.exceptions import abort

from server import app
from ratselib.decorators import crossdomain
from system_database import database
import time


@app.route('/monitoring/api/v1.0/log_message/<string:maxentries>', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_log_short(maxentries):
    return get_log_full(0, time.time(), maxentries)


@app.route('/monitoring/api/v1.0/log_message/<int:fromtime>/<int:totime>/<string:maxentries>', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_log_full(fromtime, totime, maxentries):
    cursor = database.cursor()

    if maxentries != 0:
        cursor.execute("SELECT * FROM log_messages WHERE Time > %s AND TIME < %s ORDER BY Time DESC LIMIT %s;",
                       (fromtime, totime, maxentries))
    else:
        cursor.execute("SELECT * FROM log_messages WHERE Time > %s AND TIME < %s ORDER BY Time DESC;",
                       (fromtime, totime))

    data = "["
    for dataobject in cursor:
        data += """
            {
                "Id" : \"""" + str(dataobject[4]) + """\",
                "Time" : \"""" + str(dataobject[0]) + """\",
                "Origin" : \"""" + dataobject[1] + """\",
                "Message" : \"""" + dataobject[2] + """\",
                "Type" : \"""" + str(dataobject[3]) + """\"
            },
        """
    data = data.strip().strip(",")
    data += "]"
    cursor.close()
    return data, 200, {'Content-Type': 'application/json'}


@app.route('/monitoring/api/v1.0/log_message', methods=['POST'])
@crossdomain(origin='*')
def add_log():
    print request.json
    if not request.json or not 'Origin' in request.json or not 'Message' in request.json or not 'Type' in request.json:
        abort(400)
    else:
        cursor = database.cursor();
        cursor.execute("INSERT INTO log_messages (Time, Origin, Message, Type) VALUES (%s,%s,%s,%s);",
                       (time.time(), request.json["Origin"], request.json["Message"], request.json["Type"]))
        cursor.close()
        database.commit()
        return "{'message': 'OK'}"
