from server import app
from ratselib.decorators import crossdomain
from system_database import database
from config import *
import time


@app.route('/monitoring/api/v1.0/cron')
@crossdomain(origin="*", headers="Content-Type,Accept")
def run_cron():
    cursor = database.cursor()
    cursor.execute("DELETE FROM log_messages WHERE Time < %s", (time.time() - DATABASE_DELETE_PERIOD,))
    message = cursor.statusmessage
    cursor.close()
    database.commit()
    return "{'message': '" + message + "'}"