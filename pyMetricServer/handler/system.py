import time

from pyMetricServer.system.decorators import crossdomain

from pyMetricServer import app
from pyMetricServer.config import *
from pyMetricServer.system.database import database


@app.route('/api/v1.0/cron')
@crossdomain(origin="*", headers="Content-Type,Accept")
def run_cron():
    """
    Runs some database cleanup (optional if database gets to big)
    TODO: shedule this into another thread so we don't need to trust cron to curl that api endpoint
    :return:
    """
    cursor = database.cursor()
    cursor.execute("DELETE FROM log_messages WHERE Time < %s", (time.time() - DATABASE_DELETE_PERIOD,))
    message = cursor.statusmessage
    cursor.close()
    database.commit()
    return "{'message': '" + message + "'}"
