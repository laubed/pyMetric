import psycopg2
from pyMetricServer.config import *
import time


database = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_NAME)
cursor = database.cursor();
cursor.execute("CREATE TABLE IF NOT EXISTS log_messages (Id BIGSERIAL, Time INTEGER, Origin TEXT, Message TEXT, Type INTEGER);")
cursor.execute("CREATE TABLE IF NOT EXISTS log_metric (Id BIGSERIAL, Time INTEGER, Origin TEXT, Key TEXT, Value DOUBLE PRECISION)")
database.commit()
cursor.close()
