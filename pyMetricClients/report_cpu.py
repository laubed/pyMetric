#!/usr/bin/python
import sys
import urllib
import urllib2

import psutil


if len(sys.argv) == 3:
    origin = str(sys.argv[1])
    endpoint = str(sys.argv[2])

    for x in range(60):
        cpu = psutil.cpu_percent(1, percpu=True)
        print cpu
        cpuvalue = 0
        for c in cpu:
            cpuvalue += c
        cpuvalue /= len(cpu)
        print cpuvalue

        url = 'http://%s/api/v1.0/metrics' % endpoint
        data = urllib.urlencode({'origin': origin,
                                 'key': 'cpu_usage',
                                 'value': cpuvalue})
        urllib2.urlopen(url=url, data=data).read()
    sys.exit(0)
else:
    print "Usage run_cron.py <Origin> <API Endpoint>"
    sys.exit(-1)