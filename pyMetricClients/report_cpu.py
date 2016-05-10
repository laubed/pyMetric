#!/usr/bin/python
import sys
import httplib
import psutil


if len(sys.argv) == 3:
    origin = str(sys.argv[1])
    endpoint = str(sys.argv[2])

    cpu = psutil.cpu_percent(5)

    connection = httplib.HTTPConnection(endpoint)
    connection.request("POST", "/api/v1.0/metrics",
                       """{
                            "Origin":"%s",
                            "Key": "cpu_usage",
                            "Value": "%s"
                       }""" % (origin, cpu),
                       {"Content-type": "application/json"})

    connection.getresponse()
    sys.exit(0)
else:
    print "Usage run_cron.py <Origin> <API Endpoint>"
    sys.exit(-1)