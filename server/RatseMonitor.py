#!flask/bin/python
import time
import psycopg2
from flask import Flask, jsonify, abort, request, make_response

from ratselib.decorators import crossdomain
from config import *

app = Flask(__name__)


database = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_NAME)
cursor = database.cursor();
cursor.execute("CREATE TABLE IF NOT EXISTS log_messages (Time INTEGER, Origin TEXT, Message TEXT, Type INTEGER);")
database.commit();


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/monitoring/api/v1.0/cron')
@crossdomain(origin="*", headers="Content-Type,Accept")
def run_cron():
    cursor = database.cursor()
    cursor.execute("DELETE FROM log_messages WHERE Time < %s", (time.time() - DATABASE_DELETE_PERIOD,))
    message = cursor.statusmessage
    cursor.close()
    database.commit()
    return "{'error': '" + message + "'}"


@app.route('/monitoring/api/v1.0/log_message/all/<int:max>', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_log_max(max):
    return get_log_timespan(max, 0, time.time());


@app.route('/monitoring/api/v1.0/log_message/all', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_log():
    return get_log_timespan(0, 0, time.time());


@app.route('/monitoring/api/v1.0/log_message/<int:fromTime>/<int:toTime>', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_log_timespan(max, fromTime, toTime):
    return get_log_timespan_filter(fromTime, toTime, None, max);


@app.route('/monitoring/api/v1.0/log_message/<int:fromtime>/<int:totime>/<string:typefilter>', methods=['GET'])
@crossdomain(origin='*', headers="Content-Type,Accept")
def get_log_timespan_filter(fromtime, totime, typefilter, max):
    cursor = database.cursor();

    if(typefilter != None):
        if(max != 0):
            cursor.execute("SELECT * FROM log_messages WHERE Type = %s AND Time > %s AND TIME < %s ORDER BY Time DESC LIMIT %s;", (typefilter, fromtime, totime, max));
        else:
            cursor.execute(
                "SELECT * FROM log_messages WHERE Type = %s AND Time > %s AND TIME < %s ORDER BY Time DESC;",
                (typefilter, fromtime, totime));
    else:
        if(max != 0):
            cursor.execute("SELECT * FROM log_messages WHERE Time > %s AND TIME < %s ORDER BY Time DESC LIMIT %s;",
                       ( fromtime, totime, max));
        else:
            cursor.execute("SELECT * FROM log_messages WHERE Time > %s AND TIME < %s ORDER BY Time DESC;",
                           (fromtime, totime));
    data = "["
    for dataobj in cursor:
        data += """
            {
                "Id" : \"""" + str(dataobj[4]) + """\",
                "Time" : \"""" + str(dataobj[0]) + """\",
                "Origin" : \"""" + dataobj[1] + """\",
                "Message" : \"""" + dataobj[2] + """\",
                "Type" : \"""" + str(dataobj[3]) + """\"
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
        cursor.execute("INSERT INTO log_messages (Time, Origin, Message, Type) VALUES (%s,%s,%s,%s);", (time.time(), request.json["Origin"], request.json["Message"], request.json["Type"]));
        cursor.close()
        database.commit()
        return "{'error': 'OK'}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
