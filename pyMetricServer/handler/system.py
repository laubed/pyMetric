import time

from pyMetricService.pymetriclib.decorators import crossdomain

from pyMetricService import app
from pyMetricService.config import *
from pyMetricService.system.database import database


@app.route('/monitoring/api/v1.0/cron')
@crossdomain(origin="*", headers="Content-Type,Accept")
def run_cron():
    cursor = database.cursor()
    cursor.execute("DELETE FROM log_messages WHERE Time < %s", (time.time() - DATABASE_DELETE_PERIOD,))
    message = cursor.statusmessage
    cursor.close()
    database.commit()
    return "{'message': '" + message + "'}"
