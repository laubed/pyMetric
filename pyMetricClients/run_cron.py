#!/usr/bin/python
import sys
import httplib


if len(sys.argv) == 2:
    endpoint = str(sys.argv[1])

    connection = httplib.HTTPConnection(endpoint)
    connection.request("GET", "/metric/api/v1.0/cron")
    connection.getresponse()
    sys.exit(0)
else:
    print "Usage run_cron.py <API Endpoint>"
    sys.exit(-1)