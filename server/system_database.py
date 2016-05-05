import psycopg2
from config import *
import time


database = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_NAME)
cursor = database.cursor();
cursor.execute("CREATE TABLE IF NOT EXISTS log_messages (Time INTEGER, Origin TEXT, Message TEXT, Type INTEGER);")
database.commit();