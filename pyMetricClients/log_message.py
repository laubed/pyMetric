#!/usr/bin/python
import sys
import httplib
import urllib
import urllib2
import time

typedict = {"LOG": 0, "NOTICE": 1, "WARNING": 2, "ERROR": 3}


if len(sys.argv) == 5:
    origin = str(sys.argv[1])
    message = str(sys.argv[2])
    messagetype = str(typedict[str(sys.argv[3])])
    endpoint = str(sys.argv[4])

    url = 'http://%s/api/v1.0/messages' % endpoint
    data = urllib.urlencode({'origin': origin,
                             'message': message,
                             'type': messagetype,
                             'time': time.time()})
    urllib2.urlopen(url=url, data=data).read()
    sys.exit(0)
else:
    print "Usage log_message.py <Origin> <Message> <LOG|NOTICE|WARNING|ERROR> <API Endpoint>"
    sys.exit(-1)
