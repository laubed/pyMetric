import time

from pyMetricServer.system.decorators import crossdomain

from pyMetricServer import app
from pyMetricServer.config import *
from pyMetricServer.system.database import database


@app.route('/metric/api/v1.0/cron')
@crossdomain(origin="*", headers="Content-Type,Accept")
def run_cron():
    cursor = database.cursor()
    cursor.execute("DELETE FROM log_messages WHERE Time < %s", (time.time() - DATABASE_DELETE_PERIOD,))
    message = cursor.statusmessage
    cursor.close()
    database.commit()
    return "{'message': '" + message + "'}"
