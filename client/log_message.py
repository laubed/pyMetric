#!/usr/bin/python
import sys
import httplib

typedict = {"LOG": 0, "NOTICE": 1, "WARNING": 2, "ERROR": 3}

if len(sys.argv) == 5:
    origin = str(sys.argv[1])
    message = str(sys.argv[2])
    messagetype = typedict[str(sys.argv[3])]
    endpoint = str(sys.argv[4])

    connection = httplib.HTTPConnection(endpoint)
    connection.request("POST", "/monitoring/api/v1.0/log_message",
                       '{"Origin":"' + origin + '", "Message": "' + message + '", "Type": "' + str(messagetype) + '"}',
                       {"Content-type": "application/json"})

    connection.getresponse()
    sys.exit(0)
else:
    print "Usage log_message.py <Origin> <Message> <LOG|NOTICE|WARNING|ERROR> <API Endpoint>"
    sys.exit(-1)
