#!/usr/bin/python
import sys
import urllib
import urllib2

import psutil


if len(sys.argv) == 3:
    origin = str(sys.argv[1])
    endpoint = str(sys.argv[2])

    cpu = psutil.cpu_percent(5)

    url = 'http://%s/api/v1.0/metrics' % endpoint
    data = urllib.urlencode({'origin': origin,
                             'key': 'cpu_usage',
                             'value': cpu})
    urllib2.urlopen(url=url, data=data).read()
    sys.exit(0)
else:
    print "Usage run_cron.py <Origin> <API Endpoint>"
    sys.exit(-1)